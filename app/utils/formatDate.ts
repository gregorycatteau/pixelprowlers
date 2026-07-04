export const formatDate = (value: string) => new Intl.DateTimeFormat('fr-FR', {
  dateStyle: 'medium',
  timeStyle: 'short',
}).format(new Date(value));

export const maskEmail = (email: string) => {
  const [name, domain] = email.split('@');

  if (!name || !domain) {
    return '';
  }

  return `${name.slice(0, 2)}***@${domain}`;
};

export const isEmailLike = (value: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
