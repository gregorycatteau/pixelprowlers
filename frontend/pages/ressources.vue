<template>
  <main class="bg-paper text-ink">
    <section class="page-hero">
      <div class="container-site max-w-4xl">
        <p class="eyebrow">Ressources</p>
        <h1>Comprendre assez pour décider.</h1>
        <p>
          Guides, checklists et retours terrain pour aider les petites structures à reprendre la main
          sur leurs accès, sauvegardes, outils, machines et choix open source.
        </p>
      </div>
    </section>

    <section class="content-section">
      <div class="container-site">
        <div class="resource-grid">
          <NuxtLink v-for="resource in resources" :key="resource.title" :to="resource.href" class="resource-card">
            <p>{{ resource.kicker }}</p>
            <h2>{{ resource.title }}</h2>
            <span>{{ resource.status }}</span>
          </NuxtLink>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
usePixelSeo({
  title: 'Ressources sécurité web et autonomie numérique | PixelProwlers',
  description: 'Guides pratiques PixelProwlers pour sécuriser un site WordPress, vérifier les sauvegardes, cartographier les accès et cadrer la maintenance.',
  path: '/ressources',
});

const resources = [
  {
    kicker: 'Guide WordPress',
    title: 'Sécuriser un site WordPress associatif',
    status: 'Lire le guide',
    href: '/securiser-site-wordpress-associatif',
  },
  {
    kicker: 'Checklist',
    title: 'Sauvegardes site web : erreurs fréquentes',
    status: 'Lire la checklist',
    href: '/sauvegardes-site-web-erreurs-frequentes',
  },
  {
    kicker: 'Fiche pratique',
    title: 'Ne plus dépendre d’une seule personne',
    status: 'Cartographier',
    href: '/ne-plus-dependre-une-seule-personne-site',
  },
  {
    kicker: 'Sécurité concrète',
    title: 'Formulaire de contact exposé au spam et aux injections',
    status: 'Vérifier',
    href: '/formulaire-contact-spam-injections',
  },
  {
    kicker: 'Maintenance',
    title: 'Maintenance site web pour TPE et associations',
    status: 'Cadrer',
    href: '/maintenance-site-web-tpe-associations',
  },
] as const;
</script>

<style scoped>
.page-hero {
  @apply border-b border-forest/15 bg-paper py-16 md:py-24;
}

.eyebrow {
  @apply font-mono text-xs font-bold uppercase tracking-[0.24em] text-trust;
}

.page-hero h1 {
  @apply mt-5 max-w-4xl font-heading text-4xl font-black leading-[1.04] text-ink sm:text-5xl md:text-6xl;
}

.page-hero p:not(.eyebrow) {
  @apply mt-6 max-w-3xl text-lg leading-8 text-muted md:text-xl;
}

.content-section {
  @apply bg-sand py-16 md:py-24;
}

.resource-grid {
  @apply grid gap-5 md:grid-cols-2 xl:grid-cols-3;
}

.resource-card {
  @apply rounded-lg border border-forest/15 bg-paper p-6 shadow-sm outline-none transition hover:-translate-y-1 hover:border-scan hover:shadow-soft focus-visible:ring-2 focus-visible:ring-scan focus-visible:ring-offset-2 focus-visible:ring-offset-sand;
}

.resource-card p {
  @apply font-mono text-xs font-bold uppercase tracking-[0.2em] text-trust;
}

.resource-card h2 {
  @apply mt-4 font-heading text-2xl font-black text-ink;
}

.resource-card span {
  @apply mt-6 inline-flex rounded-lg border border-forest/15 bg-sand px-3 py-2 text-sm font-bold text-forest;
}
</style>
