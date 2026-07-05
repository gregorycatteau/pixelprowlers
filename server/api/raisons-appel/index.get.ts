import { djangoApiBaseUrl } from '../../utils/djangoApi';

export default defineEventHandler(async () => (
  await $fetch(`${djangoApiBaseUrl()}/raisons-appel/`, { timeout: 8000 })
));
