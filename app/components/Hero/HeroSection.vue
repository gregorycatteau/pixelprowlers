<template>
  <section
    class="HeroSection"
    aria-labelledby="hero-title"
  >
    <div class="container HeroInner">
      <div class="HeroContent">
        <p
          v-if="eyebrow"
          class="HeroEyebrow"
        >
          {{ eyebrow }}
        </p>

        <h1 id="hero-title">
          <span class="HeroTitlePrimary">
            {{ title }}
          </span>

          <span
            v-if="secondaryTitle"
            class="HeroTitleSecondary"
          >
            {{ secondaryTitle }}
          </span>
        </h1>

        <p class="HeroSubtitle">
          {{ subtitle }}
        </p>

        <div class="HeroActions">
          <NuxtLink
            class="ButtonBase ButtonPrimary"
            :to="ctaLink"
          >
            {{ ctaText }}
          </NuxtLink>

          <NuxtLink
            v-if="secondaryCtaText && secondaryCtaLink"
            class="ButtonBase ButtonSecondary"
            :to="secondaryCtaLink"
          >
            {{ secondaryCtaText }}
          </NuxtLink>
        </div>

        <p
          v-if="ctaNote"
          class="HeroCtaNote"
        >
          {{ ctaNote }}
        </p>

        <ul
          v-if="trustItems.length"
          class="HeroTrustItems"
          aria-label="Principes d’intervention"
        >
          <li
            v-for="item in trustItems"
            :key="item"
          >
            <span
              class="HeroTrustIcon"
              aria-hidden="true"
            >
              ✓
            </span>

            <span>
              {{ item }}
            </span>
          </li>
        </ul>
      </div>

      <aside
        class="HeroFramework"
        aria-labelledby="hero-framework-title"
      >
        <p class="HeroFrameworkEyebrow">
          Cadre de confiance
        </p>

        <h2 id="hero-framework-title">
          Votre activité reste maîtresse de ses choix
        </h2>

        <p class="HeroFrameworkIntroduction">
          L’objectif n’est pas de remplacer une dépendance par une autre,
          mais de vous laisser une situation plus claire, documentée et
          transmissible.
        </p>

        <dl class="HeroFrameworkList">
          <div>
            <dt>Accès</dt>

            <dd>
              Identifiés, limités au besoin et transmis dans un cadre
              préalablement validé.
            </dd>
          </div>

          <div>
            <dt>Décisions</dt>

            <dd>
              Expliquées avant toute modification importante.
            </dd>
          </div>

          <div>
            <dt>Documentation</dt>

            <dd>
              Prévue pour rester utilisable après l’intervention.
            </dd>
          </div>
        </dl>
      </aside>
    </div>
  </section>
</template>

<script setup lang="ts">
interface Props {
  eyebrow?: string;
  title: string;
  secondaryTitle?: string;
  subtitle: string;
  ctaText: string;
  ctaLink: string;
  secondaryCtaText?: string;
  secondaryCtaLink?: string;
  ctaNote?: string;
  trustItems?: string[];
}

withDefaults(
  defineProps<Props>(),
  {
    eyebrow: '',
    secondaryTitle: '',
    secondaryCtaText: '',
    secondaryCtaLink: '',
    ctaNote: '',
    trustItems: () => [],
  },
);
</script>

<style scoped>
@reference "../../assets/css/main.css";

.HeroSection {
  @apply relative overflow-hidden border-b border-pxp-green/15 bg-pxp-panel text-pxp-ink;
}

.HeroInner {
  @apply grid gap-10 py-14 md:py-20 lg:grid-cols-3 lg:items-center;
}

.HeroContent {
  @apply lg:col-span-2;
}

.HeroEyebrow,
.HeroFrameworkEyebrow {
  @apply mb-4 text-xs font-black uppercase tracking-widest text-pxp-green;
}

.HeroContent h1 {
  @apply max-w-5xl leading-tight;
  overflow-wrap: anywhere;
}

.HeroTitlePrimary {
  @apply block text-4xl font-black text-pxp-ink md:text-6xl;
}

.HeroTitleSecondary {
  @apply mt-4 block max-w-4xl text-2xl font-black leading-tight text-pxp-green md:text-4xl;
}

.HeroSubtitle {
  @apply mt-6 max-w-3xl text-lg font-semibold leading-relaxed text-pxp-ink/80 md:text-xl;
}

.HeroActions {
  @apply mt-8 flex flex-col items-start gap-3 sm:flex-row sm:flex-wrap;
}

.HeroCtaNote {
  @apply mt-4 max-w-3xl text-sm font-semibold leading-relaxed text-pxp-ink/70;
}

.HeroTrustItems {
  @apply mt-7 flex flex-col gap-3 p-0 sm:flex-row sm:flex-wrap;
  list-style: none;
}

.HeroTrustItems li {
  @apply inline-flex items-center gap-2 rounded-full border border-pxp-green/20 bg-white px-4 py-2 text-sm font-extrabold text-pxp-ink;
}

.HeroTrustIcon {
  @apply font-black text-pxp-green;
}

.HeroFramework {
  @apply rounded-xl border border-pxp-green/20 bg-pxp-ink p-6 text-white shadow-lg md:p-8;
}

.HeroFrameworkEyebrow {
  @apply text-primary-100;
}

.HeroFramework h2 {
  @apply text-2xl font-black leading-tight text-white;
}

.HeroFrameworkIntroduction {
  @apply mt-4 font-semibold leading-relaxed text-white/75;
}

.HeroFrameworkList {
  @apply mt-6 grid gap-5;
}

.HeroFrameworkList > div {
  @apply border-t border-white/15 pt-4;
}

.HeroFrameworkList dt {
  @apply text-sm font-black uppercase tracking-wide text-primary-100;
}

.HeroFrameworkList dd {
  @apply mt-1 font-semibold leading-relaxed text-white/85;
}

@media (max-width: 639px) {
  .HeroActions .ButtonBase {
    @apply w-full justify-center text-center;
  }
}
</style>