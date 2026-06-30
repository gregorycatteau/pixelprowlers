<template>
  <footer class="site-footer">
    <div class="container-site footer-inner">
      <div>
        <p class="footer-brand">PixelProwlers</p>
        <p class="footer-copy">
          Veille numérique, outils sobres et sécurité concrète pour les petites structures qui veulent rester libres.
        </p>
      </div>

      <nav class="footer-nav" aria-label="Navigation de pied de page">
        <NuxtLink to="/audit-site-web" class="footer-link">Audit site web</NuxtLink>
        <NuxtLink to="/developpement" class="footer-link">Site maintenable</NuxtLink>
        <NuxtLink to="/formations" class="footer-link">Formations</NuxtLink>
        <NuxtLink to="/ressources" class="footer-link">Ressources</NuxtLink>
        <NuxtLink to="/materiel" class="footer-link">Matériel</NuxtLink>
        <NuxtLink to="/contact" class="footer-link">Contact</NuxtLink>
      </nav>
    </div>
  </footer>
</template>

<style scoped>
.site-footer {
  @apply border-t border-forest/15 bg-sand py-10;
}

.footer-inner {
  @apply grid gap-8 md:grid-cols-[1fr_auto] md:items-end;
}

.footer-brand {
  @apply font-heading text-xl font-extrabold text-ink;
}

.footer-copy {
  @apply mt-3 max-w-xl text-sm leading-6 text-muted;
}

.footer-nav {
  @apply flex flex-wrap gap-4 text-sm font-bold;
}

.footer-link {
  @apply rounded-md text-forest outline-none transition hover:text-trust focus-visible:ring-2 focus-visible:ring-scan focus-visible:ring-offset-2 focus-visible:ring-offset-sand;
}
</style>
