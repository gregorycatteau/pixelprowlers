<template>
  <footer class="SiteFooter">
    <div class="FooterInner">
      <div class="FooterTop">
        <div class="FooterIdentity">
          <NuxtLink to="/" class="FooterBrand" aria-label="PixelProwlers — accueil">
            <img
              class="FooterLogo"
              src="/logo-nav-transparent.png"
              alt=""
              width="40"
              height="40"
            >
            <span class="FooterName">PixelProwlers</span>
          </NuxtLink>

          <p class="FooterPromise">Réparer au composant et prolonger l’usage du matériel. Vous accompagner aussi par le conseil, le développement et la formation.</p>

          <a class="FooterEmail" href="mailto:contact@pixelprowlers.io">
            contact@pixelprowlers.io
          </a>
        </div>

        <div class="FooterNavigation">
          <nav aria-labelledby="footer-expertise-title">
            <h2 id="footer-expertise-title" class="FooterHeading">
              Nos expertises
            </h2>

            <ul class="FooterLinkList">
              <li v-for="pillar in navPillars" :key="pillar.href">
                <NuxtLink class="FooterLink" :to="pillar.href">
                  {{ pillar.label }}
                </NuxtLink>
              </li>
            </ul>
          </nav>

          <nav aria-labelledby="footer-navigation-title">
            <h2 id="footer-navigation-title" class="FooterHeading">
              Nous joindre
            </h2>

            <ul class="FooterLinkList">
              <li v-for="link in transverseLinks" :key="link.href">
                <NuxtLink class="FooterLink" :to="link.href">
                  {{ link.label }}
                </NuxtLink>
              </li>
            </ul>
          </nav>

          <nav aria-labelledby="footer-trust-title">
            <h2 id="footer-trust-title" class="FooterHeading">
              Confiance
            </h2>

            <ul class="FooterLinkList">
              <li v-for="link in footerLegalLinks" :key="link.href">
                <NuxtLink class="FooterLink" :to="link.href">
                  {{ link.label }}
                </NuxtLink>
              </li>
            </ul>
          </nav>
        </div>
      </div>

      <!--
        Trois engagements, comme la grille l'attend (`sm:grid-cols-3`). Ceux
        affichés jusqu'ici ne parlaient que d'accès numériques : les deux
        premiers nomment désormais ce que l'atelier promet sur du matériel,
        le troisième vaut pour les deux métiers.
      -->
      <div class="FooterCommitments" aria-label="Engagements de PixelProwlers">
        <span>Examen avant devis</span>
        <span>Défauts annoncés, jamais masqués</span>
        <span>Restitution documentée</span>
      </div>

      <div class="FooterBottom">
        <p>
          © {{ currentYear }} PixelProwlers. Tous droits réservés.
        </p>

        <p>
          Site édité par PixelProwlers —
          <NuxtLink class="FooterInlineLink" to="/mentions-legales">
            informations légales
          </NuxtLink>
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import {
  footerLegalLinks,
  navPillars,
  navTransverse,
} from '~/utils/navigation';

/*
 * Le pied de page reprend la même structure que le menu : les quatre
 * expertises d'abord, puis les accès transversaux. Il ne cherche pas à
 * reproduire toute la navigation historique.
 */
const transverseLinks = [
  navTransverse.urgency,
  navTransverse.contact,
  navTransverse.about,
] as const;

const currentYear = new Date().getFullYear();
</script>

<style scoped>
@reference "../assets/css/main.css";

.SiteFooter {
  @apply border-t border-white/10 bg-pxp-ink text-white;
}

.FooterInner {
  @apply mx-auto w-[min(1120px,calc(100%-32px))] py-10;
}

.FooterTop {
  @apply grid gap-10;
}

.FooterIdentity {
  @apply max-w-xl;
}

.FooterBrand {
  @apply inline-flex items-center gap-3 rounded-lg font-black text-white transition focus-visible:outline focus-visible:outline-offset-4 focus-visible:outline-[#9ed7b9];
}

.FooterLogo {
  @apply h-10 w-10 rounded-xl object-contain;
}

.FooterName {
  @apply text-xl tracking-tight;
}

.FooterPromise {
  @apply mt-5 max-w-lg leading-7 text-white/70;
}

.FooterEmail {
  @apply mt-5 inline-flex rounded-md font-bold text-[#9ed7b9] underline decoration-[#9ed7b9]/35 underline-offset-4 transition hover:decoration-[#9ed7b9] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#9ed7b9];
}

.FooterNavigation {
  /* Trois colonnes depuis la fusion des expertises et des accès
   * transversaux : deux de front sur mobile, trois dès que la place existe. */
  @apply grid grid-cols-2 gap-8 sm:grid-cols-3;
}

.FooterHeading {
  @apply text-sm font-black uppercase tracking-[0.14em] text-[#9ed7b9];
}

.FooterLinkList li { @apply m-0 border-0 bg-transparent p-0; }

.FooterLinkList {
  @apply mt-2 space-y-1;
}

/*
 * Cible tactile confortable (min ~44px) : le lien porte sa propre
 * hauteur/marge intérieure plutôt que de dépendre du seul texte.
 */
.FooterLink {
  @apply border-0 bg-transparent shadow-none;
  @apply -mx-2 inline-flex min-h-11 items-center rounded-md px-2 text-sm font-normal text-white/75 transition-colors duration-(--motion-feedback) ease-(--motion-ease-standard) hover:text-white focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#9ed7b9];
}

.FooterCommitments {
  @apply mt-10 grid gap-3 border-y border-white/10 py-6 text-sm font-semibold text-white/70;
}

.FooterCommitments span {
  @apply relative pl-6;
}

.FooterCommitments span::before {
  @apply absolute left-0 top-0 font-black text-[#9ed7b9];
  content: "✓";
}

.FooterBottom {
  @apply mt-6 flex flex-col gap-3 text-sm leading-6 text-white/55;
}

.FooterInlineLink {
  @apply rounded-sm text-white/75 underline decoration-white/25 underline-offset-4 transition hover:text-white hover:decoration-white focus-visible:outline focus-visible:outline-offset-4 focus-visible:outline-[#9ed7b9];
}

@media (min-width: 640px) {
  .FooterCommitments {
    @apply grid-cols-3;
  }
}

@media (min-width: 768px) {
  .FooterInner {
    @apply py-14;
  }

  .FooterTop {
    @apply grid-cols-[minmax(0,1.25fr)_minmax(320px,0.75fr)] gap-16;
  }

  .FooterBottom {
    @apply flex-row items-center justify-between gap-8;
  }
}
</style>
