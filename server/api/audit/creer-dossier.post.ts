import { assertSameOrigin, postToDjango } from '../../utils/djangoApi';

type CreateAuditDossierBody = {
  prenom?: string;
  nom?: string;
  email?: string;
  telephone?: string;
  type_personne?: 'individu' | 'association' | 'entreprise';
  nom_structure?: string;
  consentement_rgpd?: boolean;
};

type CreateAuditDossierResponse = {
  numero_dossier: string;
  statut: string;
};

export default defineEventHandler(async (event) => {
  assertSameOrigin(event);

  const body = await readBody<CreateAuditDossierBody>(event);

  return postToDjango<CreateAuditDossierResponse>('/audit/creer-dossier/', body);
});
