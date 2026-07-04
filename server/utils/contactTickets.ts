import { randomBytes } from 'node:crypto';

export type ContactDemandType =
  | 'diagnostic'
  | 'urgency'
  | 'audit'
  | 'refonte'
  | 'transmission'
  | 'partnership';

export type ContactTicketStatus =
  | 'open'
  | 'in_progress'
  | 'waiting_customer'
  | 'resolved'
  | 'closed';

export type ContactTicketMessage = {
  id: string;
  author: 'customer' | 'support' | 'system';
  authorName: string;
  message: string;
  attachments: string[];
  createdAt: string;
};

export type ContactTicket = {
  ticketId: string;
  secretToken: string;
  organization: string;
  email: string;
  phone: string;
  demandType: ContactDemandType;
  message: string;
  status: ContactTicketStatus;
  messages: ContactTicketMessage[];
  emailConfirmation: {
    status: 'sent' | 'not_configured' | 'failed';
  };
  createdAt: string;
  updatedAt: string;
};

export const demandLabels: Record<ContactDemandType, string> = {
  diagnostic: 'Diagnostic',
  urgency: 'Urgence',
  audit: 'Audit',
  refonte: 'Refonte',
  transmission: 'Transmission',
  partnership: 'Partenariat / autre',
};

const currentYear = new Date().getFullYear();

export const publicTicket = (ticket: ContactTicket) => ({
  ticketId: ticket.ticketId,
  secretToken: ticket.secretToken,
  organization: ticket.organization,
  email: ticket.email,
  phone: ticket.phone,
  demandType: ticket.demandType,
  demandLabel: demandLabels[ticket.demandType],
  message: ticket.message,
  status: ticket.status,
  messages: ticket.messages,
  emailConfirmation: ticket.emailConfirmation,
  createdAt: ticket.createdAt,
  updatedAt: ticket.updatedAt,
});

export const createContactTicketId = async () => {
  const storage = useStorage('data');
  const key = `contact-ticket-counter:${currentYear}`;
  const current = Number(await storage.getItem<number>(key) || 0) + 1;
  await storage.setItem(key, current);
  return `PP-${currentYear}-${String(current).padStart(4, '0')}`;
};

export const createSecretToken = () => {
  return randomBytes(32).toString('hex');
};

export const contactTicketKey = (secretToken: string) => `contact-tickets:${secretToken}`;
