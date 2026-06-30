<template>
  <SeoArticlePage
    eyebrow="WordPress associatif"
    title="Sécuriser un site WordPress associatif sans transformer l’équipe en service informatique."
    intro="Un site WordPress d’association peut être très utile, mais il devient fragile quand les extensions s’empilent, que les accès circulent mal et que personne n’a testé les sauvegardes."
    summary-title="Le vrai sujet n’est pas WordPress. C’est la maintenance."
    summary="WordPress n’est pas automatiquement dangereux. Ce qui expose une association, c’est souvent un mélange de comptes oubliés, plugins non suivis, sauvegardes jamais restaurées et responsabilités floues."
    :symptoms="symptoms"
    :risks="risks"
    :exploitation="exploitation"
    :checklist="checklist"
    :pixel-actions="pixelActions"
    :limits="limits"
    :internal-links="internalLinks"
    :primary-cta="primaryCta"
    final-title="Votre WordPress mérite une vérification calme, pas une refonte réflexe."
    final-text="On regarde les accès, les sauvegardes, les extensions et les points de rupture. Ensuite seulement, on décide quoi corriger, documenter ou remplacer."
    :final-cta="finalCta"
  />
</template>

<script setup lang="ts">
usePixelSeo({
  title: 'Sécuriser un site WordPress associatif | PixelProwlers',
  description: 'Checklist et méthode pour sécuriser un site WordPress associatif : accès, plugins, sauvegardes, formulaires, hébergement et maintenance réaliste.',
  path: '/securiser-site-wordpress-associatif',
  type: 'article',
});

const symptoms = [
  {
    title: 'Plugins installés sans inventaire',
    text: 'Personne ne sait vraiment lesquels sont indispensables, lesquels sont obsolètes et lesquels peuvent être supprimés sans casser le site.',
  },
  {
    title: 'Comptes administrateurs trop nombreux',
    text: 'Anciens bénévoles, prestataires, membres du bureau et comptes partagés restent actifs plus longtemps que nécessaire.',
  },
  {
    title: 'Sauvegardes supposées',
    text: 'La sauvegarde existe peut-être chez l’hébergeur ou dans une extension, mais personne n’a vérifié qu’une restauration fonctionne.',
  },
  {
    title: 'Mises à jour évitées',
    text: 'L’équipe repousse les mises à jour par peur de casser le site. C’est compréhensible, mais ce n’est pas une stratégie durable.',
  },
] as const;

const risks = [
  'Perte d’accès au tableau de bord ou à l’hébergement.',
  'Site cassé après une mise à jour réalisée sans sauvegarde exploitable.',
  'Formulaires utilisés pour du spam ou des tentatives d’injection.',
  'Compte ancien encore administrateur après le départ d’un bénévole.',
  'Dépendance à une seule personne qui connaît les accès et les procédures.',
] as const;

const exploitation = 'Une panne ou une compromission exploite rarement un seul détail spectaculaire. Elle profite plutôt d’un enchaînement banal : mot de passe réutilisé, extension oubliée, compte administrateur dormant, sauvegarde non testée et hébergement mal compris. Un accès partagé dans un tableur n’est pas une stratégie.';

const checklist = [
  'Lister les comptes administrateurs WordPress et supprimer ceux qui ne servent plus.',
  'Vérifier que chaque compte important utilise un mot de passe unique et une MFA quand c’est possible.',
  'Identifier les plugins indispensables, inutiles, abandonnés ou redondants.',
  'Contrôler la version de WordPress, du thème et des extensions.',
  'Vérifier où sont les sauvegardes et tester au moins une restauration.',
  'Documenter l’hébergeur, le nom de domaine, les accès et les responsabilités.',
  'Vérifier les formulaires : validation, anti-spam, destinataires et données envoyées.',
] as const;

const pixelActions = [
  {
    title: 'Audit WordPress ciblé',
    text: 'Revue des accès, extensions, sauvegardes, formulaires et points de maintenance qui exposent réellement l’association.',
  },
  {
    title: 'Plan de correction priorisé',
    text: 'Pas de liste interminable : d’abord ce qui réduit le risque concret, puis ce qui améliore la maintenance.',
  },
  {
    title: 'Documentation et transmission',
    text: 'Comprendre assez pour décider, documenter assez pour ne pas dépendre. Le livrable doit rester utilisable après l’intervention.',
  },
  {
    title: 'Refonte seulement si nécessaire',
    text: 'Réparer quand c’est fiable, remplacer quand c’est nécessaire. Une migration vers un site plus sobre se justifie si elle réduit la fragilité.',
  },
] as const;

const limits = [
  'Un audit ne garantit pas l’absence totale de faille.',
  'Une intervention sans accès administrateur ou hébergement peut être limitée.',
  'Une sauvegarde absente réduit fortement les options en cas de casse.',
  'PixelProwlers ne promet pas de récupération miracle après piratage.',
  'La sécurité durable implique une maintenance et des responsabilités claires.',
] as const;

const internalLinks = [
  { label: 'Audit sécurité de site web', href: '/audit-site-web' },
  { label: 'Site sobre, sécurisé, maintenable', href: '/developpement' },
  { label: 'Sauvegardes : erreurs fréquentes', href: '/sauvegardes-site-web-erreurs-frequentes' },
  { label: 'Décrire ma situation', href: '/contact' },
] as const;

const primaryCta = { label: 'Faire vérifier mon site', href: '/audit-site-web' } as const;
const finalCta = { label: 'Planifier un premier échange', href: '/contact' } as const;
</script>
