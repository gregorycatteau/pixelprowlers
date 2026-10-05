<template>
  <main class="pillar-page">
    <section class="pillar-hero" aria-labelledby="services-title">
      <div class="form-container pillar-hero-content">
        <p class="eyebrow">Services numériques</p>

        <h1 id="services-title">
          Conseil, assistance et cybersécurité, puis développement
        </h1>

        <p class="pillar-introduction">
          Choisir vos outils, être accompagné dans leur usage, sécuriser
          vos accès et vos données, puis créer ou faire évoluer un site,
          une application ou un outil métier. Nous commençons par définir
          votre besoin et le cadre de l’intervention.
        </p>

        <div class="pillar-actions">
          <AppButton href="/diagnostic-situation">
            Faire le bilan numérique
          </AppButton>

          <AppButton variant="secondary" href="/contact?besoin=conseil">
            Nous décrire la situation
          </AppButton>
        </div>

        <p class="cta-note">
          Le bilan numérique pose quelques questions sur votre site et vos
          accès. Il donne un point de départ, pas un devis.
        </p>
      </div>
    </section>

    <section id="conseil-cybersecurite" class="pillar-section" aria-labelledby="services-routes-title">
      <div class="article-container">
        <h2 id="services-routes-title">Conseil, assistance et cybersécurité</h2>

        <p class="pillar-section-intro">
          Le conseil aide à choisir et à prioriser. L’assistance vous
          accompagne face à une difficulté concrète. La cybersécurité
          examine les risques sur les systèmes pour lesquels vous êtes
          autorisé à demander une intervention.
        </p>

        <div v-reveal class="pillar-card-grid">
          <article v-for="route in routes" :key="route.href" class="pillar-card">
            <h3>{{ route.title }}</h3>

            <p>{{ route.description }}</p>

            <NuxtLink class="pillar-card-link" :to="route.href">
              {{ route.linkLabel }}
              <span aria-hidden="true">&nbsp;→</span>
            </NuxtLink>
          </article>
        </div>

        <p class="pillar-boundary">
          Toute vérification de cybersécurité nécessite votre autorisation
          et un périmètre défini ensemble : systèmes concernés, accès
          nécessaires et actions permises. Aucun test sur un système tiers
          n’est engagé sans autorisation de son responsable.
        </p>
      </div>
    </section>

    <section id="developpement" class="pillar-section pillar-section-alt" aria-labelledby="development-title">
      <div class="article-container">
        <h2 id="development-title">Développement de sites, applications et outils métier</h2>

        <p class="pillar-section-intro">
          Un site pour présenter votre activité, une application pour un
          usage précis, ou un outil métier pour simplifier un travail
          répétitif : le besoin guide le choix technique. Le périmètre,
          la faisabilité, la maîtrise des données et la maintenance sont
          discutés avant tout engagement.
        </p>

        <div v-reveal class="pillar-card-grid">
          <article v-for="route in developmentRoutes" :key="route.href" class="pillar-card">
            <h3>{{ route.title }}</h3>
            <p>{{ route.description }}</p>
            <NuxtLink class="pillar-card-link" :to="route.href">
              {{ route.linkLabel }}
              <span aria-hidden="true">&nbsp;→</span>
            </NuxtLink>
          </article>
        </div>
      </div>
    </section>

    <section class="pillar-section pillar-section-alt" aria-labelledby="services-method-title">
      <div class="article-container">
        <h2 id="services-method-title">Ce que vous pouvez attendre</h2>

        <ul v-reveal class="pillar-principles">
          <li v-for="principle in principles" :key="principle">
            {{ principle }}
          </li>
        </ul>

        <p class="pillar-boundary">
          Aucun accès ne vous est demandé avant qu’un périmètre écrit ne soit
          accepté, et aucune modification n’est réalisée sans votre
          validation.
        </p>
      </div>
    </section>

    <section class="pillar-final" aria-labelledby="services-final-title">
      <div class="article-container">
        <h2 id="services-final-title">Vous ne savez pas par où prendre le sujet ?</h2>

        <p>
          Décrivez votre situation en quelques mots. Nous vous répondons en
          vous indiquant l’entrée la plus adaptée, même si ce n’est pas la
          nôtre.
        </p>

        <div class="pillar-actions">
          <AppButton href="/diagnostic-situation">
            Faire le bilan numérique
          </AppButton>

          <AppButton variant="secondary" href="/contact?besoin=conseil">
            Nous décrire la situation
          </AppButton>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';

const runtimeConfig = useRuntimeConfig();

/*
 * Page carrefour : elle oriente vers les pages spécialisées, qui gardent
 * leurs URL et leur contenu commercial. Elle ne les recopie pas, pour ne pas
 * se mettre en concurrence avec elles.
 */
const routes = [
  {
    title: 'Conseil : choisir et prioriser',
    description:
      'Faire le point sur vos outils, vos usages et vos difficultés pour décider par où commencer.',
    href: '/diagnostic-situation',
    linkLabel: 'Faire le bilan numérique',
  },
  {
    title: 'Assistance : avancer face à une difficulté',
    description:
      'Décrire un problème d’usage ou de configuration pour examiner l’accompagnement adapté à votre situation.',
    href: '/contact?besoin=conseil',
    linkLabel: 'Décrire mon besoin d’assistance',
  },
  {
    title: 'Cybersécurité : examiner un site',
    description:
      'Pour savoir ce qui est fragile avant que cela ne casse : infrastructure, sauvegardes, accès, formulaires.',
    href: '/audit-site-web',
    linkLabel: 'Faire auditer un site',
  },
  {
    title: 'Transmission des accès',
    description:
      'Pour savoir qui possède quoi, qui peut intervenir, et comment continuer sans dépendre d’une seule personne.',
    href: '/transmission-acces',
    linkLabel: 'Clarifier mes accès',
  },
  {
    title: 'Urgence web',
    description:
      'Site inaccessible, accès perdu, modification suspecte : le parcours d’urgence est distinct et prioritaire.',
    href: '/urgence',
    linkLabel: 'Signaler un incident',
  },
];

const developmentRoutes = [
  {
    title: 'Sites web : créer ou faire évoluer',
    description:
      'Créer un site ou reprendre un existant avec une structure compréhensible et une maintenance prévue dès le départ.',
    href: '/refonte-site',
    linkLabel: 'Parler de mon site',
  },
  {
    title: 'Applications et outils métier',
    description:
      'Définir un outil autour de vos usages : traitement de données, suivi d’activité ou automatisation de tâches. La faisabilité se vérifie avec vous.',
    href: '/contact?besoin=developpement',
    linkLabel: 'Décrire mon projet d’application',
  },
];

const principles = [
  'Un état des lieux lisible, sans jargon inutile.',
  'Des priorités classées par impact réel, pas par facilité.',
  'Des accès limités au strict nécessaire, et documentés.',
  'Une documentation qui reste utilisable après notre départ.',
  'La réversibilité privilégiée : vous devez pouvoir changer de prestataire.',
];

const siteUrl = String(
  runtimeConfig.public.siteUrl || 'https://pixelprowlers.io',
).replace(/\/+$/, '');

const canonicalUrl = `${siteUrl}/services-numeriques`;

const title = 'Conseil, cybersécurité et développement web et logiciel | PixelProwlers';

const description = [
  'Conseil, assistance et cybersécurité dans un cadre autorisé.',
  'Développement de sites, applications et outils métier : des besoins',
  'définis ensemble, des données maîtrisées et une maintenance prévue.',
].join(' ');

useSeoMeta({
  title,
  description,
  robots: 'index, follow',

  ogType: 'website',
  ogTitle: title,
  ogDescription: description,
  ogUrl: canonicalUrl,
  ogSiteName: 'PixelProwlers',

  twitterCard: 'summary',
  twitterTitle: title,
  twitterDescription: description,
});

useHead({
  link: [
    {
      rel: 'canonical',
      href: canonicalUrl,
    },
  ],

  script: [
    {
      type: 'application/ld+json',
      textContent: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'WebPage',
        name: title,
        description,
        url: canonicalUrl,
        isPartOf: {
          '@type': 'WebSite',
          name: 'PixelProwlers',
          url: siteUrl,
        },
        about: [
          'Conseil et assistance informatique',
          'Audit de sécurité de site web',
          'Transmission et sécurisation des accès',
          'Développement de sites, applications et outils métier',
          'Autonomie numérique',
        ],
      }),
    },
  ],
});
</script>

<style scoped>
@reference "../assets/css/main.css";

.pillar-page {
  @apply bg-pxp-paper text-pxp-ink;
}

.pillar-hero {
  @apply border-b border-pxp-green/15 bg-pxp-panel py-12 md:py-16;
}

.pillar-hero-content {
  @apply grid gap-5;
}

.pillar-hero h1 {
  @apply max-w-4xl text-4xl font-black leading-tight text-pxp-ink md:text-5xl;
}

.pillar-introduction {
  @apply max-w-3xl text-lg font-semibold leading-relaxed text-pxp-ink/80;
}

.pillar-actions {
  @apply flex flex-wrap gap-3;
}

.cta-note {
  @apply max-w-3xl text-sm font-semibold leading-relaxed text-pxp-ink/70;
}

.pillar-section {
  @apply py-12 md:py-16;
}

.pillar-section-alt {
  @apply border-t border-pxp-green/15 bg-pxp-panel;
}

.pillar-section h2 {
  @apply text-3xl font-black leading-tight text-pxp-ink;
}

.pillar-section-intro {
  @apply mt-3 max-w-3xl font-semibold leading-relaxed text-pxp-ink/80;
}

.pillar-card-grid {
  @apply mt-8 grid gap-4 md:grid-cols-2;
}

.pillar-card {
  @apply grid content-start gap-2 rounded-xl border border-pxp-green/20 bg-white p-5 shadow-sm md:p-6;
}

.pillar-card h3 {
  @apply text-lg font-black text-pxp-ink;
}

.pillar-card p {
  @apply font-semibold leading-relaxed text-pxp-ink/80;
}

.pillar-card-link {
  @apply mt-1 inline-flex min-h-11 items-center font-black text-pxp-green underline decoration-2 underline-offset-4;
}

.pillar-card-link:hover {
  @apply text-pxp-ink;
}

.pillar-card-link:focus-visible {
  @apply outline-none ring-2 ring-pxp-green ring-offset-2;
}

.pillar-principles {
  @apply mt-6 grid gap-2 pl-5;
  list-style: disc;
}

.pillar-principles li {
  @apply font-semibold leading-relaxed text-pxp-ink/80;
}

.pillar-boundary {
  @apply mt-6 max-w-3xl rounded-lg border-2 border-pxp-orange/50 bg-pxp-orange/10 p-4 font-semibold leading-relaxed text-pxp-ink;
}

.pillar-final {
  @apply bg-pxp-blue py-16 text-white md:py-20;
}

.pillar-final h2 {
  @apply text-3xl font-black leading-tight md:text-4xl;
}

.pillar-final p {
  @apply mt-3 max-w-3xl font-semibold leading-relaxed text-white/85;
}

.pillar-final .pillar-actions {
  @apply mt-6;
}
</style>
