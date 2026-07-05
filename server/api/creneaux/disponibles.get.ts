import { djangoApiBaseUrl } from '../../utils/djangoApi';

export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  const url = new URL(`${djangoApiBaseUrl()}/creneaux/disponibles/`);
  for (const key of ['motif', 'date_debut', 'date_fin', 'urgence']) {
    const value = query[key];
    if (typeof value === 'string') url.searchParams.set(key, value);
  }
  return await $fetch(url.toString(), { timeout: 8000 });
});
