<template>
  <SeoArticlePage
    eyebrow="Dépendance technique"
    title="Ne plus dépendre d’une seule personne pour son site web."
    intro="Quand une seule personne connaît les accès, les sauvegardes, l’hébergement et les procédures, le site n’est pas seulement technique : il devient un risque organisationnel."
    summary-title="Un accès partagé dans un tableur n’est pas une stratégie."
    summary="La continuité numérique commence par une cartographie simple : qui possède quoi, qui peut agir, où sont les procédures et ce qui bloque si la personne clé disparaît."
    :symptoms="symptoms"
    :risks="risks"
    :exploitation="exploitation"
    :checklist="checklist"
    :pixel-actions="pixelActions"
    :limits="limits"
    :internal-links="internalLinks"
    :primary-cta="primaryCta"
    final-title="Cartographiez les accès avant le départ de la personne qui sait."
    final-text="On peut remettre à plat les comptes, responsabilités, procédures et sauvegardes sans transformer votre structure en service informatique."
    :final-cta="finalCta"
  />
</template>

<script setup lang="ts">
usePixelSeo({
  title: 'Ne plus dépendre d’une seule personne pour son site | PixelProwlers',
  description: 'Réduire la dépendance à une seule personne pour un site web : accès, hébergement, sauvegardes, documentation, passation et continuité numérique.',
  path: '/ne-plus-dependre-une-seule-personne-site',
  type: 'article',
});

const symptoms = [
  {
    title: 'La personne clé répond à toutes les questions',
    text: 'Nom de domaine, hébergement, WordPress, sauvegardes, prestataire : tout passe par une seule mémoire humaine.',
  },
  {
    title: 'Les accès sont personnels',
    text: 'Comptes créés avec une adresse privée, mots de passe envoyés par message ou droits administrateurs non revus.',
  },
  {
    title: 'Aucune procédure écrite',
    text: 'Changer un texte, restaurer une sauvegarde, renouveler un domaine ou couper un compte demande d’appeler la même personne.',
  },
  {
    title: 'Passation repoussée',
    text: 'Tout le monde sait qu’il faudrait documenter, mais la tâche reste floue et revient toujours “plus tard”.',
  },
] as const;

const risks = [
  'Perte d’accès après départ, conflit, indisponibilité ou changement de bénévole.',
  'Renouvellement de domaine raté parce que l’email de notification part au mauvais endroit.',
  'Blocage complet en cas de panne, faute de procédure ou de droits disponibles.',
  'Difficulté à changer de prestataire ou à faire auditer le site.',
  'Décisions techniques prises sans visibilité sur les conséquences.',
] as const;

const exploitation = 'Une panne ou une erreur humaine exploite les zones grises : compte personnel devenu inaccessible, mot de passe unique, documentation absente, sauvegarde connue d’une seule personne. Ce n’est pas spectaculaire. C’est juste fragile.';

const checklist = [
  'Lister les accès : domaine, DNS, hébergement, CMS, email, sauvegardes, analytics et outils tiers.',
  'Identifier le propriétaire réel de chaque compte et l’adresse email associée.',
  'Supprimer ou réduire les accès des personnes qui ne doivent plus administrer.',
  'Mettre en place un gestionnaire de mots de passe adapté à la structure.',
  'Documenter les procédures minimales : mise à jour, sauvegarde, restauration, renouvellement.',
  'Définir qui décide et qui exécute en cas d’urgence.',
  'Prévoir une passation quand un bénévole, salarié ou prestataire quitte le rôle.',
] as const;

const pixelActions = [
  {
    title: 'Cartographie des accès',
    text: 'Inventaire clair des comptes, droits, propriétaires, risques et dépendances humaines.',
  },
  {
    title: 'Remise à plat progressive',
    text: 'On ne casse pas tout pour faire propre. On sécurise les accès critiques d’abord.',
  },
  {
    title: 'Documentation minimale',
    text: 'Comprendre assez pour décider, documenter assez pour ne pas dépendre.',
  },
  {
    title: 'Transmission à l’équipe',
    text: 'Explications concrètes, procédures courtes et responsabilités compréhensibles.',
  },
] as const;

const limits = [
  'Sans accès initial, certaines récupérations peuvent dépendre des hébergeurs ou prestataires.',
  'Une documentation doit être tenue à jour quand les personnes changent.',
  'PixelProwlers ne contourne pas les contrôles d’accès légitimes.',
  'Une cartographie ne remplace pas une politique interne, elle la rend possible.',
  'La réduction de dépendance demande une implication minimale de la structure.',
] as const;

const internalLinks = [
  { label: 'Audit sécurité de site web', href: '/audit-site-web' },
  { label: 'Site sobre, sécurisé, maintenable', href: '/developpement' },
  { label: 'Maintenance pour TPE et associations', href: '/maintenance-site-web-tpe-associations' },
  { label: 'Ressources pratiques', href: '/ressources' },
] as const;

const primaryCta = { label: 'Cartographier mes accès', href: '/contact' } as const;
const finalCta = { label: 'Cartographier mes accès', href: '/contact' } as const;
</script>
