<template>
  <section id="accompagnements" class="risk-section" aria-labelledby="risk-title">
    <div class="container-site">
      <div class="section-heading">
        <p class="eyebrow">Cartographie utile</p>
        <h2 id="risk-title">Ce qu’on sécurise</h2>
        <p>
          PixelProwlers ne vend pas une pile d’outils. On regarde les zones qui portent vraiment votre activité et les points de rupture possibles.
        </p>
      </div>

      <div class="zone-grid">
        <article v-for="zone in zones" :key="zone.title" class="zone-card">
          <p class="zone-index">{{ zone.index }}</p>
          <h3>{{ zone.title }}</h3>
          <p>{{ zone.description }}</p>
        </article>
      </div>

      <div class="security-panel" aria-labelledby="security-title">
        <div class="security-copy">
          <p class="eyebrow light">Angles morts</p>
          <h2 id="security-title">On pense comme l’attaquant, mais on agit comme un accompagnant.</h2>
          <p>
            Le but n’est pas de faire peur. Le but est de rendre visibles les failles simples, fréquentes et corrigeables.
          </p>
        </div>

        <div class="blind-grid" aria-label="Angles morts fréquents">
          <button
            v-for="(risk, index) in blindSpots"
            :key="risk.title"
            type="button"
            class="flip-card"
            :class="[
              `attention-${index + 1}`,
              { 'is-active': activeRisk === risk.title },
            ]"
            :aria-pressed="isRiskActive(risk.title)"
            :aria-label="riskAriaLabel(risk)"
            @click="toggleRisk(risk.title)"
          >
            <span class="flip-inner">
              <span class="card-face card-front">
                <span class="risk-marker" aria-hidden="true">{{ index + 1 }}</span>
                <span class="risk-title">{{ risk.title }}</span>
                <span class="risk-intro">{{ risk.intro }}</span>
                <span class="risk-hint">Survolez ou ouvrez pour voir le cas réel</span>
              </span>

              <span class="card-face card-back">
                <span class="risk-label">{{ risk.label }}</span>
                <span class="risk-story">{{ risk.story }}</span>
                <span class="risk-action">{{ risk.action }}</span>
              </span>
            </span>
          </button>
        </div>
      </div>

      <div class="risk-cta">
        <p>Vous reconnaissez deux ou trois angles morts ? Il est temps de vérifier avant que l’urgence décide pour vous.</p>
        <NuxtLink to="/audit-site-web">Faire vérifier mon site</NuxtLink>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';

type BlindSpot = {
  title: string;
  intro: string;
  label: string;
  story: string;
  action: string;
};

const zones = [
  {
    index: '01',
    title: 'Présence web',
    description: 'Un site clair, utile, maintenable et cohérent avec votre activité réelle.',
  },
  {
    index: '02',
    title: 'Accès & comptes',
    description: 'Des droits lisibles, des comptes maîtrisés et moins de dépendances humaines.',
  },
  {
    index: '03',
    title: 'Données & outils',
    description: 'Des documents retrouvables, des outils sobres et des sauvegardes vérifiables.',
  },
  {
    index: '04',
    title: 'Matériel',
    description: 'Des postes reconditionnés, fiabilisés et adaptés à vos usages réels.',
  },
  {
    index: '05',
    title: 'Équipe',
    description: 'Des réflexes partagés pour éviter que la sécurité repose sur une seule personne.',
  },
] as const;

const activeRisk = ref<string | null>(null);

const blindSpots: BlindSpot[] = [
  {
    title: 'Mots de passe réutilisés',
    intro: 'Un accès compromis peut ouvrir plusieurs portes.',
    label: 'Vu en audit',
    story: 'Une petite structure utilisait le même mot de passe pour l’email, l’hébergement et l’outil de facturation. Quand une boîte mail a été compromise, tout le reste a suivi.',
    action: 'À vérifier : mots de passe uniques + MFA.',
  },
  {
    title: 'Droits mal attribués',
    intro: 'Un compte oublié peut devenir une porte d’entrée durable.',
    label: 'Signal faible',
    story: 'Un ancien bénévole avait encore un accès administrateur plusieurs mois après son départ. Personne n’avait pensé à faire le ménage des comptes.',
    action: 'À vérifier : revue régulière des accès.',
  },
  {
    title: 'Sauvegardes absentes',
    intro: 'Sans sauvegarde testée, une panne devient une crise.',
    label: 'Cas réel',
    story: 'Le site était “presque sauvegardé”… jusqu’au jour où une mise à jour a cassé la production. La seule copie exploitable datait de plusieurs mois.',
    action: 'À vérifier : sauvegarde automatique + restauration testée.',
  },
  {
    title: 'Formulaires exposés',
    intro: 'Un simple formulaire peut devenir une zone d’attaque.',
    label: 'Vu en audit',
    story: 'Un formulaire de contact acceptait tout sans vraie validation. Résultat : spam massif, tentative d’injection et boîte mail saturée.',
    action: 'À vérifier : validation, rate limit, honeypot et filtrage serveur.',
  },
  {
    title: 'Outils non maintenus',
    intro: 'Un outil oublié reste visible pour un attaquant.',
    label: 'À surveiller',
    story: 'Un plugin oublié depuis deux ans continuait de tourner en silence. C’est souvent ce genre de détail que l’attaquant voit avant l’équipe.',
    action: 'À vérifier : inventaire, mises à jour et suppression du superflu.',
  },
  {
    title: 'Dépendance à une seule personne',
    intro: 'Quand tout repose sur une personne, l’organisation devient fragile.',
    label: 'Point critique',
    story: 'Une seule personne connaissait les accès, les sauvegardes et les procédures. Le jour où elle n’était pas disponible, plus personne ne savait intervenir.',
    action: 'À vérifier : documentation, accès partagés proprement et procédure d’urgence.',
  },
];

// Ouvre ou referme une carte et garantit qu’une seule carte reste active après un tap.
const toggleRisk = (title: string) => {
  activeRisk.value = activeRisk.value === title ? null : title;
};

// Indique si la carte courante est active pour synchroniser l’état visuel et ARIA.
const isRiskActive = (title: string) => activeRisk.value === title;

// Produit un libellé accessible complet pour ne pas dépendre du rendu visuel recto-verso.
const riskAriaLabel = (risk: BlindSpot) => (
  `${risk.title}. ${risk.intro} ${risk.label}. ${risk.story} ${risk.action}`
);
</script>

<style scoped>
.risk-section {
  @apply bg-paper py-16 md:py-24;
}

.section-heading {
  @apply max-w-3xl;
}

.eyebrow {
  @apply font-mono text-xs font-bold uppercase tracking-[0.24em] text-trust;
}

.eyebrow.light {
  @apply text-scan;
}

.section-heading h2 {
  @apply mt-4 font-heading text-3xl font-black text-ink md:text-5xl;
}

.section-heading p {
  @apply mt-5 text-lg leading-8 text-muted;
}

.zone-grid {
  @apply mt-10 grid gap-4 md:grid-cols-2 xl:grid-cols-5;
}

.zone-card {
  @apply rounded-lg border border-forest/15 bg-white/55 p-5 shadow-sm transition hover:-translate-y-1 hover:border-trust hover:shadow-soft;
}

.zone-index {
  @apply font-mono text-sm font-bold text-trust;
}

.zone-card h3 {
  @apply mt-4 font-heading text-xl font-extrabold text-ink;
}

.zone-card p:last-child {
  @apply mt-3 text-sm leading-6 text-muted;
}

.security-panel {
  @apply mt-12 rounded-lg bg-night p-6 text-white shadow-soft md:p-10;
}

.security-copy {
  @apply max-w-3xl;
}

.security-panel h2 {
  @apply mt-4 font-heading text-3xl font-black md:text-4xl;
}

.security-panel p {
  @apply mt-5 leading-7 text-white/75;
}

.blind-grid {
  @apply mt-10 grid gap-4 md:grid-cols-2 xl:grid-cols-3;
  perspective: 1200px;
}

.flip-card {
  @apply relative min-h-[20rem] rounded-lg text-left outline-none;
  perspective: 1200px;
}

.flip-inner {
  @apply relative block h-full min-h-[20rem] rounded-lg transition duration-500 ease-out;
  transform-style: preserve-3d;
}

.flip-card:hover .flip-inner,
.flip-card:focus-visible .flip-inner,
.flip-card.is-active .flip-inner {
  transform: rotateY(180deg);
}

.flip-card:focus-visible {
  @apply ring-2 ring-scan ring-offset-2 ring-offset-night;
}

.card-face {
  @apply absolute inset-0 flex flex-col rounded-lg border border-scan/20 bg-white/[0.055] p-5 shadow-[0_18px_42px_rgba(0,0,0,0.18)] backdrop-blur;
  backface-visibility: hidden;
}

.card-front {
  @apply justify-between;
  animation: attention-glow 10.8s ease-in-out infinite;
}

.card-back {
  @apply justify-between border-trust/45 bg-[#0b1d2b];
  transform: rotateY(180deg);
}

.risk-marker {
  @apply flex h-10 w-10 items-center justify-center rounded-full bg-scan/10 font-mono text-sm font-bold text-scan ring-1 ring-scan/20;
}

.risk-title {
  @apply mt-5 block font-heading text-2xl font-extrabold leading-tight text-white;
}

.risk-intro {
  @apply mt-3 block text-sm leading-6 text-white/75;
}

.risk-hint {
  @apply mt-5 block border-t border-white/10 pt-4 text-xs font-bold uppercase tracking-[0.16em] text-scan/80;
}

.risk-label {
  @apply inline-flex w-fit rounded-full border border-scan/25 bg-scan/10 px-3 py-1 font-mono text-[0.68rem] font-bold uppercase tracking-[0.16em] text-scan;
}

.risk-story {
  @apply mt-5 block text-sm leading-6 text-white/80;
}

.risk-action {
  @apply mt-5 block rounded-lg border border-white/10 bg-white/[0.065] px-4 py-3 text-sm font-extrabold leading-6 text-white;
}

.risk-cta {
  @apply mt-8 grid gap-4 rounded-lg border border-forest/15 bg-sand p-6 shadow-sm md:grid-cols-[1fr_auto] md:items-center;
}

.risk-cta p {
  @apply leading-7 text-muted;
}

.risk-cta a {
  @apply inline-flex min-h-12 items-center justify-center rounded-lg bg-action px-6 py-3 text-center font-extrabold text-white shadow-orange outline-none transition hover:bg-[#FF9F2D] focus-visible:ring-2 focus-visible:ring-action focus-visible:ring-offset-2 focus-visible:ring-offset-paper;
}

.attention-1 .card-front {
  animation-delay: 0s;
}

.attention-2 .card-front {
  animation-delay: 1.8s;
}

.attention-3 .card-front {
  animation-delay: 3.6s;
}

.attention-4 .card-front {
  animation-delay: 5.4s;
}

.attention-5 .card-front {
  animation-delay: 7.2s;
}

.attention-6 .card-front {
  animation-delay: 9s;
}

@keyframes attention-glow {
  0%,
  72%,
  100% {
    border-color: rgba(0, 194, 209, 0.20);
    box-shadow: 0 18px 42px rgba(0, 0, 0, 0.18);
    transform: translateY(0);
  }

  8%,
  18% {
    border-color: rgba(0, 194, 209, 0.58);
    box-shadow: 0 22px 48px rgba(0, 194, 209, 0.12);
    transform: translateY(-2px);
  }
}

@media (prefers-reduced-motion: reduce) {
  .flip-inner {
    @apply duration-0;
  }

  .card-front {
    animation: none;
  }

  .flip-card:hover .flip-inner,
  .flip-card:focus-visible .flip-inner,
  .flip-card.is-active .flip-inner {
    transform: rotateY(180deg);
  }
}
</style>
