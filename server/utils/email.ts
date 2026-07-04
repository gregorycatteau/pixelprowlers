import net from 'node:net';
import tls from 'node:tls';

type EmailPayload = {
  to: string;
  subject: string;
  body: string;
  replyTo?: string;
};

type EmailStatus = 'sent' | 'not_configured' | 'failed';

const clean = (value: unknown) => typeof value === 'string' ? value.trim() : '';

const escapeHeader = (value: string) => value.replace(/[\r\n]/g, ' ').trim();

const smtpConfig = () => {
  const host = clean(process.env.SMTP_HOST);
  const user = clean(process.env.SMTP_USER);
  const pass = clean(process.env.SMTP_PASS);
  const from = clean(process.env.CONTACT_FROM);
  const port = Number(clean(process.env.SMTP_PORT) || '587');
  const secure = clean(process.env.SMTP_SECURE).toLowerCase() === 'true';

  if (!host || !user || !pass || !from || !Number.isFinite(port)) {
    return null;
  }

  return { host, user, pass, from, port, secure };
};

const encodeBase64 = (value: string) => Buffer.from(value, 'utf8').toString('base64');

const dotStuff = (body: string) => body.replace(/\r?\n/g, '\r\n').replace(/^\./gm, '..');

const createSmtpClient = async (config: NonNullable<ReturnType<typeof smtpConfig>>) => {
  let socket: net.Socket | tls.TLSSocket = config.secure
    ? tls.connect({ host: config.host, port: config.port, servername: config.host })
    : net.connect({ host: config.host, port: config.port });

  socket.setTimeout(10000);

  const readLine = () => new Promise<string>((resolve, reject) => {
    let buffer = '';

    const cleanup = () => {
      socket.off('data', onData);
      socket.off('error', onError);
      socket.off('timeout', onTimeout);
    };

    const onData = (chunk: Buffer) => {
      buffer += chunk.toString('utf8');
      const lines = buffer.split(/\r?\n/).filter(Boolean);
      const last = lines.at(-1);

      if (last && /^\d{3} /.test(last)) {
        cleanup();
        resolve(buffer);
      }
    };

    const onError = (error: Error) => {
      cleanup();
      reject(error);
    };

    const onTimeout = () => {
      cleanup();
      reject(new Error('SMTP timeout'));
    };

    socket.on('data', onData);
    socket.on('error', onError);
    socket.on('timeout', onTimeout);
  });

  const command = async (line: string, expected: number[]) => {
    socket.write(`${line}\r\n`);
    const response = await readLine();
    const code = Number(response.slice(0, 3));

    if (!expected.includes(code)) {
      throw new Error(`SMTP command failed with ${code}`);
    }

    return response;
  };

  const waitReady = async () => {
    const response = await readLine();
    const code = Number(response.slice(0, 3));

    if (code !== 220) {
      throw new Error(`SMTP server not ready: ${code}`);
    }
  };

  const startTls = async () => {
    await command('STARTTLS', [220]);
    socket = tls.connect({ socket, servername: config.host });
    await new Promise<void>((resolve, reject) => {
      socket.once('secureConnect', resolve);
      socket.once('error', reject);
    });
  };

  return {
    command,
    waitReady,
    startTls,
    close: () => socket.end(),
  };
};

export const sendSmtpEmail = async (email: EmailPayload): Promise<EmailStatus> => {
  const config = smtpConfig();

  if (!config) {
    return 'not_configured';
  }

  const client = await createSmtpClient(config);

  try {
    await client.waitReady();
    const ehlo = await client.command('EHLO pixelprowlers.local', [250]);

    if (!config.secure && ehlo.includes('STARTTLS')) {
      await client.startTls();
      await client.command('EHLO pixelprowlers.local', [250]);
    }

    await client.command(`AUTH PLAIN ${encodeBase64(`\u0000${config.user}\u0000${config.pass}`)}`, [235]);
    await client.command(`MAIL FROM:<${config.from}>`, [250]);
    await client.command(`RCPT TO:<${email.to}>`, [250, 251]);
    await client.command('DATA', [354]);
    await client.command([
      `From: PixelProwlers <${escapeHeader(config.from)}>`,
      `To: ${escapeHeader(email.to)}`,
      email.replyTo ? `Reply-To: ${escapeHeader(email.replyTo)}` : '',
      `Subject: ${escapeHeader(email.subject)}`,
      'MIME-Version: 1.0',
      'Content-Type: text/plain; charset=utf-8',
      'Content-Transfer-Encoding: 8bit',
      '',
      dotStuff(email.body),
      '.',
    ].filter(Boolean).join('\r\n'), [250]);
    await client.command('QUIT', [221]);

    return 'sent';
  } catch (error) {
    console.warn('[email] send failed:', error instanceof Error ? error.message : 'unknown error');
    return 'failed';
  } finally {
    client.close();
  }
};
