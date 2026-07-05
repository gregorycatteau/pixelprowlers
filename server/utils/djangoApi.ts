import type { H3Event } from 'h3';

const clean = (value: unknown) => typeof value === 'string' ? value.trim().replace(/\/+$/, '') : '';

export const djangoApiBaseUrl = () => (
  clean(process.env.DJANGO_API_BASE_URL)
  || clean(process.env.NUXT_DJANGO_API_BASE_URL)
  || 'http://127.0.0.1:8000/api'
);

export const postToDjango = async <T>(path: string, body: unknown) => {
  const baseUrl = djangoApiBaseUrl();

  try {
    return await $fetch<T>(`${baseUrl}${path}`, {
      method: 'POST',
      body,
      timeout: 10000,
    });
  } catch (error) {
    const statusMessage = typeof error === 'object' && error && 'statusMessage' in error
      ? String(error.statusMessage)
      : '';

    throw createError({
      statusCode: 502,
      statusMessage: statusMessage || "L'API d'audit est indisponible pour le moment.",
    });
  }
};

export const assertSameOrigin = (event: H3Event) => {
  const origin = getHeader(event, 'origin');

  if (!origin) {
    return;
  }

  const requestUrl = getRequestURL(event);

  if (new URL(origin).host !== requestUrl.host) {
    throw createError({
      statusCode: 403,
      statusMessage: 'Origine de requête refusée.',
    });
  }
};
