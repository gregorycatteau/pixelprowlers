<template>
  <main class="diagnostic-page">
    <section class="hero-section" aria-labelledby="diagnostic-title">
      <div class="container-site hero-grid">
        <div>
          <p class="eyebrow">Diagnostic interactif</p>
          <h1 id="diagnostic-title">Votre site est-il une passoire ?</h1>
          <p class="hero-text">
            Un diagnostic simple pour repérer les angles morts fréquents : accès, comptes,
            sauvegardes, formulaires, outils maintenus et dépendance humaine.
          </p>
          <p class="security-note">
            Ne transmettez aucun mot de passe, clé privée, token, accès administrateur ou information
            sensible via ce diagnostic. Ne mentionnez pas votre domaine, vos accès, vos tokens ou vos
            informations internes.
          </p>
        </div>

        <aside class="score-panel" aria-labelledby="score-title">
          <p class="panel-kicker">Progression</p>
          <h2 id="score-title">{{ answeredCount }} / {{ totalQuestions }} réponses</h2>
          <div class="progress-track" aria-hidden="true">
            <span :class="progressClass"></span>
          </div>
          <p>
            Les réponses restent dans la mémoire de cette page. Rien n’est envoyé, stocké, journalisé
            ou ajouté à l’adresse de la page.
          </p>
        </aside>
      </div>
    </section>

    <section class="question-section" aria-labelledby="axes-title">
      <div class="container-site">
        <div class="section-heading">
          <p class="eyebrow light">6 angles morts</p>
          <h2 id="axes-title">Répondez sans chercher la perfection.</h2>
          <p>
            “Je ne sais pas” est une réponse utile. Elle signale surtout un point à documenter.
            Ne renseignez aucun nom de domaine, identifiant, secret ou détail interne.
          </p>
        </div>

        <div class="axis-grid">
          <fieldset v-for="axis in axes" :key="axis.id" class="axis-card">
            <legend>
              <span>{{ axis.number }}</span>
              {{ axis.title }}
            </legend>
            <p>{{ axis.description }}</p>

            <div class="question-list">
              <div v-for="question in axis.questions" :key="question.id" class="question-block">
                <p :id="`${question.id}-label`">{{ question.label }}</p>
                <div class="answer-grid" :aria-labelledby="`${question.id}-label`" role="radiogroup">
                  <label v-for="option in answerOptions" :key="option.value">
                    <input
                      v-model="answers[question.id]"
                      :name="question.id"
                      :value="option.value"
                      type="radio"
                    />
                    <span>{{ option.label }}</span>
                  </label>
                </div>
              </div>
            </div>
          </fieldset>
        </div>
      </div>
    </section>

    <section class="result-section" aria-labelledby="result-title" aria-live="polite">
      <div class="container-site result-grid">
        <div class="result-card">
          <p class="eyebrow light">Résultat</p>
          <template v-if="answeredCount > 0">
            <h2 id="result-title">{{ result.level }}</h2>
            <p class="score-line">{{ scorePercent }} % d’angles morts probables</p>
            <p>{{ result.message }}</p>

            <div>
              <h3>Trois priorités concrètes</h3>
              <ul>
                <li v-for="priority in result.priorities" :key="priority">{{ priority }}</li>
              </ul>
            </div>

            <div class="result-actions">
              <NuxtLink :to="result.cta.href" class="primary-result-action">{{ result.cta.label }}</NuxtLink>
              <button type="button" class="secondary-result-action" @click="copySafeSummary">
                Copier mon résumé non sensible
              </button>
              <button type="button" class="secondary-result-action" @click="resetAnswers">
                Refaire le diagnostic
              </button>
            </div>
            <p v-if="copyMessage" class="copy-feedback">{{ copyMessage }}</p>
          </template>

          <div v-else class="empty-result">
            <h2 id="result-title">Répondez aux questions pour obtenir une première lecture.</h2>
            <p>
              Le résultat apparaîtra ici au fil de vos réponses. Il sert à prioriser, pas à juger.
            </p>
          </div>
        </div>

        <aside class="link-panel" aria-labelledby="links-title">
          <h2 id="links-title">Ressources liées</h2>
          <nav aria-label="Ressources recommandées après diagnostic">
            <NuxtLink v-for="link in recommendedLinks" :key="link.href" :to="link.href">
              {{ link.label }}
            </NuxtLink>
          </nav>
        </aside>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue';

usePixelSeo({
  title: 'Diagnostic site passoire | PixelProwlers',
  description: 'Diagnostic interactif sans backend pour repérer les angles morts d’un site web : accès, sauvegardes, formulaires, outils non maintenus et dépendance humaine.',
  path: '/diagnostic-site-passoire',
});

type AnswerValue = 'yes' | 'no' | 'unknown';

type Question = {
  id: string;
  label: string;
  healthyAnswer: 'yes' | 'no';
};

type Axis = {
  id: string;
  number: string;
  title: string;
  description: string;
  links: Array<{ label: string; href: string }>;
  questions: Question[];
};

type ResultLevel = {
  level: string;
  message: string;
  priorities: string[];
  cta: {
    label: string;
    href: string;
  };
};

const answerOptions: Array<{ label: string; value: AnswerValue }> = [
  { label: 'Oui', value: 'yes' },
  { label: 'Non', value: 'no' },
  { label: 'Je ne sais pas', value: 'unknown' },
];

const axes: Axis[] = [
  {
    id: 'access',
    number: '01',
    title: 'Accès et mots de passe',
    description: 'Les comptes critiques doivent être uniques, identifiés et protégés.',
    links: [
      { label: 'Audit sécurité de site web', href: '/audit-site-web' },
      { label: 'Ne plus dépendre d’une seule personne', href: '/ne-plus-dependre-une-seule-personne-site' },
    ],
    questions: [
      { id: 'unique_passwords', label: 'Utilisez-vous des mots de passe uniques pour l’hébergement, le CMS, les emails et les outils de facturation ?', healthyAnswer: 'yes' },
      { id: 'mfa_enabled', label: 'La double authentification est-elle activée sur les comptes critiques ?', healthyAnswer: 'yes' },
      { id: 'main_access_known', label: 'Savez-vous qui possède les accès principaux ?', healthyAnswer: 'yes' },
    ],
  },
  {
    id: 'rights',
    number: '02',
    title: 'Droits et comptes utilisateurs',
    description: 'Un ancien accès oublié reste une porte ouverte trop longtemps.',
    links: [
      { label: 'Maintenance site web pour TPE et associations', href: '/maintenance-site-web-tpe-associations' },
      { label: 'Sécuriser un WordPress associatif', href: '/securiser-site-wordpress-associatif' },
    ],
    questions: [
      { id: 'old_accounts_removed', label: 'Les anciens prestataires, bénévoles ou salariés ont-ils encore des accès ?', healthyAnswer: 'no' },
      { id: 'admin_limited', label: 'Les comptes administrateurs sont-ils limités au strict nécessaire ?', healthyAnswer: 'yes' },
      { id: 'rights_reviewed', label: 'Une revue des droits est-elle faite régulièrement ?', healthyAnswer: 'yes' },
    ],
  },
  {
    id: 'backups',
    number: '03',
    title: 'Sauvegardes',
    description: 'Un site sans sauvegarde testée n’est pas maintenu.',
    links: [
      { label: 'Sauvegardes site web : erreurs fréquentes', href: '/sauvegardes-site-web-erreurs-frequentes' },
      { label: 'Audit sécurité de site web', href: '/audit-site-web' },
    ],
    questions: [
      { id: 'automatic_backup', label: 'Existe-t-il une sauvegarde automatique récente ?', healthyAnswer: 'yes' },
      { id: 'restore_tested', label: 'Une restauration a-t-elle déjà été testée ?', healthyAnswer: 'yes' },
      { id: 'offsite_backup', label: 'Les sauvegardes sont-elles stockées ailleurs que sur le même hébergement ?', healthyAnswer: 'yes' },
    ],
  },
  {
    id: 'forms',
    number: '04',
    title: 'Formulaires exposés',
    description: 'Un formulaire doit aider les vrais humains, pas ouvrir une zone d’abus.',
    links: [
      { label: 'Formulaire exposé au spam et aux injections', href: '/formulaire-contact-spam-injections' },
      { label: 'Audit sécurité de site web', href: '/audit-site-web' },
    ],
    questions: [
      { id: 'spam_protection', label: 'Le formulaire est-il protégé contre le spam ?', healthyAnswer: 'yes' },
      { id: 'server_validation', label: 'Les champs sont-ils validés côté serveur ?', healthyAnswer: 'yes' },
      { id: 'suspicious_messages', label: 'Recevez-vous des messages suspects ou répétitifs ?', healthyAnswer: 'no' },
    ],
  },
  {
    id: 'maintenance',
    number: '05',
    title: 'Outils, CMS ou plugins non maintenus',
    description: 'Un outil oublié reste visible pour les pannes comme pour les abus automatisés.',
    links: [
      { label: 'Maintenance site web pour TPE et associations', href: '/maintenance-site-web-tpe-associations' },
      { label: 'Sécuriser un WordPress associatif', href: '/securiser-site-wordpress-associatif' },
    ],
    questions: [
      { id: 'tools_updated', label: 'Le CMS, les plugins ou dépendances sont-ils à jour ?', healthyAnswer: 'yes' },
      { id: 'unused_removed', label: 'Les outils inutilisés ont-ils été supprimés ?', healthyAnswer: 'yes' },
      { id: 'inventory_known', label: 'Savez-vous quels outils tournent encore sur le site ?', healthyAnswer: 'yes' },
    ],
  },
  {
    id: 'dependency',
    number: '06',
    title: 'Dépendance à une seule personne',
    description: 'Le bon outil est celui que votre équipe peut garder en main.',
    links: [
      { label: 'Ne plus dépendre d’une seule personne', href: '/ne-plus-dependre-une-seule-personne-site' },
      { label: 'Ressources pratiques', href: '/ressources' },
    ],
    questions: [
      { id: 'single_person_access', label: 'Une seule personne connaît-elle les accès ?', healthyAnswer: 'no' },
      { id: 'minimal_docs', label: 'Une documentation minimale existe-t-elle ?', healthyAnswer: 'yes' },
      { id: 'backup_person', label: 'Quelqu’un peut-il intervenir si la personne principale est indisponible ?', healthyAnswer: 'yes' },
    ],
  },
];

const answers = reactive<Record<string, AnswerValue | ''>>(
  Object.fromEntries(axes.flatMap((axis) => axis.questions.map((question) => [question.id, ''])))
);
const copyMessage = ref('');

const totalQuestions = axes.reduce((count, axis) => count + axis.questions.length, 0);

// Compte les questions auxquelles une réponse a été donnée.
const answeredCount = computed(() => Object.values(answers).filter(Boolean).length);

// Calcule la progression du diagnostic sans tenir compte du niveau de risque.
const progressPercent = computed(() => Math.round((answeredCount.value / totalQuestions) * 100));

// Convertit la progression en classe CSS bornée pour éviter le style inline dynamique.
const progressClass = computed(() => `progress-${Math.round(progressPercent.value / 10) * 10}`);

// Transforme une réponse en score de fragilité local, sans envoyer ni stocker de donnée.
const scoreQuestion = (question: Question) => {
  const answer = answers[question.id];

  if (!answer) {
    return 0;
  }

  if (answer === 'unknown') {
    return 1;
  }

  return answer === question.healthyAnswer ? 0 : 2;
};

// Calcule le score global en pourcentage à partir des réponses locales.
const scorePercent = computed(() => {
  const maxScore = totalQuestions * 2;
  const score = axes.reduce(
    (axisTotal, axis) => axisTotal + axis.questions.reduce(
      (questionTotal, question) => questionTotal + scoreQuestion(question),
      0
    ),
    0
  );

  return Math.round((score / maxScore) * 100);
});

// Sélectionne le niveau de résultat en fonction du score obtenu.
const result = computed<ResultLevel>(() => {
  if (scorePercent.value <= 25) {
    return {
      level: 'Base plutôt saine',
      message: 'Votre base semble plutôt saine. Quelques vérifications régulières permettront d’éviter les mauvaises surprises.',
      priorities: [
        'Tester une restauration.',
        'Documenter les accès.',
        'Vérifier les comptes inutilisés.',
      ],
      cta: { label: 'Faire vérifier mon site', href: '/audit-site-web' },
    };
  }

  if (scorePercent.value <= 50) {
    return {
      level: 'Fragilité probable',
      message: 'Votre site tient peut-être debout, mais certains détails peuvent devenir problématiques en cas de panne, départ ou attaque automatisée.',
      priorities: [
        'Vérifier les sauvegardes.',
        'Revoir les droits.',
        'Sécuriser les accès critiques.',
      ],
      cta: { label: 'Lancer un audit léger', href: '/audit-site-web' },
    };
  }

  if (scorePercent.value <= 75) {
    return {
      level: 'Risque important',
      message: 'Plusieurs angles morts peuvent fragiliser votre structure. Le risque principal n’est pas forcément spectaculaire : il peut venir d’un oubli, d’un compte dormant ou d’une sauvegarde inutilisable.',
      priorities: [
        'Cartographier les accès.',
        'Prioriser les corrections.',
        'Documenter les procédures minimales.',
      ],
      cta: { label: 'Cartographier mes accès', href: '/contact' },
    };
  }

  return {
    level: 'Situation critique',
    message: 'Votre situation mérite une priorisation rapide. L’objectif n’est pas de paniquer, mais d’éviter qu’une panne, une erreur ou une compromission transforme un détail oublié en blocage complet.',
    priorities: [
      'Identifier les accès critiques.',
      'Vérifier l’existence de sauvegardes exploitables.',
      'Planifier une intervention cadrée.',
    ],
    cta: { label: 'Décrire mon urgence', href: '/contact' },
  };
});

// Remonte les axes qui semblent les plus fragiles pour proposer les ressources les plus utiles.
const recommendedLinks = computed(() => {
  const rankedAxes = axes
    .map((axis) => ({
      axis,
      score: axis.questions.reduce((total, question) => total + scoreQuestion(question), 0),
    }))
    .sort((first, second) => second.score - first.score);

  const links = rankedAxes.flatMap(({ axis }) => axis.links);
  const uniqueLinks = new Map<string, { label: string; href: string }>();

  [
    ...links,
    { label: 'Audit sécurité de site web', href: '/audit-site-web' },
    { label: 'Ressources PixelProwlers', href: '/ressources' },
  ].forEach((link) => {
    uniqueLinks.set(link.href, link);
  });

  return Array.from(uniqueLinks.values()).slice(0, 5);
});

// Identifie les axes les plus fragiles sans exposer de réponse détaillée ni information interne.
const weakAxes = computed(() => axes
  .map((axis) => ({
    title: axis.title,
    score: axis.questions.reduce((total, question) => total + scoreQuestion(question), 0),
  }))
  .filter((axis) => axis.score > 0)
  .sort((first, second) => second.score - first.score)
  .slice(0, 3)
  .map((axis) => axis.title)
);

// Produit un résumé volontairement non sensible à coller manuellement dans le formulaire de contact.
const buildSafeSummary = () => {
  const axesText = weakAxes.value.length ? weakAxes.value.join(', ') : 'Aucun axe majeur identifié';

  return [
    'Résumé non sensible du diagnostic PixelProwlers',
    `Niveau : ${result.value.level}`,
    `Axes à regarder en priorité : ${axesText}`,
    `Priorités : ${result.value.priorities.join(' / ')}`,
    'Aucun domaine, accès, token, mot de passe ou détail interne n’est inclus dans ce résumé.',
  ].join('\n');
};

// Copie le résumé non sensible si l’API Clipboard est disponible, sinon affiche une consigne claire.
const copySafeSummary = async () => {
  copyMessage.value = '';

  if (!navigator.clipboard?.writeText) {
    copyMessage.value = 'Copie automatique indisponible. Vous pouvez résumer le niveau et les priorités dans le formulaire de contact.';
    return;
  }

  try {
    await navigator.clipboard.writeText(buildSafeSummary());
    copyMessage.value = 'Résumé non sensible copié. Vous pouvez le coller dans le message du formulaire de contact.';
  } catch {
    copyMessage.value = 'Copie impossible. Vous pouvez résumer manuellement le niveau et les priorités dans le formulaire de contact.';
  }
};

// Réinitialise les réponses locales sans contacter de service externe.
const resetAnswers = () => {
  Object.keys(answers).forEach((key) => {
    answers[key] = '';
  });
  copyMessage.value = '';
};
</script>

<style scoped>
.diagnostic-page {
  @apply min-h-screen bg-night text-white;
}

.hero-section {
  @apply border-b border-scan/15 bg-night py-16 md:py-24;
}

.hero-grid {
  @apply grid gap-8 lg:grid-cols-[1.05fr_0.75fr] lg:items-center;
}

.eyebrow {
  @apply font-mono text-xs font-bold uppercase tracking-[0.24em] text-scan;
}

.eyebrow.light {
  @apply text-scan;
}

.hero-section h1 {
  @apply mt-5 max-w-4xl font-heading text-4xl font-black leading-[1.04] text-white sm:text-5xl xl:text-6xl;
}

.hero-text {
  @apply mt-6 max-w-3xl text-lg leading-8 text-white/80 md:text-xl;
}

.security-note {
  @apply mt-8 rounded-lg border border-action/35 bg-action/10 px-5 py-4 font-bold leading-7 text-white;
}

.score-panel {
  @apply rounded-lg border border-scan/20 bg-white/[0.055] p-6 shadow-[0_24px_70px_rgba(0,0,0,0.24)] md:p-8;
}

.panel-kicker {
  @apply font-mono text-xs font-bold uppercase tracking-[0.22em] text-scan;
}

.score-panel h2 {
  @apply mt-4 font-heading text-3xl font-black text-white;
}

.progress-track {
  @apply mt-6 h-3 overflow-hidden rounded-full bg-white/10;
}

.progress-track span {
  @apply block h-full rounded-full bg-scan transition-all duration-300;
}

.progress-0 {
  @apply w-0;
}

.progress-10 {
  @apply w-[10%];
}

.progress-20 {
  @apply w-[20%];
}

.progress-30 {
  @apply w-[30%];
}

.progress-40 {
  @apply w-[40%];
}

.progress-50 {
  @apply w-1/2;
}

.progress-60 {
  @apply w-[60%];
}

.progress-70 {
  @apply w-[70%];
}

.progress-80 {
  @apply w-4/5;
}

.progress-90 {
  @apply w-[90%];
}

.progress-100 {
  @apply w-full;
}

.score-panel p:not(.panel-kicker) {
  @apply mt-5 leading-7 text-white/75;
}

.question-section {
  @apply bg-[#0B1826] py-16 md:py-24;
}

.section-heading {
  @apply max-w-3xl;
}

.section-heading h2 {
  @apply mt-4 font-heading text-3xl font-black text-white md:text-5xl;
}

.section-heading p {
  @apply mt-5 text-lg leading-8 text-white/80;
}

.axis-grid {
  @apply mt-10 grid gap-5 lg:grid-cols-2;
}

.axis-card {
  @apply rounded-lg border border-scan/15 bg-white/[0.055] p-6 shadow-[0_18px_50px_rgba(0,0,0,0.16)];
}

.axis-card legend {
  @apply font-heading text-2xl font-black text-white;
}

.axis-card legend span {
  @apply mr-3 font-mono text-sm font-bold text-scan;
}

.axis-card > p {
  @apply mt-4 leading-7 text-white/75;
}

.question-list {
  @apply mt-6 grid gap-5;
}

.question-block {
  @apply rounded-lg border border-white/10 bg-night/45 p-4;
}

.question-block > p {
  @apply font-bold leading-7 text-white;
}

.answer-grid {
  @apply mt-4 grid gap-3 sm:grid-cols-3;
}

.answer-grid label {
  @apply cursor-pointer;
}

.answer-grid input {
  @apply sr-only;
}

.answer-grid span {
  @apply flex min-h-11 items-center justify-center rounded-lg border border-white/15 bg-white/[0.055] px-4 py-2 text-center text-sm font-extrabold text-white outline-none transition;
}

.answer-grid label:hover span {
  @apply border-scan/60 bg-white/[0.085];
}

.answer-grid input:focus-visible + span {
  @apply border-scan ring-2 ring-scan ring-offset-2 ring-offset-night;
}

.answer-grid input:checked + span {
  @apply border-scan bg-scan/15 text-scan;
}

.result-section {
  @apply border-t border-scan/15 bg-night py-16 md:py-24;
}

.result-grid {
  @apply grid gap-8 lg:grid-cols-[minmax(0,1fr)_22rem] lg:items-start;
}

.result-card,
.link-panel {
  @apply rounded-lg border border-scan/20 bg-white/[0.055] p-6 shadow-[0_24px_70px_rgba(0,0,0,0.22)] md:p-8;
}

.result-card h2 {
  @apply mt-4 font-heading text-3xl font-black text-white md:text-5xl;
}

.score-line {
  @apply mt-4 inline-flex rounded-lg border border-scan/20 bg-scan/10 px-4 py-2 font-mono text-sm font-bold text-scan;
}

.result-card p:not(.eyebrow):not(.score-line) {
  @apply mt-5 max-w-4xl leading-8 text-white/80;
}

.empty-result h2 {
  @apply mt-4 max-w-3xl font-heading text-3xl font-black leading-tight text-white md:text-4xl;
}

.empty-result p {
  @apply mt-5 max-w-3xl leading-8 text-white/80;
}

.result-card h3,
.link-panel h2 {
  @apply mt-8 font-heading text-2xl font-black text-white;
}

.result-card ul {
  @apply mt-5 grid gap-3;
}

.result-card li {
  @apply rounded-lg border border-white/10 bg-night/45 px-4 py-3 font-semibold leading-6 text-white/85;
}

.result-actions {
  @apply mt-8 flex flex-col gap-3 sm:flex-row;
}

.primary-result-action {
  @apply inline-flex min-h-12 items-center justify-center rounded-lg bg-action px-6 py-3 text-center font-extrabold text-white shadow-orange outline-none transition hover:bg-[#FF9F2D] focus-visible:ring-2 focus-visible:ring-action focus-visible:ring-offset-2 focus-visible:ring-offset-night;
}

.secondary-result-action {
  @apply inline-flex min-h-12 items-center justify-center rounded-lg border-2 border-scan px-6 py-3 text-center font-extrabold text-white outline-none transition hover:bg-scan/10 focus-visible:ring-2 focus-visible:ring-scan focus-visible:ring-offset-2 focus-visible:ring-offset-night;
}

.copy-feedback {
  @apply mt-5 rounded-lg border border-scan/20 bg-scan/10 px-4 py-3 text-sm font-bold leading-6 text-white;
}

.link-panel {
  @apply lg:sticky lg:top-28;
}

.link-panel h2 {
  @apply mt-0;
}

.link-panel nav {
  @apply mt-5 grid gap-3;
}

.link-panel a {
  @apply rounded-lg border border-white/10 bg-night/45 px-4 py-3 text-sm font-bold leading-6 text-white/85 outline-none transition hover:border-scan hover:text-scan focus-visible:ring-2 focus-visible:ring-scan focus-visible:ring-offset-2 focus-visible:ring-offset-night;
}

@media (prefers-reduced-motion: reduce) {
  .progress-track span,
  .answer-grid span,
  .primary-result-action,
  .secondary-result-action,
  .link-panel a {
    @apply transition-none;
  }
}
</style>
