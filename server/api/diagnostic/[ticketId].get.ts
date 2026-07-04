export default defineEventHandler(async (event) => {
  const ticketId = getRouterParam(event, 'ticketId');

  if (!ticketId) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Ticket manquant.',
    });
  }

  const ticket = await useStorage('data').getItem(`diagnostic-tickets:${ticketId}`);

  if (!ticket) {
    throw createError({
      statusCode: 404,
      statusMessage: 'Ticket introuvable.',
    });
  }

  return ticket;
});
