import { describe, expect, it } from 'vitest';
import { safeFollowupPath } from './followup';

describe('Liens personnels de suivi', () => {
  it('accepte uniquement la route locale avec la capacité complète', () => {
    expect(safeFollowupPath('/ticket/' + 'a'.repeat(43))).toBe(true);
    for (const value of [undefined, '/ticket/1', '//evil.invalid/ticket/' + 'a'.repeat(43), 'https://evil.invalid', '/admin/']) {
      expect(safeFollowupPath(value)).toBe(false);
    }
  });
});
