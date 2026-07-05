import { djangoApiBaseUrl } from '../../utils/djangoApi';

type CitationResponse = {
  id: number;
  numero?: number;
  texte: string;
  auteur: string;
  source?: string;
};

export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  const excludeId = typeof query.exclude_id === 'string' && /^\d+$/.test(query.exclude_id)
    ? query.exclude_id
    : '';
  const url = new URL(`${djangoApiBaseUrl()}/citations/random/`);

  if (excludeId) {
    url.searchParams.set('exclude_id', excludeId);
  }

  try {
    return await $fetch<CitationResponse>(url.toString(), { timeout: 8000 });
  } catch {
    return {
      id: 0,
      texte: "Il n'est jamais trop tard pour remettre de l'ordre dans ce qui compte.",
      auteur: 'PixelProwlers',
      source: '',
    };
  }
});
