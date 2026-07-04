import { NotificationService } from '../utils/notificationService';
import type { H3Event } from 'h3';
import {
  createUrgencyReference,
  urgencyTicketKey,
  type UrgencyContactPreference,
  type UrgencyExpectedNextStep,
  type UrgencyImpactLevel,
  type UrgencyProblemType,
  type UrgencyTicket,
} from '../utils/urgencyTickets';

type UrgencyBody = {
  problemType?: string;
  impactLevel?: string;
  affectedUrl?: string;
  shortDescription?: string;
  sinceWhen?: string;
  name?: string;
  organization?: string;
  email?: string;
  phone?: string;
  contactPreference?: string;
  callbackSlot?: string;
  expected_next_step?: string;
  consentToContact?: boolean;
  noSecretsConfirmed?: boolean;
  website?: string;
};

const problemTypes: UrgencyProblemType[] = [
  'site_down',
  'suspected_hack',
  'broken_form',
  'email_dns_domain',
  'content_modified',
  'critical_error',
  'massive_slowdown',
  'other',
];

const impactLevels: UrgencyImpactLevel[] = ['minor', 'disrupted', 'blocked', 'security_data_risk'];
const contactPreferences: UrgencyContactPreference[] = ['email', 'phone', 'either'];
const expectedNextSteps: UrgencyExpectedNextStep[] = [
  'understand_first',
  'quick_callback',
  'secure_before_action',
  'prepare_intervention',
  'need_guidance',
];
const singleLineFields = ['affectedUrl', 'sinceWhen', 'name', 'organization', 'email', 'phone', 'callbackSlot'] as const;

const clean = (value: unknown) => typeof value === 'string' ? value.trim() : '';

const containsCrlf = (value: string) => /[\r\n]/.test(value);

const hasLikelySecret = (value: string) => {
  const patterns = [
    /\b(password|passwd|pwd|token|api[_-]?key|secret|private[_-]?key|ssh-rsa|bearer)\b\s*[:=]/i,
    /-----BEGIN [A-Z ]*PRIVATE KEY-----/i,
    /\bghp_[A-Za-z0-9_]{20,}\b/,
    /\bsk-[A-Za-z0-9_-]{20,}\b/,
    /\bAKIA[0-9A-Z]{16}\b/,
  ];

  return patterns.some((pattern) => pattern.test(value));
};

const isEmailLike = (value: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);

const isPhoneLike = (value: string) => /^[+()\d\s.-]{6,24}$/.test(value);

const normalizeUrl = (value: string) => {
  try {
    const url = new URL(value);

    if (!['http:', 'https:'].includes(url.protocol)) {
      return '';
    }

    return url.toString();
  } catch {
    return '';
  }
};

const assertSameOrigin = (event: H3Event) => {
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

const clientKey = (event: H3Event) => {
  const forwarded = getHeader(event, 'x-forwarded-for') || '';
  const firstForwarded = forwarded.split(',')[0]?.trim();
  return firstForwarded || getRequestIP(event) || 'unknown';
};

const enforceRateLimit = async (event: H3Event) => {
  const storage = useStorage('data');
  const now = Date.now();
  const windowMs = 15 * 60 * 1000;
  const maxRequests = Number(process.env.URGENCY_RATE_LIMIT_MAX || '5');
  const key = `rate-limit:urgency:${clientKey(event)}`;
  const attempts = (await storage.getItem<number[]>(key) || []).filter((timestamp) => now - timestamp < windowMs);

  if (attempts.length >= maxRequests) {
    throw createError({
      statusCode: 429,
      statusMessage: 'Trop de demandes en peu de temps. Réessayez dans quelques minutes.',
    });
  }

  attempts.push(now);
  await storage.setItem(key, attempts);
};

const readLimitedField = (
  body: UrgencyBody,
  field: keyof UrgencyBody,
  maxLength: number,
  options: { required?: boolean; singleLine?: boolean } = {},
) => {
  const value = clean(body[field]);

  if (options.required && !value) {
    throw createError({ statusCode: 400, statusMessage: 'Des champs obligatoires sont manquants.' });
  }

  if (value.length > maxLength) {
    throw createError({ statusCode: 400, statusMessage: 'Un champ dépasse la longueur autorisée.' });
  }

  if (options.singleLine && containsCrlf(value)) {
    throw createError({ statusCode: 400, statusMessage: 'Un champ contient un saut de ligne non autorisé.' });
  }

  if (hasLikelySecret(value)) {
    throw createError({
      statusCode: 400,
      statusMessage: 'La demande semble contenir un secret. Retirez tout mot de passe, token, clé privée ou accès sensible.',
    });
  }

  return value;
};

export default defineEventHandler(async (event) => {
  assertSameOrigin(event);
  await enforceRateLimit(event);

  const body = await readBody<UrgencyBody>(event);

  if (clean(body.website)) {
    throw createError({ statusCode: 400, statusMessage: 'Demande refusée.' });
  }

  for (const field of singleLineFields) {
    const value = clean(body[field]);

    if (containsCrlf(value)) {
      throw createError({ statusCode: 400, statusMessage: 'Un champ contient un saut de ligne non autorisé.' });
    }
  }

  const problemType = problemTypes.includes(body.problemType as UrgencyProblemType)
    ? body.problemType as UrgencyProblemType
    : null;
  const impactLevel = impactLevels.includes(body.impactLevel as UrgencyImpactLevel)
    ? body.impactLevel as UrgencyImpactLevel
    : null;
  const contactPreference = contactPreferences.includes(body.contactPreference as UrgencyContactPreference)
    ? body.contactPreference as UrgencyContactPreference
    : null;
  const expectedNextStep = expectedNextSteps.includes(body.expected_next_step as UrgencyExpectedNextStep)
    ? body.expected_next_step as UrgencyExpectedNextStep
    : null;
  const affectedUrl = normalizeUrl(readLimitedField(body, 'affectedUrl', 240, { required: true, singleLine: true }));
  const shortDescription = readLimitedField(body, 'shortDescription', 700, { required: true });
  const sinceWhen = readLimitedField(body, 'sinceWhen', 120, { required: true, singleLine: true });
  const name = readLimitedField(body, 'name', 120, { required: true, singleLine: true });
  const organization = readLimitedField(body, 'organization', 160, { required: true, singleLine: true });
  const email = readLimitedField(body, 'email', 180, { required: true, singleLine: true }).toLowerCase();
  const phone = readLimitedField(body, 'phone', 40, { required: true, singleLine: true });
  const callbackSlot = readLimitedField(body, 'callbackSlot', 160, { required: true, singleLine: true });

  if (
    !problemType
    || !impactLevel
    || !contactPreference
    || !expectedNextStep
    || !affectedUrl
    || !isEmailLike(email)
    || !isPhoneLike(phone)
  ) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Vérifiez le type de problème, l impact, la prochaine étape, l URL, l email et le téléphone.',
    });
  }

  if (!body.consentToContact || !body.noSecretsConfirmed) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Les confirmations obligatoires doivent être cochées.',
    });
  }

  const createdAt = new Date().toISOString();
  const reference = await createUrgencyReference();
  const ticket: UrgencyTicket = {
    reference,
    problemType,
    impactLevel,
    affectedUrl,
    shortDescription,
    sinceWhen,
    name,
    organization,
    email,
    phone,
    contactPreference,
    callbackSlot,
    expectedNextStep,
    consentToContact: true,
    noSecretsConfirmed: true,
    status: 'open',
    notifications: {
      internalEmail: 'not_configured',
      clientEmail: 'not_configured',
      internalSms: 'skipped',
      webhook: 'not_configured',
    },
    createdAt,
  };

  ticket.notifications = await new NotificationService().notifyUrgency(ticket);
  await useStorage('data').setItem(urgencyTicketKey(reference), ticket);

  console.info(`[urgency] ticket ${reference} created.`);

  return {
    reference,
    status: ticket.status,
    clientEmailStatus: ticket.notifications.clientEmail,
    message: 'Demande urgente enregistrée.',
  };
});
