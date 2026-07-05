import { assertSameOrigin, postToDjango } from '../../utils/djangoApi';

type SubmitAuditResponsesBody = {
  numero_dossier?: string;
  reponses?: Record<string, number>;
};

type SubmitAuditResponsesResponse = {
  numero_dossier: string;
  statut: string;
  scores_series: Record<string, { label: string; score: string | number }>;
  score_global: string | number;
  pilier_faible: string;
  notification_status: Record<string, string>;
};

export default defineEventHandler(async (event) => {
  assertSameOrigin(event);

  const body = await readBody<SubmitAuditResponsesBody>(event);

  return postToDjango<SubmitAuditResponsesResponse>('/audit/soumettre-reponses/', body);
});
