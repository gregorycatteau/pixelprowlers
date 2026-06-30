<template>
  <SeoArticlePage
    eyebrow="Maintenance web"
    title="Maintenance de site web pour TPE et associations : ce qu’il faut vraiment suivre."
    intro="La maintenance web ne consiste pas à cliquer sur “mettre à jour” quand quelqu’un y pense. Elle doit protéger le site, les accès, les sauvegardes et la capacité de l’équipe à comprendre ce qui se passe."
    summary-title="La maintenance utile est visible, documentée et proportionnée."
    summary="Une petite structure n’a pas besoin d’un comité technique permanent. Elle a besoin de points de contrôle clairs, d’une sauvegarde testée et d’un interlocuteur capable d’expliquer les priorités."
    :symptoms="symptoms"
    :risks="risks"
    :exploitation="exploitation"
    :checklist="checklist"
    :pixel-actions="pixelActions"
    :limits="limits"
    :internal-links="internalLinks"
    :primary-cta="primaryCta"
    final-title="La maintenance doit réduire la fragilité, pas créer une dépendance opaque."
    final-text="On peut cadrer une maintenance sobre : accès, sauvegardes, mises à jour, documentation, surveillance raisonnable et transmission."
    :final-cta="finalCta"
  />
</template>

<script setup lang="ts">
usePixelSeo({
  title: 'Maintenance site web pour TPE et associations | PixelProwlers',
  description: 'Maintenance de site web pour TPE et associations : mises à jour, sauvegardes testées, accès, documentation, sécurité concrète et accompagnement réaliste.',
  path: '/maintenance-site-web-tpe-associations',
  type: 'article',
});

const symptoms = [
  {
    title: 'Personne ne sait qui maintient',
    text: 'Le site existe, le prestataire initial est parti, un bénévole dépanne parfois, mais aucun cadre n’est clair.',
  },
  {
    title: 'Mises à jour irrégulières',
    text: 'Elles sont faites trop vite, trop tard ou jamais, souvent sans sauvegarde testée avant intervention.',
  },
  {
    title: 'Incidents traités au cas par cas',
    text: 'Spam, page cassée, domaine à renouveler, plugin bloqué : chaque problème devient une urgence isolée.',
  },
  {
    title: 'Aucune vision des priorités',
    text: 'On ne distingue plus ce qui est critique, utile, décoratif ou simplement hérité d’une ancienne décision.',
  },
] as const;

const risks = [
  'Site inaccessible ou dégradé au mauvais moment.',
  'Sauvegarde absente ou inutilisable après une erreur de mise à jour.',
  'Accumulation de comptes, plugins et outils non maintenus.',
  'Dépendance à une seule personne ou à un prestataire opaque.',
  'Budget gaspillé dans des corrections urgentes évitables.',
] as const;

const exploitation = 'Une maintenance confuse laisse les petites failles devenir des problèmes visibles : plugin oublié, certificat expiré, sauvegarde jamais restaurée, compte ancien encore actif. Avant d’ajouter des outils, on vérifie ce qui tient encore debout.';

const checklist = [
  'Identifier le CMS, l’hébergement, le domaine, les emails et les outils reliés au site.',
  'Lister les comptes administrateurs et revoir les droits régulièrement.',
  'Vérifier que les sauvegardes sont automatiques, conservées et restaurables.',
  'Définir une routine de mise à jour avec point de retour possible.',
  'Documenter les procédures minimales et les contacts utiles.',
  'Surveiller les formulaires, erreurs visibles et expirations importantes.',
  'Faire le tri entre corrections nécessaires, améliorations utiles et demandes décoratives.',
] as const;

const pixelActions = [
  {
    title: 'Audit de départ',
    text: 'État du site, accès, sauvegardes, hébergement, formulaires, dépendances et risques prioritaires.',
  },
  {
    title: 'Maintenance proportionnée',
    text: 'Un cadre simple, adapté à la taille de la structure, sans abonnement inutile ni jargon de façade.',
  },
  {
    title: 'Documentation',
    text: 'Comprendre assez pour décider, documenter assez pour ne pas dépendre.',
  },
  {
    title: 'Évolution sobre',
    text: 'Le bon outil est celui que votre équipe peut garder en main. Une refonte n’est proposée que si elle sert vraiment.',
  },
] as const;

const limits = [
  'La maintenance ne garantit pas qu’aucune panne ne se produira.',
  'Une intervention peut être limitée si les accès ou sauvegardes manquent.',
  'La sécurité totale n’existe pas ; la réduction des risques, oui.',
  'Une maintenance utile demande un minimum de décisions côté structure.',
  'PixelProwlers ne remplace pas une organisation interne, mais peut la rendre plus claire.',
] as const;

const internalLinks = [
  { label: 'Audit sécurité de site web', href: '/audit-site-web' },
  { label: 'Site sobre, sécurisé, maintenable', href: '/developpement' },
  { label: 'Sauvegardes : erreurs fréquentes', href: '/sauvegardes-site-web-erreurs-frequentes' },
  { label: 'Contact qualifié', href: '/contact' },
] as const;

const primaryCta = { label: 'Planifier un premier échange', href: '/contact' } as const;
const finalCta = { label: 'Planifier un premier échange', href: '/contact' } as const;
</script>
