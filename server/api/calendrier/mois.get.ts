import { djangoApiBaseUrl } from '../../utils/djangoApi';

export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  const url = new URL(`${djangoApiBaseUrl()}/calendrier/mois/`);
  if (typeof query.annee === 'string') url.searchParams.set('annee', query.annee);
  if (typeof query.mois === 'string') url.searchParams.set('mois', query.mois);
  return await $fetch(url.toString(), { timeout: 8000 });
});
