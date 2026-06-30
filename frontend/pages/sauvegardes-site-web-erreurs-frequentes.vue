<template>
  <SeoArticlePage
    eyebrow="Sauvegardes site web"
    title="Sauvegardes de site web : les erreurs fréquentes qui transforment une panne en crise."
    intro="Une sauvegarde affichée dans un tableau de bord ne suffit pas. Tant qu’une restauration n’a pas été testée, l’équipe ne sait pas vraiment ce qu’elle peut récupérer."
    summary-title="Un site sans sauvegarde testée n’est pas maintenu."
    summary="La question n’est pas seulement “avons-nous une sauvegarde ?”. Il faut savoir où elle est, ce qu’elle contient, qui peut y accéder et combien de temps il faut pour restaurer."
    :symptoms="symptoms"
    :risks="risks"
    :exploitation="exploitation"
    :checklist="checklist"
    :pixel-actions="pixelActions"
    :limits="limits"
    :internal-links="internalLinks"
    :primary-cta="primaryCta"
    final-title="Vérifiez vos sauvegardes avant que la panne choisisse le calendrier."
    final-text="PixelProwlers peut auditer votre situation, clarifier les responsabilités et mettre en place une procédure de restauration compréhensible."
    :final-cta="finalCta"
  />
</template>

<script setup lang="ts">
usePixelSeo({
  title: 'Sauvegardes site web : erreurs fréquentes | PixelProwlers',
  description: 'Comprendre les erreurs fréquentes de sauvegarde de site web : sauvegardes non testées, accès absents, restauration floue et dépendance à une seule personne.',
  path: '/sauvegardes-site-web-erreurs-frequentes',
  type: 'article',
});

const symptoms = [
  {
    title: 'Personne n’a restauré récemment',
    text: 'La sauvegarde est supposée fonctionner, mais aucun test n’a prouvé que les fichiers, la base de données et la configuration reviennent correctement.',
  },
  {
    title: 'Sauvegarde au même endroit que le site',
    text: 'Quand l’hébergement lâche ou qu’un compte est compromis, la copie peut être touchée en même temps que la production.',
  },
  {
    title: 'Accès inconnus',
    text: 'La personne qui sait où sont les sauvegardes n’est pas toujours disponible, ou les accès sont liés à une adresse email personnelle.',
  },
  {
    title: 'Périmètre flou',
    text: 'On sauvegarde peut-être les fichiers, mais pas la base de données, ou l’inverse. Un site web est rarement un seul dossier.',
  },
] as const;

const risks = [
  'Perte de contenus, formulaires, commandes, adhésions ou historique.',
  'Interruption longue parce que personne ne connaît la procédure.',
  'Restauration impossible faute d’accès à l’hébergement ou au nom de domaine.',
  'Découverte trop tardive que la sauvegarde est vide, ancienne ou corrompue.',
  'Dépenses inutiles en urgence alors qu’une procédure simple aurait suffi.',
] as const;

const exploitation = 'Une erreur humaine ou une panne exploite surtout l’impréparation : mise à jour lancée sans copie exploitable, hébergeur mal compris, sauvegarde stockée au mauvais endroit, procédure absente. Avant d’ajouter des outils, on vérifie ce qui tient encore debout.';

const checklist = [
  'Identifier qui possède les accès au site, à l’hébergement, au nom de domaine et aux sauvegardes.',
  'Vérifier la fréquence des sauvegardes et la durée de conservation.',
  'Confirmer que fichiers et base de données sont sauvegardés ensemble.',
  'Stocker au moins une copie hors de l’hébergement principal.',
  'Tester une restauration sur un environnement adapté, sans casser le site public.',
  'Documenter la procédure en langage compréhensible par l’équipe.',
  'Prévoir qui décide quoi en cas de panne ou compromission.',
] as const;

const pixelActions = [
  {
    title: 'Audit des sauvegardes',
    text: 'Vérification du périmètre, des accès, de la fréquence, du stockage et de la capacité de restauration.',
  },
  {
    title: 'Procédure documentée',
    text: 'Un mode opératoire court, lisible et exploitable quand l’équipe doit agir sans improviser.',
  },
  {
    title: 'Priorisation réaliste',
    text: 'Toutes les petites structures n’ont pas besoin d’une usine à gaz. Elles ont besoin d’une restauration fiable.',
  },
  {
    title: 'Transmission',
    text: 'Le bon outil est celui que votre équipe peut garder en main, y compris le jour où il faut restaurer.',
  },
] as const;

const limits = [
  'Une sauvegarde inexistante ne peut pas être recréée après coup.',
  'Une restauration peut être limitée si les accès hébergeur ou domaine manquent.',
  'Un audit ne garantit pas qu’aucune panne ne surviendra.',
  'Une procédure doit être entretenue quand les outils, personnes ou hébergeurs changent.',
  'PixelProwlers ne promet pas de récupération complète sans copie exploitable.',
] as const;

const internalLinks = [
  { label: 'Audit sécurité de site web', href: '/audit-site-web' },
  { label: 'Sécuriser un WordPress associatif', href: '/securiser-site-wordpress-associatif' },
  { label: 'Maintenance pour TPE et associations', href: '/maintenance-site-web-tpe-associations' },
  { label: 'Contact qualifié', href: '/contact' },
] as const;

const primaryCta = { label: 'Lancer un diagnostic', href: '/audit-site-web' } as const;
const finalCta = { label: 'Faire vérifier mes sauvegardes', href: '/contact' } as const;
</script>
