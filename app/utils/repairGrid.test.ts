import { describe, expect, it } from 'vitest';
import { budgetLabel, publishedRepairGrid as grid, validEstimate, resolveScenarios, offersForFamily, diagnosticSettlement, diagnosticPresentation, precisionOptions } from './repairGrid';
const offer = (id: string) => grid.offers.find(o => o.id === id)!;
describe('Grille publique autorisée, montants consommateurs en centimes', () => {
  it('conserve les 41 offres et leurs montants sans conversion de TVA', () => {
    const expected: Record<string, number | number[]> = {
      orientation: 0, 'diagnostic-standard': 4900, 'diagnostic-electronique': 8900,
      'phone-port-clean': 3900, 'phone-battery': [8900,12900], 'phone-screen-lcd': [9900,15900], 'phone-screen-oled': [14900,23900], 'phone-screen-original': [21900,44900], 'phone-charge-module': [9900,15900], 'phone-charge-soldered': [13900,20900], 'phone-board': [16900,29900],
      'tablet-battery': [13900,21900], 'tablet-screen-lcd': [14900,24900], 'tablet-screen-oled': [22900,47900], 'tablet-charge-soldered': [15900,24900],
      'desktop-thermal':7900, 'laptop-thermal':9900, 'laptop-thermal-complex':[14900,19900], 'computer-software':[8900,12900], 'computer-reinstall':11900, 'computer-reinstall-transfer':[16900,21900], 'computer-ssd':[9900,16900], 'computer-ssd-clone':[14900,22900], 'laptop-battery':[9900,16900], 'laptop-screen':[14900,25900], 'laptop-keyboard':[12900,21900], 'laptop-dcjack':[11900,17900], 'laptop-usbc':[14900,22900], 'computer-bios':[14900,19900], 'computer-board':[21900,37900], 'macbook-board':[29900,49900],
      'console-thermal':[9900,14900], 'console-hdmi-ps4-xbox':[12900,17900], 'console-hdmi-ps5':[15900,19900], 'console-usbc-switch':[13900,18900], 'console-board':[21900,34900], 'controller-drift-one':[5900,7900], 'controller-drift-two':[8900,10900], 'controller-charge':[5900,8900], 'controller-hall-tmr':[8900,11900], 'liquid-treatment':[14900,24900],
    };
    expect(grid.offers).toHaveLength(Object.keys(expected).length);
    for (const [id, amount] of Object.entries(expected)) {
      const e = offer(id).estimate; expect(validEstimate(e)).toBe(true);
      expect(e.kind === 'range' ? [e.min,e.max] : e.amount).toEqual(amount);
      expect(offer(id).scope.length).toBeGreaterThan(10);
    }
    expect(new Set(grid.offers.map(o => o.id)).size).toBe(grid.offers.length);
    expect(budgetLabel(offer('phone-port-clean').estimate)).toMatch(/^39\s*€/);
    expect(budgetLabel(offer('orientation').estimate)).toBe('Gratuite');
  });
  it('ne traite ni une absence ni des centimes fractionnaires comme un prix nul', () => {
    for (const amount of [undefined, NaN, -1, 1.5]) expect(validEstimate({ kind: 'fixed', amount: amount as number, includes: [], excludes: [] })).toBe(false);
    expect(validEstimate({ kind: 'range', min: 5000, max:1000, includes: [], excludes: [] })).toBe(false);
  });
  it('ne publie jamais Hall/TMR et ne fabrique aucune validation technique', () => {
    expect(offer('controller-hall-tmr').published).toBe(false);
    expect(offersForFamily(grid,'controller').map(o => o.id)).not.toContain('controller-hall-tmr');
    expect(JSON.stringify(grid)).not.toMatch(/supplier|margin|tvaConfirmed|modelValidated/i);
  });
});
describe('Scénarios alternatifs et périmètres', () => {
  it('présente trois alternatives de charge sans total ni cause imposée', () => {
    const r = resolveScenarios(grid,'phone','charge');
    expect(r.offers.map(o => o.id)).toEqual(['phone-port-clean','phone-charge-module','phone-charge-soldered']);
    expect(r.possible.map(o => o.id)).toEqual(['phone-board']);
    expect(r).not.toHaveProperty('total');
  });
  it('ne substitue pas un LCD à un OLED et accepte le type inconnu', () => {
    expect(resolveScenarios(grid,'phone','screen','oled').offers.map(o => o.id)).toEqual(['phone-screen-oled']);
    expect(resolveScenarios(grid,'phone','screen','unknown').offers).toHaveLength(3);
    expect(offer('phone-screen-lcd').quoteCases.join(' ')).toContain('OLED');
  });
  it('distingue HDMI PS5 et PS4/Xbox, sans HDMI supposé pour Switch', () => {
    expect(resolveScenarios(grid,'console','image','ps5').offers[0]?.id).toBe('console-hdmi-ps5');
    expect(resolveScenarios(grid,'console','image','switch').offers.every(o => o.estimate.kind === 'diagnostic')).toBe(true);
    expect(resolveScenarios(grid,'console','connector','switch').offers[0]?.id).toBe('console-usbc-switch');
  });
  it('propose un ou deux joysticks, jamais une addition ni Hall/TMR', () => {
    expect(resolveScenarios(grid,'controller','drift','one').offers.map(o => o.id)).toEqual(['controller-drift-one']);
    expect(resolveScenarios(grid,'controller','drift','two').offers.map(o => o.id)).toEqual(['controller-drift-two']);
    expect(resolveScenarios(grid,'controller','drift','unknown').offers).toHaveLength(2);
  });
  it('conserve les prestations communes aux PC sans septième famille', () => {
    for (const family of ['laptop','desktop'] as const) expect(resolveScenarios(grid,family,'slow').offers.map(o => o.id)).toEqual(['computer-software','computer-ssd-clone']);
    expect(resolveScenarios(grid,'desktop','battery').offers).toEqual([]);
  });
  it('oriente le liquide et la panne inconnue vers les diagnostics', () => {
    const r = resolveScenarios(grid,'phone','liquid'); expect(r.diagnosticFirst).toBe(true);
    expect(r.offers.map(o => o.id)).toEqual(['diagnostic-standard','diagnostic-electronique']);
    expect(r.possible[0]?.id).toBe('liquid-treatment');
    expect(resolveScenarios(grid,'tablet','unknown').offers).toHaveLength(2);
    expect(precisionOptions('controller','drift').map(p => p.id)).toContain('unknown');
  });
});
describe('Déduction sans cumul', () => {
  it('déduit 89 € de 219 € et prévoit le remboursement si nécessaire', () => {
    expect(diagnosticSettlement(21900,8900)).toEqual({remaining:13000,refundOrCredit:0});
    expect(diagnosticSettlement(3900,4900)).toEqual({remaining:0,refundOrCredit:1000});
    expect(diagnosticPresentation(grid).supplement).toMatch(/^40\s*€/);
    expect(() => diagnosticSettlement(-1,0)).toThrow();
  });
});
