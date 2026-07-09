export const offers = [
  {
    kicker: 'Audit',
    title: 'On regarde avant que ça casse',
    description:
      "Vous voulez savoir si c'est fragile ? On scrute tout : le site, les sauvegardes, les accès, les formulaires. On vous dit ce qui risque de casser et par quoi commencer.",
    points: [
      "Rapport qu'un humain peut lire (pas du charabia)",
      'Priorités claires : urgent vs important vs peut attendre',
      'Pas de promesse magique, juste la vérité',
      'Vous repartez sachant ce qui tient et ce qui ne tient pas',
    ],
    href: '/audit-site-web',
    cta: 'Faire analyser mon site',
    ctaNote: 'Réponse sous 24h. Sans engagement. Pas d’accès demandé sans validation.',
  },
  {
    kicker: 'Refonte',
    title: 'On reconstruit pour que ça dure',
    description:
      'Votre site est une passoire ? On le remplace par quelque chose de simple, qui tient la route, et que vos gens peuvent vraiment maintenir sans coder.',
    points: [
      'Moins de câbles, moins de dépendances inutiles',
      'Simple à comprendre, simple à modifier',
      'Rapide pour vos visiteurs, léger pour vos machines',
      "Documenté : l'équipe sait comment ça marche",
    ],
    href: '/audit-refonte',
    cta: 'Clarifier mon site',
    ctaNote: 'Cadrage avant devis. Aucune modification sans votre accord.',
  },
  {
    kicker: 'Transmission',
    title: "L'équipe reprend la main",
    description:
      "Tout repose sur une seule personne ? On remet ça à plat : qui a accès à quoi, qui peut intervenir, comment on procède en urgence. Après, l'équipe sait.",
    points: [
      'Inventaire réel : accès, outils et comptes clarifiés',
      'Procédures écrites : "si ça casse, on fait ça"',
      'Formation rapide : vos gens deviennent autonomes',
      'Moins de dépendance à une personne, plus de confiance',
    ],
    href: '/transmission-acces',
    cta: 'Sécuriser mes accès',
    ctaNote: 'Confidentialité stricte. Aucun accès partagé sans cadre clair.',
  },
] as const;

export const credibilityProofs = [
  'Site bloqué → accès récupéré en 24h',
  'WordPress piraté → nettoyé + sécurisé',
  'Refonte mal livrée → reprise complète',
] as const;

export const methodProofs = [
  'Audit structuré : accès, sécurité, sauvegardes, performance',
  'Priorisation claire',
  'Aucune action sans validation',
] as const;

export const trustGuarantees = [
  'Vous ne partagez jamais vos accès sans cadre clair',
  'Confidentialité stricte',
  'Aucune modification sans votre accord',
] as const;

export const postActionSteps = [
  'Analyse',
  'Rapport',
  'Recommandations',
] as const;

export const inactionCosts = [
  'Un site fragile finit souvent par casser au pire moment',
  'Les problèmes d’accès ou de sécurité empirent rarement seuls',
  'Chaque semaine sans correction augmente le risque de blocage ou de perte',
] as const;

export const outcomeProjections = [
  'Vous retrouvez le contrôle de votre site',
  'Vos accès sont sécurisés et centralisés',
  'Vous savez exactement quoi faire, dans le bon ordre',
  'Vous n’êtes plus dépendant d’un prestataire flou',
] as const;

export const problems = [
  {
    title: 'Votre site ne reflète plus votre activité.',
    zone: 'Présence web',
    description: 'Un site clair, utile, maintenable et cohérent avec votre activité réelle.',
  },
  {
    title: 'Vos accès sont dispersés entre plusieurs personnes.',
    zone: 'Accès & comptes',
    description: 'Des droits lisibles, des comptes maîtrisés et moins de dépendances humaines.',
  },
  {
    title: 'Vos documents vivent entre mails, Drive perso et vieux PC.',
    zone: 'Données & outils',
    description: 'Des documents retrouvables, des outils sobres et des sauvegardes vérifiables.',
  },
] as const;

export const steps = [
  {
    number: '01',
    title: 'Écouter',
    description: 'Comprendre vos usages, vos contraintes, votre niveau d’urgence et les personnes impliquées.',
  },
  {
    number: '02',
    title: "Faire l'inventaire",
    description: 'Repérer les sites, comptes, machines, documents, outils et points fragiles.',
  },
  {
    number: '03',
    title: 'Prioriser',
    description: "Traiter d'abord ce qui réduit le plus de risque ou de friction pour l'équipe.",
  },
  {
    number: '04',
    title: 'Transmettre',
    description: "Documenter, expliquer et former pour que vous gardiez la main après l'intervention.",
  },
] as const;

export const goodFits = [
  'Vous êtes une association, TPE, école, indépendant ou collectif avec un vrai besoin de fiabilité.',
  'Vous voulez comprendre ce qui est fait et pourquoi.',
  'Vous préférez réduire les risques concrets avant d’empiler des abonnements.',
  'Vous voulez que l’équipe gagne en autonomie grâce à la documentation et à la transmission.',
] as const;

export const badFits = [
  'Vous voulez juste un site vite fait, sans maintenance ni sauvegarde.',
  'Vous cherchez une promesse magique sans implication interne.',
  'Vous voulez multiplier les outils sans clarifier les usages.',
  'Vous voulez déléguer sans documenter ni transmettre.',
] as const;

export type Landing = {
  kicker: string;
  title: string;
  subtitle: string;
  heroCta: string;
  secondaryCta: string;
  primaryHref: string;
  secondaryHref: string;
  heroCtaNote?: string;
  finalCtaNote?: string;
  finalTitle: string;
  finalText: string;
  finalCta: string;
  sections: Array<{
    id: string;
    title: string;
    intro?: string;
    blocks?: Array<{ title: string; text?: string; items?: string[] }>;
    items?: string[];
    paragraphs?: string[];
    alt?: boolean;
  }>;
};

export const landings: Record<string, Landing> = {
  '/audit-site-web': {
    kicker: 'Audit',
    title: 'Savoir avant que ça casse.',
    subtitle: 'Audit complet de votre site : infra, sécu, accès, sauvegardes. Rapport lisible. Priorités claires. Actions réalistes.',
    heroCta: 'Faire analyser mon site',
    secondaryCta: "Parlons d'abord",
    primaryHref: '#audit-parcours',
    secondaryHref: '/rendez-vous',
    heroCtaNote: 'Réponse sous 24h. Sans engagement. Pas d’accès demandé sans validation.',
    finalTitle: 'Vous voulez savoir ce qui tient vraiment ?',
    finalText: "On vérifie, on classe les risques, puis on vous dit ce qui mérite d'être traité maintenant. Si tout fonctionne parfaitement, ce ne sera probablement pas utile.",
    finalCta: 'Obtenir un diagnostic clair',
    finalCtaNote: 'Analyse, rapport, recommandations. Vous validez avant toute action.',
    sections: [
      {
        id: 'audit-preuves',
        title: 'Des problèmes déjà vus, déjà repris.',
        intro: 'Le doute est normal : on parle de sécurité, d’accès et de continuité. Voilà le type de situations traitées.',
        items: [...credibilityProofs],
      },
      {
        id: 'audit-methode',
        title: 'La méthode avant l’intervention.',
        alt: true,
        blocks: [
          { title: 'Audit structuré', items: ['Accès', 'Sécurité', 'Sauvegardes', 'Performance'] },
          { title: 'Priorisation claire', text: "On distingue ce qui bloque, ce qui expose, et ce qui peut attendre." },
          { title: 'Validation obligatoire', text: 'Aucune action sans validation. Aucun accès demandé sans cadre clair.' },
        ],
      },
      {
        id: 'audit-inaction',
        title: 'Ce que l’attente peut coûter.',
        intro: 'Un audit sert surtout à éviter que le problème soit découvert trop tard.',
        items: [...inactionCosts],
      },
      {
        id: 'audit-regarde',
        title: "Qu'est-ce qu'on regarde ?",
        intro: 'On scrute les zones critiques.',
        blocks: [
          { title: 'Infrastructure & hosting', items: ['SSL/TLS valide et à jour ?', 'HTTPS forcé ?', 'Backups testées ?', 'Firewall configuré ?'] },
          { title: 'Données & sauvegardes', items: ['Stratégie de backup claire ?', 'Restauration testée ?', 'Données sensibles identifiées ?'] },
          { title: 'Accès & équipe', items: ['MFA disponible ?', 'Accès documentés ?', 'Anciens comptes révoqués ?', 'Procédures documentées ?'] },
        ],
      },
      {
        id: 'audit-repart',
        title: "Après l'audit, vous avez :",
        alt: true,
        items: ['Rapport lisible', 'Priorités claires', 'Actions réalistes avec effort et complexité visibles', 'Recommandations précises par zone', ...outcomeProjections],
      },
      {
        id: 'audit-apres',
        title: 'Ce qui se passe après votre demande.',
        intro: "Vous savez à quoi vous attendre avant de cliquer.",
        blocks: [
          { title: 'Analyse', text: 'On lit votre situation et on vérifie les signaux prioritaires.' },
          { title: 'Rapport', text: 'Vous recevez une synthèse claire, sans jargon inutile.' },
          { title: 'Recommandations', text: 'On vous dit quoi corriger, dans quel ordre, et ce qui peut attendre.' },
        ],
      },
      {
        id: 'audit-garanties',
        title: 'Vos accès restent sous contrôle.',
        alt: true,
        intro: 'Ce service est conçu pour des sites en production ou en difficulté. Nous intervenons sur des situations réelles, pas des projets exploratoires.',
        items: [...trustGuarantees],
      },
    ],
  },
  '/refonte-site': {
    kicker: 'Refonte',
    title: 'On reconstruit pour que ça dure.',
    subtitle: "Votre site ralentit l'équipe ? On le remplace par quelque chose de simple, qui tient la route, et que vos gens peuvent vraiment maintenir.",
    heroCta: 'Parlons refonte',
    secondaryCta: 'Premier échange',
    primaryHref: '/audit-refonte',
    secondaryHref: '/rendez-vous',
    finalTitle: 'Avant de refondre, on vérifie que ça vaut le coup.',
    finalText: "Un audit seul peut suffire. Une refonte légère peut suffire. Si PixelProwlers n'est pas la bonne option, on vous le dit.",
    finalCta: 'Parlons refonte',
    sections: [
      {
        id: 'refonte-reconnait',
        title: 'Vous reconnaissez ça ?',
        items: ['Le site ralentit vos visiteurs ou l’équipe qui le gère', 'Personne ne comprend comment ça marche', 'Les mises à jour cassent des choses', 'Chaque petit changement dépend de quelqu’un d’extérieur'],
      },
      {
        id: 'refonte-fait',
        title: 'Notre approche',
        alt: true,
        blocks: [
          { title: 'Découverte', items: ['Audit du site actuel', 'Définition des besoins réels', 'Flux utilisateur'] },
          { title: 'Développement', items: ['Architecture simple', 'Peu de dépendances inutiles', 'Documentation pour l’équipe'] },
          { title: 'Transmission', items: ['Formation de l’équipe', 'Procédures de maintenance', 'Support initial'] },
        ],
      },
    ],
  },
  '/transmission-acces': {
    kicker: 'Transmission',
    title: "L'équipe reprend la main.",
    subtitle: 'Tout repose sur une personne ? On remet ça à plat : accès clair, procédures écrites, formation rapide. Après, vous savez.',
    heroCta: 'Reprendre la main',
    secondaryCta: 'Consultation rapide',
    primaryHref: '/rendez-vous',
    secondaryHref: '/rendez-vous',
    finalTitle: "C'est l'offre la plus ignorée, et la plus utile.",
    finalText: 'Une documentation + deux personnes formées = tranquillité pendant des années. Ne la négligez pas.',
    finalCta: 'Reprendre la main',
    sections: [
      {
        id: 'transmission-signal',
        title: "Vous êtes trop dépendants d'une seule personne.",
        paragraphs: [
          "Le jour où la personne clé n'est pas disponible, tombe malade, change de job ou oublie les mots de passe, tout ralentit.",
        ],
        items: ['Accès dispersés', 'Responsabilités floues', 'Procédure d’urgence absente', 'Documentation fragile'],
      },
      {
        id: 'transmission-fait',
        title: 'Notre approche',
        alt: true,
        blocks: [
          { title: 'Audit des accès', items: ['Inventaire complet', 'Dépendances cachées', 'Points de rupture identifiés'] },
          { title: 'Documentation', items: ['Cartographie des accès', 'Procédures écrites', 'Guide de maintenance simple'] },
          { title: 'Formation', items: ['Formation de 2-3 personnes', 'Accès partagés proprement', 'Autonomie garantie'] },
        ],
      },
    ],
  },
};

export const auditRefonteLanding: Landing = {
  kicker: 'Audit refonte',
  title: 'Avant de reconstruire, on cadre vraiment.',
  subtitle: "Un parcours pour comprendre votre site actuel, vos objectifs, vos contraintes et les signaux techniques qui doivent guider la refonte.",
  heroCta: "Démarrer l'audit refonte",
  secondaryCta: "Parlons d'abord",
  primaryHref: '#audit-refonte-parcours',
  secondaryHref: '/rendez-vous',
  finalTitle: 'Vous repartez avec une base claire.',
  finalText: "Le questionnaire donne le contexte. L'analyse technique donne les premiers signaux. L'échange humain fait le tri.",
  finalCta: "Démarrer l'audit refonte",
  sections: [
    {
      id: 'audit-refonte-cadre',
      title: 'Ce que le parcours vérifie',
      blocks: [
        { title: 'Objectifs', items: ['Pourquoi changer maintenant', 'Décisionnaires impliqués', 'Délai souhaité'] },
        { title: 'Existant', items: ['Ce qui fonctionne déjà', 'Ce qui freine', 'Contenus à conserver'] },
        { title: 'Technique', items: ['Balises essentielles', 'HTTPS', 'Ressources lentes ou en erreur'] },
      ],
    },
    {
      id: 'audit-refonte-resultat',
      title: 'Le résultat attendu',
      alt: true,
      items: ['Une référence de dossier', 'Un statut de traitement visible', 'Un rapport technique initial', 'Une grille Nielsen pour orienter la discussion'],
    },
  ],
};

export const values = [
  {
    title: 'Open source = liberté réelle',
    text: "Si ton code dépend d'un éditeur propriétaire qui peut disparaître demain ou changer les règles, tu n'es pas vraiment propriétaire.",
  },
  {
    title: 'Linux = sobriété efficace',
    text: 'Linux fait le job, sans surcharge inutile. Ça marche sur du vieux matériel comme sur du neuf.',
  },
  {
    title: 'Transmission = autonomie',
    text: "Si tout s'écroule parce qu'une seule personne part, ça n'était pas du travail durable. On documente, on explique, on transmet.",
  },
] as const;

export const aboutGoodFits = [
  "Les associations qui veulent de l'impact réel sans arnaque.",
  "Les écoles qui comprennent que la tech c'est un outil, pas une fin en soi.",
  'Les indépendants qui en ont marre des abonnements inutiles.',
  'Les collectifs qui veulent rester maîtres de leur outil.',
] as const;

export const aboutBadFits = [
  "Vous cherchez du bâclé et du vite, on ne fera pas un bon travail et ce n'est pas notre style.",
  'Vous voulez déléguer complètement sans comprendre, on va vous ennuyer avec nos questions.',
  "Vous croyez qu'une IA va vous sauver, on ne partage pas cette vision.",
] as const;
