import { sendSmtpEmail } from './email';
import type { NotificationStatus, UrgencyTicket } from './urgencyTickets';
import { contactPreferenceLabels, expectedNextStepLabels, impactLabels, problemLabels } from './urgencyTickets';

const clean = (value: unknown) => typeof value === 'string' ? value.trim() : '';

const isCriticalImpact = (ticket: UrgencyTicket) => (
  ticket.impactLevel === 'blocked'
  || ticket.impactLevel === 'security_data_risk'
);

const buildInternalEmail = (ticket: UrgencyTicket) => ({
  subject: `[URGENT] ${ticket.reference} - ${problemLabels[ticket.problemType]}`,
  body: [
    `Reference : ${ticket.reference}`,
    `Impact : ${impactLabels[ticket.impactLevel]}`,
    `Type : ${problemLabels[ticket.problemType]}`,
    `URL : ${ticket.affectedUrl}`,
    `Depuis : ${ticket.sinceWhen}`,
    '',
    `Nom : ${ticket.name}`,
    `Structure : ${ticket.organization}`,
    `Email : ${ticket.email}`,
    `Telephone : ${ticket.phone}`,
    `Preference : ${contactPreferenceLabels[ticket.contactPreference]}`,
    `Creneau : ${ticket.callbackSlot}`,
    `Prochaine etape souhaitee : ${expectedNextStepLabels[ticket.expectedNextStep]}`,
    '',
    'Description :',
    ticket.shortDescription,
    '',
    'Rappel : aucun secret ne doit etre demande par email. Utiliser un canal adapte si un acces devient necessaire.',
  ].join('\n'),
});

const buildClientEmail = (ticket: UrgencyTicket) => ({
  subject: `Demande urgence recue - ${ticket.reference}`,
  body: [
    `Bonjour ${ticket.name},`,
    '',
    'Votre demande d urgence PixelProwlers a bien ete recue.',
    '',
    `Reference de dossier : ${ticket.reference}`,
    `URL concernee : ${ticket.affectedUrl}`,
    `Impact declare : ${impactLabels[ticket.impactLevel]}`,
    `Prochaine etape souhaitee : ${expectedNextStepLabels[ticket.expectedNextStep]}`,
    '',
    'Nous prenons connaissance de la situation et nous vous recontactons selon le moyen indique.',
    'Les modalites d intervention seront vues apres un premier echange humain.',
    '',
    'Important : ne transmettez pas de mot de passe, token, cle privee, acces administrateur ou information sensible par email ou formulaire.',
    'Vous pouvez conserver les preuves utiles de votre cote : captures d ecran, messages d erreur, heures approximatives, changements recents.',
    '',
    'PixelProwlers',
    'https://pixelprowlers.io',
  ].join('\n'),
});

const sendWebhook = async (ticket: UrgencyTicket): Promise<NotificationStatus> => {
  const url = clean(process.env.URGENCY_WEBHOOK_URL);

  if (!url) {
    return 'not_configured';
  }

  try {
    await $fetch(url, {
      method: 'POST',
      body: {
        reference: ticket.reference,
        problemType: ticket.problemType,
        problemLabel: problemLabels[ticket.problemType],
        impactLevel: ticket.impactLevel,
        impactLabel: impactLabels[ticket.impactLevel],
        affectedUrl: ticket.affectedUrl,
        createdAt: ticket.createdAt,
      },
      headers: clean(process.env.URGENCY_WEBHOOK_TOKEN)
        ? { Authorization: `Bearer ${clean(process.env.URGENCY_WEBHOOK_TOKEN)}` }
        : undefined,
      timeout: 6000,
    });

    return 'sent';
  } catch (error) {
    console.warn('[urgency] webhook notification failed:', error instanceof Error ? error.message : 'unknown error');
    return 'failed';
  }
};

const sendInternalSms = async (ticket: UrgencyTicket): Promise<NotificationStatus> => {
  const url = clean(process.env.URGENCY_SMS_WEBHOOK_URL);

  if (!isCriticalImpact(ticket)) {
    return 'skipped';
  }

  if (!url) {
    return 'not_configured';
  }

  try {
    await $fetch(url, {
      method: 'POST',
      body: {
        message: `PixelProwlers urgence critique ${ticket.reference} - ${impactLabels[ticket.impactLevel]} - ${ticket.affectedUrl}`,
      },
      headers: clean(process.env.URGENCY_SMS_WEBHOOK_TOKEN)
        ? { Authorization: `Bearer ${clean(process.env.URGENCY_SMS_WEBHOOK_TOKEN)}` }
        : undefined,
      timeout: 6000,
    });

    return 'sent';
  } catch (error) {
    console.warn('[urgency] sms notification failed:', error instanceof Error ? error.message : 'unknown error');
    return 'failed';
  }
};

export class NotificationService {
  // Orchestre les notifications sans exposer de contenu sensible dans les logs.
  async notifyUrgency(ticket: UrgencyTicket) {
    const internalTo = clean(process.env.URGENCY_INTERNAL_EMAIL || process.env.CONTACT_TO);
    const internalEmail = internalTo
      ? await sendSmtpEmail({
          to: internalTo,
          subject: buildInternalEmail(ticket).subject,
          body: buildInternalEmail(ticket).body,
          replyTo: ticket.email,
        })
      : 'not_configured';

    const clientEmailContent = buildClientEmail(ticket);
    const clientEmail = await sendSmtpEmail({
      to: ticket.email,
      subject: clientEmailContent.subject,
      body: clientEmailContent.body,
    });

    const [internalSms, webhook] = await Promise.all([
      sendInternalSms(ticket),
      sendWebhook(ticket),
    ]);

    return {
      internalEmail,
      clientEmail,
      internalSms,
      webhook,
    };
  }
}
