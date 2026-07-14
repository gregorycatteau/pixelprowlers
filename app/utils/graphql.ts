const DEFAULT_GRAPHQL_API_URL = '/graphql/';
const GRAPHQL_TIMEOUT_MS = 12000;

type GraphqlResponse<T> = {
  data?: T;
  errors?: Array<{ message?: string }>;
};

export class GraphqlRequestError extends Error {
  status?: number;
  statusText?: string;
  kind: 'network' | 'timeout' | 'http' | 'graphql' | 'invalid-response';

  constructor(
    message: string,
    kind: GraphqlRequestError['kind'],
    details: { status?: number; statusText?: string } = {},
  ) {
    super(message);
    this.name = 'GraphqlRequestError';
    this.kind = kind;
    this.status = details.status;
    this.statusText = details.statusText;
  }
}

const normalizeUrl = (value: unknown) => (
  typeof value === 'string'
    ? `${value.trim().replace(/\/+$/, '')}/`
    : ''
);

export const getGraphqlApiUrl = () => {
  const config = useRuntimeConfig();

  return normalizeUrl(config.public.graphqlApiUrl || config.graphqlApiUrl) || DEFAULT_GRAPHQL_API_URL;
};

const isAbortError = (error: unknown) => (
  error instanceof DOMException && error.name === 'AbortError'
);

const parseGraphqlResponse = <T>(text: string, status: number, statusText: string) => {
  if (!text) {
    return {};
  }

  try {
    return JSON.parse(text) as GraphqlResponse<T>;
  } catch (error) {
    throw new GraphqlRequestError("La reponse API n'est pas lisible.", 'invalid-response', {
      status,
      statusText,
    });
  }
};

const graphQlErrorMessages = (errors: GraphqlResponse<unknown>['errors']) => (
  errors
    ?.map((entry) => entry.message?.trim())
    .filter((message): message is string => Boolean(message))
    || []
);

const logGraphqlFailure = (endpoint: string, error: GraphqlRequestError) => {
  console.warn('[graphql] request failed', {
    endpoint,
    kind: error.kind,
    status: error.status,
    statusText: error.statusText,
  });
};

export const graphqlRequest = async <T, V extends Record<string, any> = Record<string, any>>(
  query: string,
  variables?: V,
) => {
  const endpoint = getGraphqlApiUrl();
  const controller = new AbortController();
  const timeoutId = globalThis.setTimeout(() => controller.abort(), GRAPHQL_TIMEOUT_MS);

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        variables: variables || {},
      }),
      credentials: 'same-origin',
      signal: controller.signal,
    });

    const text = await response.text();
    const payload = parseGraphqlResponse<T>(text, response.status, response.statusText);

    if (!response.ok) {
      throw new GraphqlRequestError(
        payload.errors?.length ? graphQlErrorMessages(payload.errors).join(' ') : response.statusText,
        'http',
        { status: response.status, statusText: response.statusText },
      );
    }

    const errors = graphQlErrorMessages(payload.errors);
    if (errors.length) {
      throw new GraphqlRequestError(errors.join(' '), 'graphql', {
        status: response.status,
        statusText: response.statusText,
      });
    }

    if (!payload.data) {
      throw new GraphqlRequestError('Réponse API invalide.', 'invalid-response', {
        status: response.status,
        statusText: response.statusText,
      });
    }

    return payload.data;
  } catch (error) {
    if (error instanceof GraphqlRequestError) {
      logGraphqlFailure(endpoint, error);
      throw error;
    }

    const wrappedError = isAbortError(error)
      ? new GraphqlRequestError('La demande a mis trop de temps à répondre.', 'timeout')
      : new GraphqlRequestError(
        "Le navigateur n'a pas pu joindre l'API GraphQL.",
        'network',
      );
    logGraphqlFailure(endpoint, wrappedError);
    throw wrappedError;
  } finally {
    globalThis.clearTimeout(timeoutId);
  }
};

export const parseGraphqlJson = <T>(value: unknown, fallback: T) => {
  if (typeof value === 'string') {
    try {
      return JSON.parse(value) as T;
    } catch {
      return fallback;
    }
  }

  if (value && typeof value === 'object') {
    return value as T;
  }

  return fallback;
};

export const graphqlErrorMessage = (error: unknown, fallback: string) => {
  if (error instanceof GraphqlRequestError) {
    if (error.kind === 'timeout') {
      return "La demande met trop de temps à répondre. Réessayez dans un instant, vos informations n'ont pas besoin d'être ressaisies.";
    }

    if (error.kind === 'network') {
      return "Le service de création des audits est momentanément indisponible. Vos informations sont conservées dans le formulaire : vous pouvez réessayer dans quelques instants.";
    }

    if (error.kind === 'http') {
      if (error.status === 400) {
        return error.message || 'Certaines informations doivent être corrigées avant de créer le dossier.';
      }

      if (error.status === 403) {
        return "La demande a été refusée par le service d'audit. Rechargez la page puis réessayez.";
      }

      if (error.status === 404) {
        return "Le point d'entrée du service d'audit est introuvable. La configuration locale de l'API doit être vérifiée.";
      }

      if (error.status && error.status >= 500) {
        return "Le service d'audit rencontre un problème temporaire. Réessayez dans quelques instants.";
      }

      return fallback;
    }

    if (error.kind === 'graphql') {
      return error.message || fallback;
    }

    return fallback;
  }

  return fallback;
};

export const CITATION_ALEATOIRE_QUERY = /* GraphQL */ `
  query CitationAleatoire($excludeId: Int) {
    citationAleatoire(excludeId: $excludeId) {
      id
      texte
      auteur
      source
    }
  }
`;

export const CREATE_AUDIT_DOSSIER_MUTATION = /* GraphQL */ `
  mutation CreateAuditDossier(
    $consentementRgpd: Boolean!
    $email: String!
    $nom: String!
    $nomStructure: String
    $prenom: String!
    $telephone: String!
    $typePersonne: String!
  ) {
    createAuditDossier(
      consentementRgpd: $consentementRgpd
      email: $email
      nom: $nom
      nomStructure: $nomStructure
      prenom: $prenom
      telephone: $telephone
      typePersonne: $typePersonne
    ) {
      dossier {
        numeroDossier
        statut
      }
    }
  }
`;

export const SUBMIT_AUDIT_REPONSES_MUTATION = /* GraphQL */ `
  mutation SubmitAuditReponses($numeroDossier: String!, $reponses: JSONString!) {
    submitAuditReponses(numeroDossier: $numeroDossier, reponses: $reponses) {
      numero_dossier: numeroDossier
      statut
      scores_series: scoresSeries
      score_global: scoreGlobal
      pilier_faible: pilierFaible
      notification_status: notificationStatus
    }
  }
`;

export const CREATE_REFONTE_AUDIT_MUTATION = /* GraphQL */ `
  mutation CreateRefonteAudit(
    $consentementRgpd: Boolean!
    $email: String!
    $nom: String!
    $nomStructure: String
    $prenom: String!
    $reponses: JSONString!
    $siteUrl: String!
    $telephone: String!
    $typePersonne: String!
  ) {
    createRefonteAudit(
      consentementRgpd: $consentementRgpd
      email: $email
      nom: $nom
      nomStructure: $nomStructure
      prenom: $prenom
      reponses: $reponses
      siteUrl: $siteUrl
      telephone: $telephone
      typePersonne: $typePersonne
    ) {
      audit {
        reference
        analysis_status: analysisStatus
      }
    }
  }
`;

export const REFONTE_AUDIT_QUERY = /* GraphQL */ `
  query RefonteAudit($reference: String!) {
    refonteAudit(reference: $reference) {
      reference
      site_url: siteUrl
      analysis_status: analysisStatus
      technical_report: technicalReport
      pagespeed_report: pagespeedReport
      heuristic_report: heuristicReport
      analysis_error: analysisError
      date_creation: dateCreation
      date_maj: dateMaj
    }
  }
`;

export const MOTIFS_QUERY = /* GraphQL */ `
  query Motifs {
    motifs {
      id
      nom
      duree_minutes: dureeMinutes
      creneau_type: creneauType
    }
  }
`;

export const RAISONS_APPPEL_QUERY = /* GraphQL */ `
  query RaisonsAppel {
    raisonsAppel {
      id
      nom
    }
  }
`;

export const CALENDRIER_MOIS_QUERY = /* GraphQL */ `
  query CalendrierMois($annee: Int!, $mois: Int!) {
    calendrierMois(annee: $annee, mois: $mois) {
      date
      statut
    }
  }
`;

export const CRENEAUX_DISPONIBLES_QUERY = /* GraphQL */ `
  query CreneauxDisponibles(
    $motifId: Int!
    $dateDebut: Date!
    $dateFin: Date!
    $urgence: Boolean = false
    ) {
    creneauxDisponibles(
      motifId: $motifId
      dateDebut: $dateDebut
      dateFin: $dateFin
      urgence: $urgence
    ) {
      date
      heure_debut: heureDebut
      heure_fin: heureFin
    }
  }
`;

export const CREATE_RDV_RESERVATION_MUTATION = /* GraphQL */ `
  mutation CreateRdvReservation(
    $date: Date!
    $email: String!
    $heureDebut: String!
    $heureFin: String!
    $message: String
    $motifId: Int!
    $nom: String!
    $prenom: String!
    $raisonIds: [Int]!
    $telephone: String!
    $urgence: Boolean = false
  ) {
    createRdvReservation(
      date: $date
      email: $email
      heureDebut: $heureDebut
      heureFin: $heureFin
      message: $message
      motifId: $motifId
      nom: $nom
      prenom: $prenom
      raisonIds: $raisonIds
      telephone: $telephone
      urgence: $urgence
    ) {
      rdv {
        motif {
          id
          nom
          duree_minutes: dureeMinutes
          creneau_type: creneauType
        }
        creneaux {
          date
          heure_debut: heureDebut
          heure_fin: heureFin
        }
      }
    }
  }
`;

export const CREATE_URGENCY_REQUEST_MUTATION = /* GraphQL */ `
  mutation CreateUrgencyRequest(
    $affectedUrl: String!
    $callbackSlot: String!
    $consentToContact: Boolean!
    $contactPreference: String!
    $email: String!
    $expectedNextStep: String!
    $impactLevel: String!
    $name: String!
    $noSecretsConfirmed: Boolean!
    $organization: String!
    $phone: String!
    $problemType: String!
    $shortDescription: String!
    $sinceWhen: String!
    $website: String
  ) {
    createUrgencyRequest(
      affectedUrl: $affectedUrl
      callbackSlot: $callbackSlot
      consentToContact: $consentToContact
      contactPreference: $contactPreference
      email: $email
      expectedNextStep: $expectedNextStep
      impactLevel: $impactLevel
      name: $name
      noSecretsConfirmed: $noSecretsConfirmed
      organization: $organization
      phone: $phone
      problemType: $problemType
      shortDescription: $shortDescription
      sinceWhen: $sinceWhen
      website: $website
    ) {
      reference
      status
      message
      clientEmailStatus
      ticket {
        reference
        status
      }
    }
  }
`;
