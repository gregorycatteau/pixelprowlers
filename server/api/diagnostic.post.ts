import net from 'node:net';
import tls from 'node:tls';

type DiagnosticPath = 'CRITICAL' | 'AUDIT' | 'TRANSMISSION' | 'MAINTENANCE';

type DiagnosticAnswers = {
  structure?: string;
  structureOther?: string;
  stress?: string;
  siteState?: string;
  dependency?: string;
};

type DiagnosticContact = {
  name?: string;
  email?: string;
  phone?: string;
  message?: string;
};

type DiagnosticTicket = {
  id: string;
  organization: string;
  email: string;
  phone: string;
  message: string;
  status: 'open';
  answers: DiagnosticAnswers;
  diagnosticResult: {
    path: DiagnosticPath;
    scores: {
      urgency: number;
      fragility: number;
      dependency: number;
      total: number;
    };
    timestamp: string;
  };
  emailConfirmation: {
    subject: string;
    body: string;
    status: 'sent' | 'not_configured' | 'failed';
  };
  createdAt: string;
};

type DiagnosticBody = {
  answers?: DiagnosticAnswers;
  contact?: DiagnosticContact;
};

const currentYear = new Date().getFullYear();

const assertString = (value: unknown) => typeof value === 'string' ? value.trim() : '';

const isEmailLike = (value: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);

const redactEmail = (email: string) => {
  const [name, domain] = email.split('@');
  return `${name.slice(0, 2)}***@${domain}`;
};

const createTicketId = () => {
  const randomPart = Math.random().toString(36).slice(2, 8).toUpperCase();
  return `PP-${currentYear}-${randomPart}`;
};

const analyzeDiagnostic = (answers: DiagnosticAnswers) => {
  let urgency = 0;
  let fragility = 0;
  let dependency = 0;

  if (answers.stress === 'site-slow' || answers.stress === 'single-person' || answers.stress === 'backups') {
    urgency += 2;
  }

  if (answers.siteState === 'fragile') {
    fragility += 2;
  }

  if (answers.dependency === 'one') {
    dependency += 3;
  } else if (answers.dependency === 'unclear') {
    dependency += 2;
  }

  const total = urgency + fragility + dependency;
  let path: DiagnosticPath = 'MAINTENANCE';

  if (total >= 7) {
    path = 'CRITICAL';
  } else if (fragility >= 2) {
    path = 'AUDIT';
  } else if (dependency >= 2) {
    path = 'TRANSMISSION';
  } else if (urgency >= 2 || answers.stress === 'some' || answers.siteState === 'doubt') {
    path = 'AUDIT';
  }

  return {
    path,
    scores: {
      urgency,
      fragility,
      dependency,
      total,
    },
  };
};

const escapeHeader = (value: string) => value.replace(/[\r\n]/g, ' ').trim();

const smtpConfig = () => {
  const host = assertString(process.env.SMTP_HOST);
  const user = assertString(process.env.SMTP_USER);
  const pass = assertString(process.env.SMTP_PASS);
  const from = assertString(process.env.CONTACT_FROM);
  const port = Number(assertString(process.env.SMTP_PORT) || '587');
  const secure = assertString(process.env.SMTP_SECURE).toLowerCase() === 'true';

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

  const close = () => {
    socket.end();
  };

  return { command, waitReady, startTls, close };
};

const sendEmail = async (email: { to: string; subject: string; body: string }) => {
  const config = smtpConfig();

  if (!config) {
    return 'not_configured' as const;
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
      `Subject: ${escapeHeader(email.subject)}`,
      'MIME-Version: 1.0',
      'Content-Type: text/plain; charset=utf-8',
      'Content-Transfer-Encoding: 8bit',
      '',
      dotStuff(email.body),
      '.',
    ].join('\r\n'), [250]);
    await client.command('QUIT', [221]);

    return 'sent' as const;
  } catch (error) {
    console.warn('[diagnostic] confirmation email failed:', error instanceof Error ? error.message : 'unknown error');
    return 'failed' as const;
  } finally {
    client.close();
  }
};

const buildConfirmationEmail = (
  ticket: Pick<DiagnosticTicket, 'id' | 'organization' | 'email'>,
  resultUrl: string,
): DiagnosticTicket['emailConfirmation'] => {

  return {
    subject: `Votre diagnostic PixelProwlers - Ticket ${ticket.id}`,
    body: [
      `Bonjour ${ticket.organization},`,
      '',
      "Merci d'avoir répondu à notre diagnostic.",
      '',
      `Voici votre analyse personnalisée : ${resultUrl}`,
      '',
      'Vous pouvez revenir à cette page quand vous voulez.',
      'Le ticket reste ouvert pour que vous nous contactiez si besoin.',
      '',
      'Si vous avez des questions : contact@pixelprowlers.io',
      '',
      'À bientôt,',
      'Grégory',
      'PixelProwlers',
    ].join('\n'),
    status: 'not_configured' as const,
  };
};

export default defineEventHandler(async (event) => {
  const body = await readBody<DiagnosticBody>(event);
  const answers = body.answers || {};
  const contact = body.contact || {};
  const organization = assertString(contact.name);
  const email = assertString(contact.email).toLowerCase();
  const phone = assertString(contact.phone);
  const message = assertString(contact.message).slice(0, 240);

  if (!organization || !email || !isEmailLike(email) || !message) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Nom, email valide et contexte sont obligatoires.',
    });
  }

  const analyzed = analyzeDiagnostic(answers);
  const id = createTicketId();
  const createdAt = new Date().toISOString();
  const requestUrl = getRequestURL(event);
  const resultUrl = new URL(`/diagnostic-result/${id}`, requestUrl.origin).toString();
  const emailConfirmation = buildConfirmationEmail({ id, organization, email }, resultUrl);
  emailConfirmation.status = await sendEmail({
    to: email,
    subject: emailConfirmation.subject,
    body: emailConfirmation.body,
  });
  const ticket: DiagnosticTicket = {
    id,
    organization,
    email,
    phone,
    message,
    status: 'open',
    answers,
    diagnosticResult: {
      ...analyzed,
      timestamp: createdAt,
    },
    emailConfirmation,
    createdAt,
  };

  await useStorage('data').setItem(`diagnostic-tickets:${id}`, ticket);

  console.info(
    `[diagnostic] ticket ${id} created for ${redactEmail(email)}. Confirmation email status: ${emailConfirmation.status}.`,
  );

  return {
    ticketId: id,
    redirectTo: `/diagnostic-result/${id}`,
    path: analyzed.path,
  };
});
