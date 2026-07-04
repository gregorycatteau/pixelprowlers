import {
  contactTicketKey,
  createContactTicketId,
  createSecretToken,
  demandLabels,
  publicTicket,
  type ContactDemandType,
  type ContactTicket,
} from '../utils/contactTickets';
import { sendSmtpEmail } from '../utils/email';

type ContactBody = {
  demandType?: ContactDemandType;
  organization?: string;
  email?: string;
  phone?: string;
  message?: string;
};

const demandValues: ContactDemandType[] = ['diagnostic', 'urgency', 'audit', 'refonte', 'transmission', 'partnership'];

const clean = (value: unknown) => typeof value === 'string' ? value.trim() : '';

const isEmailLike = (value: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);

const redactEmail = (email: string) => {
  const [name, domain] = email.split('@');
  return `${name.slice(0, 2)}***@${domain}`;
};

const buildConfirmationEmail = (ticket: ContactTicket, ticketUrl: string) => ({
  subject: `Votre ticket a été créé - ${ticket.ticketId}`,
  body: [
    `Bonjour ${ticket.organization},`,
    '',
    "Merci de nous avoir contacté. Voici les détails de votre demande :",
    '',
    '---',
    `TICKET : ${ticket.ticketId}`,
    `Type : ${demandLabels[ticket.demandType]}`,
    `Créé : ${new Date(ticket.createdAt).toLocaleString('fr-FR')}`,
    'Statut : Ouvert',
    '---',
    '',
    'Votre situation :',
    ticket.message,
    '',
    '---',
    '',
    'Prochaines étapes :',
    '1. On analyse votre demande (24h)',
    '2. On vous recontacte par email ou téléphone',
    '3. On discute ensemble des solutions',
    '4. Suivi en temps réel via votre ticket',
    '',
    '---',
    '',
    'Consulter votre ticket :',
    ticketUrl,
    '',
    `Numéro : ${ticket.ticketId}`,
    '',
    'Questions ? Répondez directement à cet email ou consultez votre ticket.',
    '',
    'À bientôt,',
    'Grégory',
    'PixelProwlers',
  ].join('\n'),
});

export default defineEventHandler(async (event) => {
  const body = await readBody<ContactBody>(event);
  const demandType = demandValues.includes(body.demandType as ContactDemandType)
    ? body.demandType as ContactDemandType
    : null;
  const organization = clean(body.organization);
  const email = clean(body.email).toLowerCase();
  const phone = clean(body.phone);
  const message = clean(body.message).slice(0, 500);

  if (!demandType || !organization || !email || !isEmailLike(email) || !message) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Type, prénom/organisation, email valide et problématique sont obligatoires.',
    });
  }

  const now = new Date().toISOString();
  const ticketId = await createContactTicketId();
  const secretToken = createSecretToken();
  const ticket: ContactTicket = {
    ticketId,
    secretToken,
    organization,
    email,
    phone,
    demandType,
    message,
    status: 'open',
    messages: [
      {
        id: 'msg-1',
        author: 'system',
        authorName: 'PixelProwlers',
        message: `Ticket créé : ${demandLabels[demandType]}.`,
        attachments: [],
        createdAt: now,
      },
      {
        id: 'msg-2',
        author: 'customer',
        authorName: organization,
        message,
        attachments: [],
        createdAt: now,
      },
    ],
    emailConfirmation: {
      status: 'not_configured',
    },
    createdAt: now,
    updatedAt: now,
  };

  const requestUrl = getRequestURL(event);
  const ticketUrl = new URL(`/ticket/${secretToken}`, requestUrl.origin).toString();
  const confirmationEmail = buildConfirmationEmail(ticket, ticketUrl);
  ticket.emailConfirmation.status = await sendSmtpEmail({
    to: email,
    subject: confirmationEmail.subject,
    body: confirmationEmail.body,
    replyTo: email,
  });

  await useStorage('data').setItem(contactTicketKey(secretToken), ticket);

  const supportTo = clean(process.env.CONTACT_TO);

  if (supportTo) {
    await sendSmtpEmail({
      to: supportTo,
      subject: `Nouveau ticket ${ticket.ticketId} - ${demandLabels[demandType]}`,
      body: [
        `Ticket : ${ticket.ticketId}`,
        `Type : ${demandLabels[demandType]}`,
        `Organisation : ${organization}`,
        `Email : ${email}`,
        `Téléphone : ${phone || 'non renseigné'}`,
        '',
        message,
        '',
        `Lien : ${ticketUrl}`,
      ].join('\n'),
      replyTo: email,
    });
  }

  console.info(`[contact] ticket ${ticketId} created for ${redactEmail(email)}.`);

  return {
    ...publicTicket(ticket),
    ticketUrl: `/ticket/${secretToken}`,
    confirmationUrl: `/contact/confirmation?token=${secretToken}`,
  };
});
