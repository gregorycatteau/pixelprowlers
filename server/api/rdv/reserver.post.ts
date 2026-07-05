import { assertSameOrigin, postToDjango } from '../../utils/djangoApi';

export default defineEventHandler(async (event) => {
  assertSameOrigin(event);
  const body = await readBody(event);
  return await postToDjango('/rdv/reserver/', body);
});
