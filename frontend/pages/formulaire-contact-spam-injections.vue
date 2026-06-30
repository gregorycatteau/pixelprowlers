<template>
  <SeoArticlePage
    eyebrow="Formulaire exposé"
    title="Formulaire de contact exposé au spam et aux injections : quoi vérifier sans paniquer."
    intro="Un formulaire de contact paraît banal. Mal configuré, il peut saturer une boîte mail, exposer des données ou devenir un point faible visible sur un site associatif ou TPE."
    summary-title="Un formulaire n’est pas juste une zone de texte."
    summary="Validation, anti-spam, limitation des abus, traitement côté serveur et données envoyées par email : les détails simples font souvent la différence."
    :symptoms="symptoms"
    :risks="risks"
    :exploitation="exploitation"
    :checklist="checklist"
    :pixel-actions="pixelActions"
    :limits="limits"
    :internal-links="internalLinks"
    :primary-cta="primaryCta"
    final-title="Votre formulaire doit aider les vrais humains, pas ouvrir une porte inutile."
    final-text="On vérifie les validations, le traitement serveur, l’anti-spam, les emails et la collecte de données pour réduire les risques concrets."
    :final-cta="finalCta"
  />
</template>

<script setup lang="ts">
usePixelSeo({
  title: 'Formulaire de contact exposé au spam et aux injections | PixelProwlers',
  description: 'Identifier les risques d’un formulaire de contact exposé : spam, injection, validation absente, données sensibles, emails saturés et corrections réalistes.',
  path: '/formulaire-contact-spam-injections',
  type: 'article',
});

const symptoms = [
  {
    title: 'Spam massif',
    text: 'La boîte de contact reçoit des dizaines ou centaines de messages automatiques, parfois avec pièces jointes ou liens douteux.',
  },
  {
    title: 'Champs trop permissifs',
    text: 'Le formulaire accepte tout, trop longtemps, sans validation claire ni limitation du nombre d’envois.',
  },
  {
    title: 'Messages techniques visibles',
    text: 'Une erreur affiche des détails de serveur, d’API ou de configuration qui ne devraient pas être publics.',
  },
  {
    title: 'Données sensibles demandées',
    text: 'Le formulaire encourage parfois les visiteurs à envoyer trop d’informations alors qu’un premier échange devrait rester sobre.',
  },
] as const;

const risks = [
  'Boîte mail saturée et vrais messages noyés dans le spam.',
  'Tentatives d’injection ou d’abus sur un traitement serveur trop permissif.',
  'Collecte excessive de données personnelles sans nécessité claire.',
  'Perte de confiance si le formulaire paraît cassé ou peu professionnel.',
  'Temps perdu à trier, bloquer et réparer dans l’urgence.',
] as const;

const exploitation = 'Un abus de formulaire profite de validations absentes, de messages d’erreur trop bavards, d’absence de limitation et de traitements automatisés mal cadrés. Il ne faut pas transformer le sujet en film d’attaque : il faut vérifier les contrôles simples et les responsabilités.';

const checklist = [
  'Limiter les champs à ce qui est réellement nécessaire.',
  'Valider les données côté navigateur et côté serveur.',
  'Ajouter une protection anti-spam proportionnée : honeypot, temporisation, limitation ou captcha si nécessaire.',
  'Éviter d’afficher des erreurs techniques détaillées au public.',
  'Ne pas demander de mots de passe, pièces sensibles ou secrets techniques.',
  'Vérifier à qui les messages sont envoyés et comment ils sont conservés.',
  'Documenter le comportement attendu en cas de spam massif.',
] as const;

const pixelActions = [
  {
    title: 'Revue du formulaire',
    text: 'Contrôle de la collecte, validation, anti-spam, traitement serveur et messages d’erreur.',
  },
  {
    title: 'Correction sobre',
    text: 'Pas besoin d’un arsenal lourd si un filtrage propre, une validation stricte et une limite d’envoi suffisent.',
  },
  {
    title: 'Confidentialité',
    text: 'Réduction des données demandées et consignes claires pour ne pas collecter de secrets via le formulaire.',
  },
  {
    title: 'Maintenance',
    text: 'Documentation des réglages pour que l’équipe comprenne quoi surveiller après la correction.',
  },
] as const;

const limits = [
  'Aucun formulaire public ne supprime 100 % du spam.',
  'Une correction peut dépendre du CMS, de l’hébergement ou du prestataire actuel.',
  'PixelProwlers ne collecte pas de secrets techniques via un formulaire public.',
  'Un audit ne remplace pas un test d’intrusion complet.',
  'La protection doit rester proportionnée aux usages réels du site.',
] as const;

const internalLinks = [
  { label: 'Audit sécurité de site web', href: '/audit-site-web' },
  { label: 'Sécuriser un WordPress associatif', href: '/securiser-site-wordpress-associatif' },
  { label: 'Site sobre, sécurisé, maintenable', href: '/developpement' },
  { label: 'Contact qualifié', href: '/contact' },
] as const;

const primaryCta = { label: 'Faire vérifier mon formulaire', href: '/audit-site-web' } as const;
const finalCta = { label: 'Lancer un diagnostic', href: '/contact' } as const;
</script>
