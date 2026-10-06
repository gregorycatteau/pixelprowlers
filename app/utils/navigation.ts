/**
 * Structure de navigation publique et grammaire des appels à l'action.
 *
 * PixelProwlers présente quatre expertises, mais elles n'ont pas le même
 * rang : l'atelier — réparer du matériel, en vendre du reconditionné —
 * porte l'activité, et le volet numérique la prolonge. L'ordre ci-dessous
 * est cette hiérarchie, pas une simple liste. Ce module en est la seule
 * source de vérité : le header (desktop et mobile) et le pied de page la
 * consomment, plutôt que d'en recopier chacun une variante qui finirait
 * par diverger.
 *
 * Le contexte d'un appel à l'action est déduit du chemin courant, jamais
 * d'un paramètre de requête ni d'une valeur fournie par le visiteur : la
 * destination sort toujours des constantes ci-dessous.
 */

export type NavPillar = {
  label: string;
  href: string;
  /* Lue à haute voix dans le menu mobile, où les libellés se suivent. Elle
   * tranche surtout entre le matériel du visiteur et le nôtre : « Réparation »
   * et « Matériel reconditionné » désignent deux gestes opposés. */
  description: string;
};

/*
 * L'ordre est la hiérarchie du métier, pas un classement esthétique :
 * l'atelier d'abord, le numérique ensuite. Le libellé du premier pilier ne
 * dit plus « reconditionnement » — partager cette racine avec le pilier
 * suivant obligeait la description à porter seule la distinction.
 */
export const navPillars: readonly NavPillar[] = [
  {
    label: 'Réparation',
    href: '/reparation-informatique',
    description: 'Ordinateur ou téléphone en panne',
  },
  {
    label: 'Matériel reconditionné',
    href: '/materiel-reconditionne',
    description: 'Réemploi et demandes de disponibilité',
  },
  {
    label: 'Services numériques',
    href: '/services-numeriques',
    description: 'Conseil, cybersécurité, développement',
  },
  {
    label: 'Formations',
    href: '/formations',
    description: 'Comprendre et être autonome',
  },
] as const;

/* Pages transversales : elles n'ont pas rang d'expertise. */
export const navTransverse = {
  about: { label: 'À propos', href: '/a-propos' },
  contact: { label: 'Contact', href: '/contact' },
  urgency: { label: 'Urgence web', href: '/urgence' },
  urgencyLong: { label: 'Urgence web', href: '/urgence' },
} as const;

export const footerLegalLinks = [
  { label: 'Mentions légales', href: '/mentions-legales' },
  { label: 'Confidentialité', href: '/confidentialite' },
] as const;

export type ContextualCta = {
  label: string;
  href: string;
};

const CTA_CONTACT: ContextualCta = { label: 'Contact', href: '/contact' };

const CTA_DIGITAL_SERVICES: ContextualCta = {
  label: 'Faire le bilan numérique',
  href: '/diagnostic-situation',
};

const CTA_DESCRIBE_FAILURE: ContextualCta = {
  label: 'Estimer ma réparation',
  href: '/reparation-informatique#parcours-reparation',
};

const CTA_SEE_MACHINES: ContextualCta = {
  label: 'Demander les disponibilités',
  href: '/materiel-reconditionne',
};

/*
 * Chemins du pilier « Services numériques ». Les pages spécialisées gardent
 * leurs URL historiques : elles sont rattachées au pilier ici, pas déplacées.
 */
const DIGITAL_SERVICES_PATHS = [
  '/services-numeriques',
  '/audit-site-web',
  '/audit-refonte',
  '/refonte-site',
  '/transmission-acces',
  '/diagnostic-situation',
  '/diagnostic-result',
] as const;

const normalizePath = (path: string): string => {
  const [withoutQuery = ''] = (path || '/').split('?');
  const [clean = ''] = withoutQuery.split('#');

  if (clean.length > 1 && clean.endsWith('/')) {
    return clean.slice(0, -1);
  }

  return clean || '/';
};

const isWithin = (path: string, base: string): boolean => (
  path === base || path.startsWith(`${base}/`)
);

/**
 * Appel à l'action du header pour un chemin donné.
 *
 * Le CTA réparation rejoint le parcours, y compris par son ancre sur la page
 * déjà affichée. Le catalogue utilise une demande de disponibilités. Sur la
 * page de contact elle-même, plus rien d'utile ne reste à proposer :
 * la fonction retourne `null` et le header n'affiche alors aucun bouton,
 * plutôt qu'un lien vers la page courante.
 *
 * Hors des piliers, le repli est « Décrire ma panne » et non un contact
 * générique : c'est la demande majoritaire, et une page transversale —
 * accueil, à propos, mentions légales — ne dit rien qui justifie de
 * proposer autre chose. Le contact générique reste le repli des pages du
 * volet numérique, où la panne matérielle serait hors sujet.
 */
export const contextualCtaFor = (rawPath: string): ContextualCta | null => {
  const path = normalizePath(rawPath);

  if (isWithin(path, '/contact')) {
    return null;
  }

  if (isWithin(path, '/reparation-informatique')) {
    return CTA_DESCRIBE_FAILURE;
  }

  if (isWithin(path, '/materiel-reconditionne')) {
    /*
     * Le catalogue n'est pas encore consommé : sur la page pilier elle-même,
     * renvoyer vers cette même page n'apporterait rien.
     */
    if (path === CTA_SEE_MACHINES.href) {
      return { label: 'Demander les disponibilités', href: '/contact?besoin=reemploi' };
    }

    return CTA_SEE_MACHINES;
  }

  if (isWithin(path, '/urgence')) {
    return { label: 'Signaler un incident', href: '/urgence#urgence-formulaire' };
  }

  if (isWithin(path, '/formations')) {
    /*
     * `formation` présélectionne le besoin public ; le formulaire le traduit
     * vers le service historique formation et la demande transmission.
     */
    return {
      label: 'Nous contacter pour une formation',
      href: '/contact?besoin=formation',
    };
  }

  if (DIGITAL_SERVICES_PATHS.some((base) => isWithin(path, base))) {
    if (path === CTA_DIGITAL_SERVICES.href) {
      return CTA_CONTACT;
    }

    return CTA_DIGITAL_SERVICES;
  }

  return CTA_DESCRIBE_FAILURE;
};

/**
 * Pilier auquel appartient un chemin, ou `null` pour une page transversale.
 * Sert à marquer l'entrée active de la navigation, y compris depuis une page
 * spécialisée qui ne porte pas l'URL du pilier.
 */
export const activePillarHrefFor = (rawPath: string): string | null => {
  const path = normalizePath(rawPath);

  if (isWithin(path, '/reparation-informatique')) {
    return '/reparation-informatique';
  }

  if (isWithin(path, '/materiel-reconditionne')) {
    return '/materiel-reconditionne';
  }

  if (isWithin(path, '/formations')) {
    return '/formations';
  }

  if (DIGITAL_SERVICES_PATHS.some((base) => isWithin(path, base))) {
    return '/services-numeriques';
  }

  return null;
};
