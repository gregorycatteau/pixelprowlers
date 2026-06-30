<template>
  <main class="bg-paper text-ink">
    <section class="page-hero">
      <div class="container-site hero-grid">
        <div>
          <p class="eyebrow">Ressources</p>
          <h1>Comprendre assez pour décider.</h1>
          <p>
            Guides, checklists et retours terrain pour aider les petites structures à reprendre la main
            sur leurs accès, sauvegardes, outils, machines et choix open source.
          </p>
        </div>

        <aside class="diagnostic-card" aria-labelledby="diagnostic-card-title">
          <p class="eyebrow">Diagnostic</p>
          <h2 id="diagnostic-card-title">Votre site est-il une passoire ?</h2>
          <p>
            Un parcours court pour repérer les angles morts sans transmettre de donnée sensible.
          </p>
          <NuxtLink to="/diagnostic-site-passoire">Lancer le diagnostic</NuxtLink>
        </aside>
      </div>
    </section>

    <section class="content-section">
      <div class="container-site">
        <section v-for="group in resourceGroups" :key="group.title" class="resource-group" :aria-labelledby="group.id">
          <div class="group-heading">
            <p class="eyebrow">{{ group.kicker }}</p>
            <h2 :id="group.id">{{ group.title }}</h2>
            <p>{{ group.description }}</p>
          </div>

          <div class="resource-grid">
            <NuxtLink
              v-for="resource in group.items.filter((item) => item.href)"
              :key="resource.title"
              :to="resource.href"
              class="resource-card"
            >
              <p>{{ resource.kicker }}</p>
              <h3>{{ resource.title }}</h3>
              <span :class="statusClass(resource.status)">{{ resource.status }}</span>
            </NuxtLink>

            <article
              v-for="resource in group.items.filter((item) => !item.href)"
              :key="resource.title"
              class="resource-card pending"
            >
              <p>{{ resource.kicker }}</p>
              <h3>{{ resource.title }}</h3>
              <span :class="statusClass(resource.status)">{{ resource.status }}</span>
            </article>
          </div>
        </section>
      </div>
    </section>

    <section class="newsletter-section" aria-labelledby="newsletter-title">
      <div class="container-site newsletter-grid">
        <div>
          <p class="eyebrow light">Lettre sobre</p>
          <h2 id="newsletter-title">Une lettre utile, pas un tunnel marketing.</h2>
          <p>
            Une lettre sobre pour apprendre à reprendre la main sur ses outils numériques :
            sécurité, Linux, sauvegardes, reconditionné, documentation et retours terrain.
          </p>
        </div>

        <div class="newsletter-panel">
          <p>
            La pré-inscription n’est pas encore ouverte. Aucun email n’est collecté ici pour l’instant.
          </p>
          <button type="button" disabled>Inscription bientôt disponible</button>
        </div>
      </div>
    </section>

    <section class="journal-section" aria-labelledby="journal-title">
      <div class="container-site">
        <div class="group-heading">
          <p class="eyebrow">Journal de bord</p>
          <h2 id="journal-title">Terrain, réparations utiles et leçons apprises.</h2>
          <p>
            Une future série courte pour partager des retours anonymisés : erreurs fréquentes,
            choix open source, reconditionné sérieux et maintenance qui tient dans la vraie vie.
          </p>
        </div>

        <div class="journal-grid">
          <article v-for="entry in journalEntries" :key="entry.title" class="journal-card">
            <p>{{ entry.kicker }}</p>
            <h3>{{ entry.title }}</h3>
            <span>{{ entry.status }}</span>
          </article>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
usePixelSeo({
  title: 'Ressources sécurité web et autonomie numérique | PixelProwlers',
  description: 'Guides, checklists et ressources PixelProwlers pour sécuriser un site, vérifier les sauvegardes, découvrir Linux utile et documenter son numérique.',
  path: '/ressources',
});

type ResourceStatus = 'Disponible' | 'En préparation' | 'Bientôt';

type ResourceItem = {
  kicker: string;
  title: string;
  status: ResourceStatus;
  href?: string;
};

type ResourceGroup = {
  id: string;
  kicker: string;
  title: string;
  description: string;
  items: ResourceItem[];
};

const resourceGroups: ResourceGroup[] = [
  {
    id: 'guides-securite-site-web',
    kicker: 'Guides sécurité site web',
    title: 'Sécurité concrète pour sites fragiles.',
    description: 'Les guides longue traîne déjà publiés restent le socle : WordPress, formulaires, maintenance et dépendance humaine.',
    items: [
      { kicker: 'Guide WordPress', title: 'Sécuriser un site WordPress associatif', status: 'Disponible', href: '/securiser-site-wordpress-associatif' },
      { kicker: 'Sécurité concrète', title: 'Formulaire de contact exposé au spam et aux injections', status: 'Disponible', href: '/formulaire-contact-spam-injections' },
      { kicker: 'Maintenance', title: 'Maintenance site web pour TPE et associations', status: 'Disponible', href: '/maintenance-site-web-tpe-associations' },
    ],
  },
  {
    id: 'checklists',
    kicker: 'Checklists',
    title: 'Vérifier sans se perdre.',
    description: 'Des supports courts pour faire le point avant un audit, une passation ou une intervention.',
    items: [
      { kicker: 'Checklist', title: 'Sauvegardes site web : erreurs fréquentes', status: 'Disponible', href: '/sauvegardes-site-web-erreurs-frequentes' },
      { kicker: 'Checklist', title: 'Checklist sauvegardes', status: 'En préparation' },
      { kicker: 'Checklist', title: 'Checklist accès admin', status: 'En préparation' },
    ],
  },
  {
    id: 'linux-open-source',
    kicker: 'Linux et open source',
    title: 'Des outils que l’équipe peut comprendre.',
    description: 'Linux et l’open source comme méthode : réduire les dépendances, documenter les choix et garder la main.',
    items: [
      { kicker: 'Fiche Linux', title: 'Fiche premiers pas Linux', status: 'Bientôt' },
      { kicker: 'Guide sécurité', title: 'Guide mots de passe + MFA', status: 'En préparation' },
      { kicker: 'Comparatif', title: 'Solutions propriétaires vs open source', status: 'Bientôt' },
    ],
  },
  {
    id: 'reconditionne-utile',
    kicker: 'Reconditionné utile',
    title: 'Réparer quand c’est fiable, remplacer quand c’est nécessaire.',
    description: 'Des repères pour éviter l’achat réflexe de matériel neuf quand une réparation ou un reconditionnement sérieux suffit.',
    items: [
      { kicker: 'Fiche pratique', title: 'Choisir un poste reconditionné pour une association', status: 'Bientôt' },
      { kicker: 'Méthode', title: 'Quand réparer, quand remplacer', status: 'En préparation' },
    ],
  },
  {
    id: 'documentation-minimale',
    kicker: 'Documentation minimale',
    title: 'Ne plus dépendre d’une seule mémoire humaine.',
    description: 'Des modèles pour cartographier les accès, outils, procédures et responsabilités.',
    items: [
      { kicker: 'Fiche pratique', title: 'Ne plus dépendre d’une seule personne', status: 'Disponible', href: '/ne-plus-dependre-une-seule-personne-site' },
      { kicker: 'Modèle', title: 'Modèle d’inventaire numérique', status: 'En préparation' },
      { kicker: 'Diagnostic', title: 'Votre site est-il une passoire ?', status: 'Disponible', href: '/diagnostic-site-passoire' },
    ],
  },
];

const journalEntries = [
  { kicker: 'Retour terrain', title: 'Le site qui avait des sauvegardes, mais aucune restauration testée', status: 'Bientôt' },
  { kicker: 'Réparation utile', title: 'Un poste reconditionné qui évite un achat neuf inutile', status: 'En préparation' },
  { kicker: 'Choix open source', title: 'Remplacer un outil opaque par une solution documentée', status: 'Bientôt' },
] as const;

// Retourne la classe visuelle associée au statut d’une ressource.
const statusClass = (status: ResourceStatus) => ({
  'status-available': status === 'Disponible',
  'status-progress': status === 'En préparation',
  'status-soon': status === 'Bientôt',
});
</script>

<style scoped>
.page-hero {
  @apply border-b border-forest/15 bg-paper py-16 md:py-24;
}

.hero-grid {
  @apply grid gap-8 lg:grid-cols-[1fr_0.75fr] lg:items-center;
}

.eyebrow {
  @apply font-mono text-xs font-bold uppercase tracking-[0.24em] text-trust;
}

.eyebrow.light {
  @apply text-scan;
}

.page-hero h1 {
  @apply mt-5 max-w-4xl font-heading text-4xl font-black leading-[1.04] text-ink sm:text-5xl md:text-6xl;
}

.page-hero p:not(.eyebrow) {
  @apply mt-6 max-w-3xl text-lg leading-8 text-muted md:text-xl;
}

.diagnostic-card {
  @apply rounded-lg border border-forest/15 bg-sand p-6 shadow-soft;
}

.diagnostic-card h2 {
  @apply mt-4 font-heading text-3xl font-black text-ink;
}

.diagnostic-card p:not(.eyebrow) {
  @apply mt-4 leading-7 text-muted;
}

.diagnostic-card a {
  @apply mt-6 inline-flex min-h-12 items-center justify-center rounded-lg bg-action px-6 py-3 text-center font-extrabold text-white shadow-orange outline-none transition hover:bg-[#FF9F2D] focus-visible:ring-2 focus-visible:ring-action focus-visible:ring-offset-2 focus-visible:ring-offset-sand;
}

.content-section,
.journal-section {
  @apply bg-sand py-16 md:py-24;
}

.resource-group {
  @apply mt-14 first:mt-0;
}

.group-heading {
  @apply max-w-3xl;
}

.group-heading h2 {
  @apply mt-4 font-heading text-3xl font-black text-ink md:text-4xl;
}

.group-heading p:not(.eyebrow) {
  @apply mt-5 text-lg leading-8 text-muted;
}

.resource-grid,
.journal-grid {
  @apply mt-8 grid gap-5 md:grid-cols-2 xl:grid-cols-3;
}

.resource-card,
.journal-card {
  @apply rounded-lg border border-forest/15 bg-paper p-6 shadow-sm outline-none transition hover:-translate-y-1 hover:border-scan hover:shadow-soft focus-visible:ring-2 focus-visible:ring-scan focus-visible:ring-offset-2 focus-visible:ring-offset-sand;
}

.resource-card.pending {
  @apply hover:translate-y-0 hover:border-forest/15 hover:shadow-sm;
}

.resource-card p,
.journal-card p {
  @apply font-mono text-xs font-bold uppercase tracking-[0.2em] text-trust;
}

.resource-card h3,
.journal-card h3 {
  @apply mt-4 font-heading text-2xl font-black text-ink;
}

.resource-card span,
.journal-card span {
  @apply mt-6 inline-flex rounded-lg border px-3 py-2 text-sm font-bold;
}

.status-available {
  @apply border-forest/15 bg-sand text-forest;
}

.status-progress {
  @apply border-trust/20 bg-trust/10 text-trust;
}

.status-soon {
  @apply border-muted/20 bg-white/70 text-muted;
}

.newsletter-section {
  @apply bg-night py-16 text-white md:py-24;
}

.newsletter-grid {
  @apply grid gap-8 lg:grid-cols-[1fr_0.75fr] lg:items-center;
}

.newsletter-section h2 {
  @apply mt-4 max-w-3xl font-heading text-3xl font-black md:text-5xl;
}

.newsletter-section p:not(.eyebrow) {
  @apply mt-5 max-w-3xl text-lg leading-8 text-white/75;
}

.newsletter-panel {
  @apply rounded-lg border border-scan/20 bg-white/[0.055] p-6 shadow-[0_24px_70px_rgba(0,0,0,0.22)];
}

.newsletter-panel p {
  @apply mt-0 leading-7 text-white/75;
}

.newsletter-panel button {
  @apply mt-6 inline-flex min-h-12 w-full cursor-not-allowed items-center justify-center rounded-lg border border-white/15 bg-white/10 px-5 py-3 text-center font-extrabold text-white/60;
}

@media (prefers-reduced-motion: reduce) {
  .resource-card,
  .journal-card,
  .diagnostic-card a {
    @apply transition-none;
  }
}
</style>
