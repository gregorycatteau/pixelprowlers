import { djangoApiBaseUrl } from '../../utils/djangoApi';

export default defineEventHandler(async (event) => {
  const reference = getRouterParam(event, 'reference');

  if (!reference) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Référence manquante.',
    });
  }

  return await $fetch(`${djangoApiBaseUrl()}/audit-refonte/${encodeURIComponent(reference)}/`, {
    timeout: 8000,
  });
});
