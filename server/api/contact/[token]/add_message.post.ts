import {
  contactTicketKey,
  demandLabels,
  publicTicket,
  type ContactTicket,
  type ContactTicketMessage,
} from '../../../utils/contactTickets';
import { sendSmtpEmail } from '../../../utils/email';

type MessageBody = {
  message?: string;
  authorName?: string;
};

const clean = (value: unknown) => typeof value === 'string' ? value.trim() : '';

export default defineEventHandler(async (event) => {
  const token = getRouterParam(event, 'token');

  if (!token) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Token manquant.',
    });
  }

  const key = contactTicketKey(token);
  const ticket = await useStorage('data').getItem<ContactTicket>(key);

  if (!ticket) {
    throw createError({
      statusCode: 404,
      statusMessage: 'Ticket introuvable.',
    });
  }

  const body = await readBody<MessageBody>(event);
  const message = clean(body.message).slice(0, 1200);

  if (!message) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Message obligatoire.',
    });
  }

  const now = new Date().toISOString();
  const ticketMessage: ContactTicketMessage = {
    id: `msg-${ticket.messages.length + 1}`,
    author: 'customer',
    authorName: clean(body.authorName) || ticket.organization || 'Client',
    message,
    attachments: [],
    createdAt: now,
  };

  ticket.messages.push(ticketMessage);
  ticket.updatedAt = now;

  await useStorage('data').setItem(key, ticket);

  const supportTo = clean(process.env.CONTACT_TO);

  if (supportTo) {
    const requestUrl = getRequestURL(event);
    const ticketUrl = new URL(`/ticket/${token}`, requestUrl.origin).toString();

    await sendSmtpEmail({
      to: supportTo,
      subject: `Nouveau message - ${ticket.ticketId}`,
      body: [
        `Ticket : ${ticket.ticketId}`,
        `Type : ${demandLabels[ticket.demandType]}`,
        `Client : ${ticket.organization}`,
        `Email : ${ticket.email}`,
        '',
        message,
        '',
        `Lien : ${ticketUrl}`,
      ].join('\n'),
      replyTo: ticket.email,
    });
  }

  return publicTicket(ticket);
});
