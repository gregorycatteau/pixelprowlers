/** Accept only the existing local ticket capability route. */
export const safeFollowupPath = (value?: string): boolean => /^\/ticket\/[A-Za-z0-9_-]{43}$/.test(value ?? '');
