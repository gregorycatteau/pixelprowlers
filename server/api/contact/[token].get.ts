import { contactTicketKey, publicTicket, type ContactTicket } from '../../utils/contactTickets';

export default defineEventHandler(async (event) => {
  const token = getRouterParam(event, 'token');

  if (!token) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Token manquant.',
    });
  }

  const ticket = await useStorage('data').getItem<ContactTicket>(contactTicketKey(token));

  if (!ticket) {
    throw createError({
      statusCode: 404,
      statusMessage: 'Ticket introuvable.',
    });
  }

  return publicTicket(ticket);
});
