import { djangoApiBaseUrl } from '../../utils/djangoApi';

export default defineEventHandler(async () => (
  await $fetch(`${djangoApiBaseUrl()}/motifs/`, { timeout: 8000 })
));
