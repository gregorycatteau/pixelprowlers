import { beforeEach, describe, expect, it, vi } from 'vitest';
import { useContactForm } from './useContact';
import { graphqlRequest } from '~/utils/graphql';
import { contactApiMapping } from '~/utils/contactNeeds';

vi.mock('~/utils/graphql', () => ({ graphqlRequest: vi.fn(), parseGraphqlJson: (value: unknown, fallback: unknown) => value || fallback }));
const request = vi.mocked(graphqlRequest);
const fixture = { ticketId: 'test-reference', secretToken: 'dummy-test-token', name: 'Demande de test', company: '', email: 'test@example.invalid', phone: '', demandType: 'partnership', demandLabel: 'Test', message: 'Texte de test', status: 'open', messages: [], emailConfirmation: { status: 'not_configured' } };
/** Prépare une saisie fictive valide sans destinataire réel. */
const filled = (need = 'reparation' as keyof typeof contactApiMapping) => {
  const state = useContactForm(need);
  Object.assign(state.form, { organization: 'Test contrôlé', email: 'test@example.invalid', message: 'Mon appareil ne démarre plus depuis hier.', model: 'Modèle test' });
  return state;
};

beforeEach(() => { request.mockReset(); });
describe('Envoi et conservation du contact', () => {
  it.each(Object.keys(contactApiMapping) as Array<keyof typeof contactApiMapping>)('envoie le mapping reconnu pour %s', async need => {
    request.mockResolvedValue({ createContact: { contact: fixture } });
    const state = filled(need);
    const result = await state.submit();
    expect(result?.ticketId).toBe('test-reference');
    expect(request.mock.calls[0]?.[1]).toMatchObject(contactApiMapping[need]);
    expect(request.mock.calls[0]?.[1]).toMatchObject({ privacyConsent: true });
    expect(state.isSubmitting.value).toBe(false);
  });
  it('envoie le nom sans le dupliquer comme société et ne transmet que les détails actifs', async () => {
    request.mockResolvedValue({ createContact: { contact: fixture } });
    const state = filled();
    state.form.usage = 'Usage conservé localement';
    state.form.budget = 'Budget conservé localement';
    await state.submit();
    expect(request.mock.calls[0]?.[1]).toMatchObject({ name: 'Test contrôlé', company: '' });
    expect(request.mock.calls[0]?.[1]?.message).not.toContain('Usage conservé localement');
    state.form.need = 'reemploi';
    await state.submit();
    expect(request.mock.calls[1]?.[1]?.message).toContain('Usage conservé localement');
    expect(request.mock.calls[1]?.[1]?.message).not.toContain('Modèle test');
    expect(state.form.model).toBe('Modèle test');
  });
  it('conserve tous les champs après erreur réseau et permet une nouvelle tentative', async () => {
    request.mockRejectedValueOnce(new Error('Network unavailable'));
    const state = filled();
    const original = { ...state.form };
    expect(await state.submit()).toBeNull();
    expect(state.form).toEqual(original);
    expect(state.submitError.value.length).toBeGreaterThan(0);
    expect(state.isSubmitting.value).toBe(false);
    request.mockResolvedValueOnce({ createContact: { contact: fixture } });
    expect(await state.submit()).not.toBeNull();
    expect(state.submitError.value).toBe('');
  });
  it('traite une réponse sans contact comme un échec sans effacer la saisie', async () => {
    request.mockResolvedValue({ createContact: { contact: null } });
    const state = filled();
    expect(await state.submit()).toBeNull();
    expect(state.form.model).toBe('Modèle test');
    expect(state.submitError.value).not.toBe('');
  });
  it('empêche un second envoi pendant l’attente', async () => {
    let finish!: (value: unknown) => void;
    request.mockImplementation(() => new Promise(resolve => { finish = resolve; }) as ReturnType<typeof graphqlRequest>);
    const state = filled();
    const pending = state.submit();
    expect(state.isSubmitting.value).toBe(true);
    expect(await state.submit()).toBeNull();
    expect(request).toHaveBeenCalledTimes(1);
    finish({ createContact: { contact: fixture } });
    await pending;
    expect(state.isSubmitting.value).toBe(false);
  });
  it('refuse un besoin inconnu, une description trop courte et un dépassement sans appeler l’API', async () => {
    const state = filled();
    state.form.need = '';
    expect(await state.submit()).toBeNull();
    state.form.need = 'reparation';
    state.form.message = 'Court';
    expect(await state.submit()).toBeNull();
    state.form.message = 'x'.repeat(501);
    expect(await state.submit()).toBeNull();
    state.form.message = 'Message suffisamment long pour être envoyé.';
    state.form.model = 'x'.repeat(4000);
    expect(await state.submit()).toBeNull();
    expect(request).not.toHaveBeenCalled();
  });
});

describe('Message enrichi du parcours', () => {
  it('refuse le dépassement de 4000 caractères sans tronquer ni envoyer', async () => {
    const state = filled(); state.form.repairContext = 'Contexte fictif '.repeat(300);
    const original = state.form.repairContext;
    expect(state.canSubmit.value).toBe(false); expect(await state.submit()).toBeNull();
    expect(request).not.toHaveBeenCalled(); expect(state.form.repairContext).toBe(original);
  });
  it('garde le contexte après erreur et transmet sa mise à jour au réessai', async () => {
    const state = filled(); state.form.repairContext = 'Symptôme : Ne charge plus\nGrille : TEST';
    request.mockRejectedValueOnce(new Error('Échec contrôlé')); await state.submit();
    expect(state.form.repairContext).toContain('Ne charge plus');
    state.form.repairContext = 'Symptôme : Ne démarre plus\nGrille : TEST';
    request.mockResolvedValueOnce({ createContact: { contact: fixture } }); await state.submit();
    expect(request.mock.calls[1]?.[1]?.message).toContain('Ne démarre plus');
    expect(request.mock.calls[1]?.[1]?.message).not.toContain('Ne charge plus');
  });
});
