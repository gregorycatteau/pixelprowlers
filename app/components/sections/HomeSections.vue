<template>
  <div class="HomeSections">
    <section
      id="solutions"
      class="HomeSection HomeSectionAlt"
      aria-labelledby="offers-title"
    >
      <div class="container">
        <header v-reveal class="SectionHeading">
          <p class="eyebrow">
            Quatre situations, quatre réponses
          </p>

          <h2 id="offers-title">
            Commencez par le besoin réel, pas par une solution imposée
          </h2>

          <p>
            Une panne, un audit, une réparation et une transmission
            d’accès ne demandent ni le même travail ni le même niveau
            d’engagement. Chaque offre possède donc son propre périmètre,
            ses livrables et ses limites.
          </p>
        </header>

        <div v-reveal class="OfferGrid">
          <article
            v-for="offer in offers"
            :key="offer.title"
            class="OfferCard"
          >
            <p class="OfferKicker">
              {{ offer.kicker }}
            </p>

            <h3>
              {{ offer.title }}
            </h3>

            <p class="OfferDescription">
              {{ offer.description }}
            </p>

            <div class="OfferDeliverables">
              <h4>Ce que vous obtenez</h4>

              <ul>
                <li
                  v-for="deliverable in offer.deliverables"
                  :key="deliverable"
                >
                  <span aria-hidden="true">✓</span>
                  <span>{{ deliverable }}</span>
                </li>
              </ul>
            </div>

            <p class="OfferBoundary">
              <strong>Limite :</strong>
              {{ offer.boundary }}
            </p>

            <p class="OfferPricing">
              <strong>Méthode de prix :</strong>
              {{ offer.pricing }}
            </p>

            <AppButton
              class="OfferAction"
              :href="offer.href"
            >
              {{ offer.cta }}
            </AppButton>
          </article>
        </div>

        <aside
          class="PricingFramework"
          aria-labelledby="pricing-framework-title"
        >
          <div>
            <p class="eyebrow">
              Avant tout engagement
            </p>

            <h3 id="pricing-framework-title">
              Le prix suit un périmètre compréhensible
            </h3>
          </div>

          <p>
            Lorsqu’une intervention est proposée, elle distingue les
            livrables, les exclusions, les accès nécessaires, les délais
            prévisionnels et le prix. Aucun travail supplémentaire n’est
            ajouté sans validation.
          </p>
        </aside>
      </div>
    </section>

    <section
      id="autonomie"
      class="HomeSection"
      aria-labelledby="autonomy-title"
    >
      <div class="container">
        <header v-reveal class="SectionHeading">
          <p class="eyebrow">
            Autonomie numérique
          </p>

          <h2 id="autonomy-title">
            La souveraineté utile commence par la liberté de choisir
          </h2>

          <p>
            Il ne s’agit pas de vous reprocher les outils que vous utilisez.
            Il s’agit de réduire progressivement ce qui vous empêche de
            récupérer vos données, vos accès ou la maîtrise de votre site.
          </p>
        </header>

        <div v-reveal class="PrincipleGrid">
          <article
            v-for="principle in autonomyPrinciples"
            :key="principle.title"
            class="PrincipleCard"
          >
            <span
              class="PrincipleNumber"
              aria-hidden="true"
            >
              {{ principle.number }}
            </span>

            <h3>
              {{ principle.title }}
            </h3>

            <p>
              {{ principle.description }}
            </p>
          </article>
        </div>
      </div>
    </section>

    <section
      id="livrables"
      class="HomeSection HomeSectionAlt"
      aria-labelledby="evidence-title"
    >
      <div class="container">
        <header v-reveal class="SectionHeading">
          <p class="eyebrow">
            Confiance vérifiable
          </p>

          <h2 id="evidence-title">
            Une intervention sérieuse doit laisser des traces utiles
          </h2>

          <p>
            Les livrables exacts dépendent de la prestation retenue.
            Le cadre recherché reste le même : vous permettre de comprendre
            ce qui a été observé, décidé, modifié et transmis.
          </p>
        </header>

        <div v-reveal class="EvidenceGrid">
          <article
            v-for="evidence in evidenceItems"
            :key="evidence.title"
            class="EvidenceCard"
          >
            <h3>
              {{ evidence.title }}
            </h3>

            <p>
              {{ evidence.description }}
            </p>

            <p class="EvidenceUse">
              <strong>Utilité :</strong>
              {{ evidence.use }}
            </p>
          </article>
        </div>
      </div>
    </section>

    <section
      id="methode"
      class="HomeSection"
      aria-labelledby="method-title"
    >
      <div class="container MethodLayout">
        <header v-reveal class="SectionHeading">
          <p class="eyebrow">
            Méthode d’intervention
          </p>

          <h2 id="method-title">
            Comprendre avant d’accéder, cadrer avant de modifier
          </h2>

          <p>
            La méthode sépare la qualification, la décision, l’intervention
            et la transmission. Vous savez ainsi à quel moment un accès peut
            être demandé et ce qui doit être validé.
          </p>
        </header>

        <ol class="MethodSteps">
          <li
            v-for="step in methodSteps"
            :key="step.number"
            class="MethodStep"
          >
            <span
              class="MethodStepNumber"
              aria-hidden="true"
            >
              {{ step.number }}
            </span>

            <div>
              <h3>
                {{ step.title }}
              </h3>

              <p>
                {{ step.description }}
              </p>
            </div>
          </li>
        </ol>
      </div>
    </section>

    <section
      id="collaboration"
      class="HomeSection HomeSectionAlt"
      aria-labelledby="collaboration-title"
    >
      <div class="container">
        <header v-reveal class="SectionHeading">
          <p class="eyebrow">
            Cadre de collaboration
          </p>

          <h2 id="collaboration-title">
            Vérifions que la manière de travailler vous convient
          </h2>

          <p>
            Une bonne collaboration repose autant sur le cadre de décision
            que sur la solution technique.
          </p>
        </header>

        <div v-reveal class="CollaborationGrid">
          <article class="CollaborationCard CollaborationCardPositive">
            <h3>
              Ce cadre est adapté si vous souhaitez…
            </h3>

            <ul>
              <li
                v-for="item in goodFits"
                :key="item"
              >
                <span aria-hidden="true">✓</span>
                <span>{{ item }}</span>
              </li>
            </ul>
          </article>

          <article class="CollaborationCard">
            <h3>
              Un autre cadre sera préférable si vous attendez…
            </h3>

            <ul>
              <li
                v-for="item in unsuitableFits"
                :key="item"
              >
                <span aria-hidden="true">—</span>
                <span>{{ item }}</span>
              </li>
            </ul>
          </article>
        </div>
      </div>
    </section>

    <section
      id="contact"
      class="FinalSection"
      aria-labelledby="final-title"
    >
      <div class="container">
        <div v-reveal class="FinalPanel">
          <div>
            <p class="FinalEyebrow">
              Première orientation
            </p>

            <h2 id="final-title">
              Vous ne savez pas encore quelle offre choisir&nbsp;?
            </h2>

            <p>
              Le pré-diagnostic vous aide à situer votre priorité en quatre
              questions. Son résultat est immédiat et indicatif : vous
              décidez ensuite si vous souhaitez transmettre une demande.
            </p>
          </div>

          <div class="FinalActions">
            <AppButton href="/diagnostic-situation">
              Faire le pré-diagnostic
            </AppButton>

            <AppButton
              variant="secondary"
              href="/contact"
            >
              Décrire ma situation
            </AppButton>
          </div>

          <p class="FinalNote">
            Aucun mot de passe ni accès privé n’est demandé dans ces
            formulaires. Vous pouvez aussi appeler le
            <a href="tel:+33668145152">06 68 14 51 52</a>.
          </p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';

const offers = [
  {
    kicker: 'Incident en cours',
    title: 'Qualification d’un incident web',

    description:
      'Pour un site inaccessible, un accès perdu, une fonction bloquée ou une modification suspecte.',

    deliverables: [
      'Une référence de dossier',
      'Une qualification des faits et de leur impact',
      'Une prochaine étape adaptée à la situation observée',
      'Un périmètre séparé si une intervention est nécessaire',
    ],

    boundary:
      'L’enregistrement ne garantit ni la disponibilité immédiate d’un intervenant ni un délai de résolution.',

    pricing:
      'La qualification et l’éventuelle intervention sont distinguées avant tout engagement financier.',

    href: '/urgence',
    cta: 'Signaler un incident',
  },

  {
    kicker: 'Vérifier avant de décider',
    title: 'Audit ciblé d’un site web',

    description:
      'Pour distinguer les problèmes observables, les risques potentiels et les améliorations simplement souhaitables.',

    deliverables: [
      'Un périmètre de vérification défini',
      'Des constats reliés aux éléments observés',
      'Des priorités classées par impact',
      'Une restitution compréhensible',
    ],

    boundary:
      'Les corrections et la refonte ne sont pas incluses sauf si elles figurent explicitement dans le périmètre accepté.',

    pricing:
      'Le prix dépend du nombre de services examinés, de la profondeur des vérifications et des accès nécessaires.',

    href: '/audit-site-web',
    cta: 'Demander un audit',
  },

  {
    kicker: 'Réparer ou reconstruire',
    title: 'Site web maintenable',

    description:
      'Pour réparer l’existant ou reconstruire ce qui ne peut plus être maintenu dans de bonnes conditions.',

    deliverables: [
      'Un périmètre fonctionnel validé',
      'Les réparations ou développements convenus',
      'Des vérifications avant mise à disposition',
      'Une documentation adaptée au projet',
    ],

    boundary:
      'Aucun résultat universel de performance, de référencement ou de sécurité ne peut être garanti sans contexte mesurable.',

    pricing:
      'Le prix dépend des fonctions retenues, de l’état de l’existant, des dépendances et du niveau de reprise nécessaire.',

    href: '/refonte-site',
    cta: 'Parler de mon site',
  },

  {
    kicker: 'Réduire la dépendance',
    title: 'Transmission et maîtrise des accès',

    description:
      'Pour savoir qui possède les comptes, qui peut intervenir et comment poursuivre sans dépendre d’une seule personne.',

    deliverables: [
      'Un inventaire des comptes et responsabilités',
      'L’identification des accès manquants ou incertains',
      'Une documentation des procédures essentielles',
      'Un plan de transmission validé',
    ],

    boundary:
      'Aucun compte n’est transféré, supprimé ou modifié sans autorisation explicite de la personne ou de l’organisation habilitée.',

    pricing:
      'Le prix dépend du nombre de comptes, d’intervenants, de services et de procédures à inventorier ou documenter.',

    href: '/transmission-acces',
    cta: 'Clarifier mes accès',
  },
] as const;

const autonomyPrinciples = [
  {
    number: '01',
    title: 'Réparer avant de remplacer',

    description:
      'L’existant est examiné avant de proposer une reconstruction. Une refonte n’est pertinente que si elle répond à un besoin démontré.',
  },

  {
    number: '02',
    title: 'Préserver la portabilité',

    description:
      'Les formats ouverts, les exports et la possibilité de changer de prestataire sont privilégiés lorsque le contexte le permet.',
  },

  {
    number: '03',
    title: 'Rendre les accès transmissibles',

    description:
      'Les comptes, responsabilités et procédures doivent pouvoir être compris par une personne autorisée autre que l’intervenant initial.',
  },
] as const;

const evidenceItems = [
  {
    title: 'Inventaire des accès',

    description:
      'Une vue des comptes, des propriétaires identifiés et des responsabilités liées aux services concernés.',

    use:
      'retrouver qui contrôle quoi et repérer les dépendances.',
  },

  {
    title: 'Constats et décisions',

    description:
      'Une distinction entre les faits observés, les hypothèses, les recommandations et les décisions finalement retenues.',

    use:
      'comprendre pourquoi une action a été réalisée ou écartée.',
  },

  {
    title: 'Trace des modifications',

    description:
      'Une description adaptée des changements effectués dans le périmètre de l’intervention.',

    use:
      'faciliter le suivi, la maintenance et une éventuelle reprise.',
  },

  {
    title: 'Documentation de transmission',

    description:
      'Des informations organisées pour les personnes qui devront administrer, maintenir ou faire évoluer la solution.',

    use:
      'éviter que la connaissance reste enfermée auprès d’un seul prestataire.',
  },
] as const;

const methodSteps = [
  {
    number: '1',
    title: 'Qualifier',

    description:
      'Nous distinguons les faits, leur impact et votre besoin sans demander de secret dans un formulaire.',
  },

  {
    number: '2',
    title: 'Cadrer',

    description:
      'Les livrables, les exclusions, les accès nécessaires, les délais prévisionnels et le prix sont présentés avant l’intervention.',
  },

  {
    number: '3',
    title: 'Intervenir',

    description:
      'Les actions restent limitées au périmètre accepté. Toute évolution importante fait l’objet d’une nouvelle validation.',
  },

  {
    number: '4',
    title: 'Transmettre',

    description:
      'Les éléments prévus sont restitués avec les informations nécessaires à leur compréhension et à leur continuité.',
  },
] as const;

const goodFits = [
  'Comprendre l’état réel d’un site avant de décider',
  'Réparer ce qui peut raisonnablement être conservé',
  'Reprendre la maîtrise de ses comptes et de ses données',
  'Avancer progressivement sans migration imposée',
  'Conserver une documentation exploitable',
] as const;

const unsuitableFits = [
  'Une promesse de résultat sans examen préalable',
  'Une intervention cachée ou impossible à retracer',
  'Le contournement d’un propriétaire de compte ou d’une autorisation',
  'Une modification sensible sans sauvegarde ni validation',
  'Une dépendance durable dont vous ne pourriez pas sortir',
] as const;
</script>

<style scoped>
@reference "../../assets/css/main.css";

.HomeSections {
  @apply bg-pxp-paper text-pxp-ink;
}

.HomeSection {
  @apply py-14 md:py-20;
}

.HomeSectionAlt {
  @apply border-y border-pxp-green/10 bg-pxp-panel;
}

.SectionHeading {
  @apply max-w-4xl;
}

.SectionHeading h2 {
  @apply text-3xl font-black leading-tight text-pxp-ink md:text-5xl;
}

.SectionHeading > p:not(.eyebrow) {
  @apply mt-5 max-w-3xl text-lg font-semibold leading-relaxed text-pxp-ink/75;
}

.OfferGrid {
  @apply mt-10 grid gap-6 lg:grid-cols-2;
}

.OfferCard {
  @apply flex h-full flex-col rounded-xl border border-pxp-green/20 bg-white p-6 shadow-sm md:p-8;
}

.OfferKicker {
  @apply text-xs font-black uppercase tracking-widest text-pxp-green;
}

.OfferCard h3 {
  @apply mt-3 text-2xl font-black leading-tight text-pxp-ink md:text-3xl;
}

.OfferDescription {
  @apply mt-4 font-semibold leading-relaxed text-pxp-ink/75;
}

.OfferDeliverables {
  @apply mt-6;
}

.OfferDeliverables h4 {
  @apply text-sm font-black uppercase tracking-wide text-pxp-ink;
}

.OfferDeliverables ul {
  @apply mt-3 grid gap-3 p-0;
  list-style: none;
}

.OfferDeliverables li {
  @apply flex items-start gap-3 font-semibold leading-relaxed text-pxp-ink/80;
}

.OfferDeliverables li > span:first-child {
  @apply font-black text-pxp-green;
}

.OfferBoundary,
.OfferPricing {
  @apply mt-5 rounded-lg px-4 py-3 text-sm font-semibold leading-relaxed;
}

.OfferBoundary {
  @apply border border-pxp-orange/20 bg-pxp-orange/10 text-pxp-ink;
}

.OfferPricing {
  @apply border border-pxp-green/20 bg-pxp-green/5 text-pxp-ink;
}

.OfferAction {
  @apply mt-6 self-start;
}

.PricingFramework {
  @apply mt-8 grid gap-5 rounded-xl border border-pxp-green/20 bg-pxp-ink p-6 text-white md:grid-cols-2 md:items-center md:p-8;
}

.PricingFramework .eyebrow {
  @apply text-primary-100;
}

.PricingFramework h3 {
  @apply text-2xl font-black leading-tight text-white;
}

.PricingFramework > p {
  @apply font-semibold leading-relaxed text-white/80;
}

.PrincipleGrid,
.EvidenceGrid {
  @apply mt-10 grid gap-6 md:grid-cols-2 lg:grid-cols-3;
}

.PrincipleCard,
.EvidenceCard {
  @apply rounded-xl border border-pxp-green/20 bg-white p-6;
}

.PrincipleNumber {
  @apply inline-flex h-11 w-11 items-center justify-center rounded-lg bg-pxp-green font-black text-white;
}

.PrincipleCard h3,
.EvidenceCard h3 {
  @apply mt-5 text-xl font-black text-pxp-ink;
}

.PrincipleCard p,
.EvidenceCard > p {
  @apply mt-3 font-semibold leading-relaxed text-pxp-ink/75;
}

.EvidenceGrid {
  @apply lg:grid-cols-2;
}

.EvidenceUse {
  @apply border-t border-pxp-green/15 pt-4;
}

.MethodLayout {
  @apply grid gap-10 lg:grid-cols-3;
}

.MethodLayout > .SectionHeading {
  @apply lg:col-span-1;
}

.MethodSteps {
  @apply grid gap-4 p-0 lg:col-span-2;
  list-style: none;
}

.MethodStep {
  @apply flex items-start gap-4 rounded-xl border border-pxp-green/20 bg-white p-5;
}

.MethodStepNumber {
  @apply flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-pxp-green font-black text-white;
}

.MethodStep h3 {
  @apply text-xl font-black text-pxp-ink;
}

.MethodStep p {
  @apply mt-2 font-semibold leading-relaxed text-pxp-ink/75;
}

.CollaborationGrid {
  @apply mt-10 grid gap-6 lg:grid-cols-2;
}

.CollaborationCard {
  @apply rounded-xl border border-pxp-green/20 bg-white p-6 md:p-8;
}

.CollaborationCardPositive {
  @apply border-pxp-green/30 bg-pxp-green/5;
}

.CollaborationCard h3 {
  @apply text-xl font-black text-pxp-ink;
}

.CollaborationCard ul {
  @apply mt-5 grid gap-4 p-0;
  list-style: none;
}

.CollaborationCard li {
  @apply flex items-start gap-3 font-semibold leading-relaxed text-pxp-ink/80;
}

.CollaborationCard li > span:first-child {
  @apply font-black text-pxp-green;
}

.FinalSection {
  @apply bg-pxp-paper py-14 md:py-20;
}

.FinalPanel {
  @apply rounded-xl border border-pxp-green/20 bg-pxp-ink p-6 text-white shadow-lg md:p-10;
}

.FinalEyebrow {
  @apply text-xs font-black uppercase tracking-widest text-primary-100;
}

.FinalPanel h2 {
  @apply mt-3 max-w-4xl text-3xl font-black leading-tight text-white md:text-5xl;
}

.FinalPanel > div:first-child > p:not(.FinalEyebrow) {
  @apply mt-5 max-w-3xl text-lg font-semibold leading-relaxed text-white/80;
}

.FinalActions {
  @apply mt-8 flex flex-col items-start gap-3 sm:flex-row sm:flex-wrap;
}

.FinalNote {
  @apply mt-5 max-w-3xl text-sm font-semibold leading-relaxed text-white/75;
}

.FinalNote a {
  @apply font-black text-primary-100 underline decoration-2 underline-offset-4;
}

@media (max-width: 639px) {
  .FinalActions .ButtonBase {
    @apply w-full justify-center text-center;
  }
}
</style>