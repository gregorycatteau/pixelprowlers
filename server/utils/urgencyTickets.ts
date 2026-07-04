import { randomInt } from 'node:crypto';

export type UrgencyProblemType =
  | 'site_down'
  | 'suspected_hack'
  | 'broken_form'
  | 'email_dns_domain'
  | 'content_modified'
  | 'critical_error'
  | 'massive_slowdown'
  | 'other';

export type UrgencyImpactLevel =
  | 'minor'
  | 'disrupted'
  | 'blocked'
  | 'security_data_risk';

export type UrgencyContactPreference =
  | 'email'
  | 'phone'
  | 'either';

export type UrgencyExpectedNextStep =
  | 'understand_first'
  | 'quick_callback'
  | 'secure_before_action'
  | 'prepare_intervention'
  | 'need_guidance';

export type NotificationStatus = 'sent' | 'not_configured' | 'failed' | 'skipped';

export type UrgencyTicket = {
  reference: string;
  problemType: UrgencyProblemType;
  impactLevel: UrgencyImpactLevel;
  affectedUrl: string;
  shortDescription: string;
  sinceWhen: string;
  name: string;
  organization: string;
  email: string;
  phone: string;
  contactPreference: UrgencyContactPreference;
  callbackSlot: string;
  expectedNextStep: UrgencyExpectedNextStep;
  consentToContact: true;
  noSecretsConfirmed: true;
  status: 'open';
  notifications: {
    internalEmail: NotificationStatus;
    clientEmail: NotificationStatus;
    internalSms: NotificationStatus;
    webhook: NotificationStatus;
  };
  createdAt: string;
};

export const problemLabels: Record<UrgencyProblemType, string> = {
  site_down: 'Site inaccessible',
  suspected_hack: 'Suspicion de piratage',
  broken_form: 'Formulaire cassé',
  email_dns_domain: 'Problème email / DNS / domaine',
  content_modified: 'Contenu modifié',
  critical_error: 'Erreur critique',
  massive_slowdown: 'Ralentissement massif',
  other: 'Autre',
};

export const impactLabels: Record<UrgencyImpactLevel, string> = {
  minor: 'Simple gêne',
  disrupted: 'Activité perturbée',
  blocked: 'Activité bloquée',
  security_data_risk: 'Risque sécurité / données',
};

export const contactPreferenceLabels: Record<UrgencyContactPreference, string> = {
  email: 'Email',
  phone: 'Téléphone',
  either: 'Email ou téléphone',
};

export const expectedNextStepLabels: Record<UrgencyExpectedNextStep, string> = {
  understand_first: 'Je veux d’abord comprendre ce qui se passe',
  quick_callback: 'Je souhaite être rappelé rapidement',
  secure_before_action: 'Je veux sécuriser la situation avant d’agir',
  prepare_intervention: 'Je veux préparer une intervention si nécessaire',
  need_guidance: 'Je ne sais pas encore, j’ai besoin d’être guidé',
};

const formatDatePart = (date: Date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}${month}${day}`;
};

// Génère une référence courte, stable et non prédictible pour le suivi client.
export const createUrgencyReference = async (date = new Date()) => {
  const storage = useStorage('data');
  const datePart = formatDatePart(date);

  for (let attempt = 0; attempt < 12; attempt += 1) {
    const suffix = String(randomInt(0, 10000)).padStart(4, '0');
    const reference = `PXP-URG-${datePart}-${suffix}`;
    const key = urgencyTicketKey(reference);
    const existing = await storage.getItem(key);

    if (!existing) {
      return reference;
    }
  }

  throw new Error('Unable to create unique urgency reference');
};

export const urgencyTicketKey = (reference: string) => `urgency-tickets:${reference}`;
