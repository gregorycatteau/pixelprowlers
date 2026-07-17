<template>
  <main class="PrivacyPage">
    <section class="PrivacyHero" aria-labelledby="privacy-title">
      <div class="article-container">
        <NuxtLink to="/" class="BackLink">
          Retour à l’accueil
        </NuxtLink>

        <p class="eyebrow">Protection des données</p>

        <h1 id="privacy-title">
          Politique de confidentialité
        </h1>

        <p class="PrivacyIntroduction">
          Cette page explique quelles données PixelProwlers traite, pourquoi
          elles sont utilisées, combien de temps elles sont conservées et
          comment exercer vos droits.
        </p>

        <p class="PrivacyDate">
          Dernière mise à jour :
          <time datetime="2026-07-17">17 juillet 2026</time>
        </p>
      </div>
    </section>

    <section class="PrivacySection" aria-labelledby="controller-title">
      <div class="article-container">
        <p class="eyebrow">Responsable du traitement</p>

        <h2 id="controller-title">
          Qui détermine l’utilisation de vos données ?
        </h2>

        <div class="IdentityCard">
          <dl>
            <div>
              <dt>Nom commercial</dt>
              <dd>PixelProwlers</dd>
            </div>

            <div>
              <dt>Responsable du traitement</dt>
              <dd>{{ dataController.legalName }}</dd>
            </div>

            <div>
              <dt>Adresse postale</dt>
              <dd>{{ dataController.postalAddress }}</dd>
            </div>

            <div>
              <dt>Contact relatif aux données personnelles</dt>
              <dd>
                <a :href="`mailto:${dataController.email}`">
                  {{ dataController.email }}
                </a>
              </dd>
            </div>
          </dl>
        </div>

        <p class="SectionText">
          PixelProwlers agit comme responsable de traitement pour les données
          collectées directement sur ce site. Dans le cadre d’une mission
          réalisée pour un client, les rôles et responsabilités relatifs aux
          données traitées sont précisés dans le cadre contractuel applicable.
        </p>
      </div>
    </section>

    <section
      class="PrivacySection PrivacySectionAlt"
      aria-labelledby="principles-title"
    >
      <div class="article-container">
        <p class="eyebrow">Principes</p>

        <h2 id="principles-title">
          Une collecte limitée à ce qui est utile
        </h2>

        <div class="PrinciplesGrid">
          <article
            v-for="principle in privacyPrinciples"
            :key="principle.title"
            class="PrincipleCard"
          >
            <h3>{{ principle.title }}</h3>
            <p>{{ principle.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <section class="PrivacySection" aria-labelledby="processing-title">
      <div class="container">
        <div class="SectionHeading">
          <p class="eyebrow">Traitements réalisés</p>

          <h2 id="processing-title">
            Pourquoi vos données sont-elles utilisées ?
          </h2>

          <p>
            Chaque traitement possède une finalité, une base légale et une
            durée de conservation déterminées.
          </p>
        </div>

        <div class="ProcessingGrid">
          <article
            v-for="processing in processingActivities"
            :key="processing.title"
            class="ProcessingCard"
          >
            <h3>{{ processing.title }}</h3>

            <dl>
              <div>
                <dt>Données concernées</dt>
                <dd>{{ processing.data }}</dd>
              </div>

              <div>
                <dt>Finalités</dt>
                <dd>{{ processing.purpose }}</dd>
              </div>

              <div>
                <dt>Base légale</dt>
                <dd>{{ processing.legalBasis }}</dd>
              </div>

              <div>
                <dt>Destinataires</dt>
                <dd>{{ processing.recipients }}</dd>
              </div>

              <div>
                <dt>Conservation</dt>
                <dd>{{ processing.retention }}</dd>
              </div>
            </dl>
          </article>
        </div>
      </div>
    </section>

    <section
      class="PrivacySection PrivacySectionAlt"
      aria-labelledby="recipients-title"
    >
      <div class="article-container">
        <p class="eyebrow">Destinataires et prestataires</p>

        <h2 id="recipients-title">
          Qui peut accéder aux données ?
        </h2>

        <p class="SectionText">
          L’accès est limité aux personnes et prestataires qui en ont besoin
          pour assurer le fonctionnement du service ou répondre à votre
          demande.
        </p>

        <ul class="PlainList">
          <li>
            PixelProwlers et les personnes expressément autorisées dans le
            cadre de la demande ou de la mission.
          </li>
          <li>
            Hostinger, pour l’hébergement du site et de son infrastructure.
          </li>
          <li>
            Brevo, lorsque l’envoi d’un message transactionnel ou de suivi
            nécessite son service de messagerie.
          </li>
          <li>
            Les prestataires techniques indispensables à une mission, lorsque
            leur intervention est prévue et encadrée.
          </li>
          <li>
            Les autorités ou organismes légalement habilités, uniquement
            lorsqu’une obligation juridique l’impose.
          </li>
        </ul>

        <p class="SectionText">
          PixelProwlers ne vend ni ne loue vos données personnelles.
        </p>
      </div>
    </section>

    <section class="PrivacySection" aria-labelledby="transfers-title">
      <div class="article-container">
        <p class="eyebrow">Localisation des données</p>

        <h2 id="transfers-title">
          Transferts en dehors de l’Espace économique européen
        </h2>

        <p class="SectionText">
          PixelProwlers privilégie des traitements et prestataires établis
          dans l’Espace économique européen.
        </p>

        <p class="SectionText">
          Lorsqu’un prestataire implique un transfert hors de cet espace,
          PixelProwlers vérifie l’existence d’un mécanisme reconnu par la
          réglementation applicable, tel qu’une décision d’adéquation ou des
          clauses contractuelles types. Les informations disponibles sur ces
          garanties peuvent être demandées à
          <a :href="`mailto:${dataController.email}`">
            {{ dataController.email }}
          </a>.
        </p>
      </div>
    </section>

    <section
      class="PrivacySection PrivacySectionAlt"
      aria-labelledby="trackers-title"
    >
      <div class="article-container">
        <p class="eyebrow">Cookies et stockage local</p>

        <h2 id="trackers-title">
          Aucun suivi publicitaire ou analytique tiers
        </h2>

        <p class="SectionText">
          À la date de mise à jour de cette politique, PixelProwlers n’utilise
          pas de service publicitaire, de profilage ni d’outil d’analyse
          d’audience tiers sur ce site.
        </p>

        <p class="SectionText">
          Le site peut utiliser le stockage de session du navigateur
          (<code>sessionStorage</code>) pour conserver temporairement l’état
          fonctionnel d’un parcours ou d’un formulaire. Ces informations
          restent dans le navigateur pendant la session et ne servent pas à
          suivre votre activité sur d’autres sites.
        </p>

        <p class="SectionText">
          Si un outil non strictement nécessaire devait être ajouté, cette
          politique et le mécanisme de recueil du consentement seraient adaptés
          avant son activation.
        </p>
      </div>
    </section>

    <section class="PrivacySection" aria-labelledby="automation-title">
      <div class="article-container">
        <p class="eyebrow">Pré-diagnostic</p>

        <h2 id="automation-title">
          Pas de décision produisant un effet juridique automatisé
        </h2>

        <p class="SectionText">
          Les réponses fournies dans le pré-diagnostic peuvent produire une
          orientation ou un niveau de priorité indicatif. Ce résultat ne
          constitue ni une décision juridique, ni un engagement contractuel,
          ni une garantie de résolution.
        </p>

        <p class="SectionText">
          Lorsqu’une intervention humaine est demandée, la situation est
          qualifiée avant toute proposition ou action sensible.
        </p>
      </div>
    </section>

    <section
      class="PrivacySection PrivacySectionAlt"
      aria-labelledby="security-title"
    >
      <div class="article-container">
        <p class="eyebrow">Sécurité</p>

        <h2 id="security-title">
          Comment les données sont-elles protégées ?
        </h2>

        <p class="SectionText">
          PixelProwlers applique des mesures proportionnées aux risques,
          notamment la limitation des accès, le chiffrement des communications,
          la séparation des environnements, la journalisation utile à la
          sécurité et la mise à jour des composants.
        </p>

        <p class="SectionText">
          Aucun système ne peut être présenté comme totalement infaillible. En
          cas d’incident susceptible d’affecter vos données, PixelProwlers
          applique les obligations d’analyse, de notification et d’information
          prévues par la réglementation.
        </p>

        <div class="SecurityWarning">
          <h3>Ne transmettez aucun secret dans les formulaires</h3>

          <p>
            N’envoyez pas de mot de passe, token, clé privée, cookie de session,
            sauvegarde, accès administrateur ou document contenant des données
            sensibles. Si un accès devient nécessaire, ses modalités seront
            définies après qualification.
          </p>
        </div>
      </div>
    </section>

    <section class="PrivacySection" aria-labelledby="rights-title">
      <div class="article-container">
        <p class="eyebrow">Vos droits</p>

        <h2 id="rights-title">
          Vous gardez la maîtrise de vos données
        </h2>

        <p class="SectionText">
          Selon le traitement concerné et les conditions prévues par la
          réglementation, vous pouvez exercer les droits suivants :
        </p>

        <ul class="RightsList">
          <li v-for="right in dataRights" :key="right.title">
            <h3>{{ right.title }}</h3>
            <p>{{ right.text }}</p>
          </li>
        </ul>

        <div class="RightsContact">
          <h3>Exercer un droit</h3>

          <p>
            Envoyez votre demande à
            <a :href="`mailto:${dataController.email}`">
              {{ dataController.email }}
            </a>
            en précisant le droit concerné et les informations permettant
            d’identifier la demande.
          </p>

          <p>
            Une preuve d’identité n’est demandée qu’en cas de doute raisonnable
            sur l’identité du demandeur. PixelProwlers répond en principe dans
            un délai d’un mois. Ce délai peut être prolongé lorsque la demande
            est complexe ou multiple, conformément à la réglementation.
          </p>

          <p>
            Si vous estimez que vos droits ne sont pas respectés, vous pouvez
            introduire une réclamation auprès de la
            <a
              href="https://www.cnil.fr/fr/plaintes"
              target="_blank"
              rel="noopener noreferrer"
            >
              Commission nationale de l’informatique et des libertés
            </a>.
          </p>
        </div>
      </div>
    </section>

    <section
      class="PrivacySection PrivacySectionAlt"
      aria-labelledby="updates-title"
    >
      <div class="article-container">
        <p class="eyebrow">Évolution du document</p>

        <h2 id="updates-title">
          Mise à jour de cette politique
        </h2>

        <p class="SectionText">
          Cette politique peut évoluer lorsque les formulaires, prestataires
          ou traitements changent. La date affichée en haut de cette page
          permet d’identifier la version applicable.
        </p>

        <p class="SectionText">
          Toute évolution substantielle affectant la manière dont les données
          sont utilisées fera l’objet d’une information adaptée.
        </p>
      </div>
    </section>

    <section class="PrivacyContact" aria-labelledby="privacy-contact-title">
      <div class="article-container">
        <p class="eyebrow PrivacyEyebrow">Une question ?</p>

        <h2 id="privacy-contact-title">
          Parlons de vos données avant de les collecter.
        </h2>

        <p>
          Pour toute question relative à cette politique ou à l’utilisation de
          vos données, contactez PixelProwlers.
        </p>

        <a
          class="ContactButton"
          :href="`mailto:${dataController.email}`"
        >
          {{ dataController.email }}
        </a>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
const dataController = {
  legalName: "Grégory Catteau",
  postalAddress:
    "BP 10023, 102 rue Joseph et François Connord, 33341 Lesparre Cedex, France",
  email: "contact@pixelprowlers.io",
} as const;

const privacyPrinciples = [
  {
    title: "Finalité déterminée",
    text: "Les données sont collectées pour répondre à une demande identifiée ou assurer une fonction précise.",
  },
  {
    title: "Collecte proportionnée",
    text: "Les formulaires doivent demander uniquement les informations nécessaires à leur objectif.",
  },
  {
    title: "Durée limitée",
    text: "Les données ne sont pas conservées sans limite et font l’objet de règles de suppression ou d’archivage.",
  },
  {
    title: "Accès contrôlé",
    text: "L’accès aux données est limité aux personnes et prestataires qui en ont besoin.",
  },
] as const;

const processingActivities = [
  {
    title: "Contact, rendez-vous et demandes commerciales",
    data: "Nom ou organisation, adresse électronique, numéro de téléphone obligatoire, type de demande, message et préférences de contact.",
    purpose: "Répondre à la demande, qualifier le besoin, organiser un échange et préparer une éventuelle proposition.",
    legalBasis: "Mesures précontractuelles prises à votre demande. L’intérêt légitime peut s’appliquer au suivi d’une demande professionnelle qui ne débouche pas immédiatement sur un contrat.",
    recipients: "PixelProwlers, l’hébergeur et le prestataire de messagerie lorsqu’un message transactionnel doit être envoyé.",
    retention: "Jusqu’à trois ans après le dernier échange actif pour un prospect, sauf opposition ou obligation justifiant une durée différente.",
  },
  {
    title: "Pré-diagnostic numérique",
    data: "Réponses au questionnaire, organisation, adresse électronique, téléphone facultatif, message et résultat d’orientation.",
    purpose: "Produire une orientation indicative, transmettre le résultat demandé et permettre une qualification humaine.",
    legalBasis: "Mesures précontractuelles prises à votre demande.",
    recipients: "PixelProwlers, l’hébergeur et le prestataire de messagerie utilisé pour transmettre le résultat.",
    retention: "Jusqu’à trois ans après le dernier échange actif, sauf demande de suppression ou transformation en relation contractuelle.",
  },
  {
    title: "Demandes urgentes et incidents",
    data: "Identité, organisation, coordonnées, URL concernée, description de l’incident, impact, horaire et préférence de rappel.",
    purpose: "Qualifier l’urgence, limiter les risques, reprendre contact et organiser une éventuelle intervention.",
    legalBasis: "Mesures précontractuelles prises à votre demande et intérêt légitime à assurer la sécurité et la traçabilité des échanges.",
    recipients: "PixelProwlers et, lorsque cela est nécessaire et autorisé, les intervenants techniques concernés.",
    retention: "Les informations opérationnelles sont conservées pendant le traitement puis archivées pour la durée nécessaire à la preuve et au suivi, dans la limite de cinq ans lorsqu’un risque contentieux le justifie.",
  },
  {
    title: "Gestion des clients et des prestations",
    data: "Identité, coordonnées, organisation, échanges, devis, contrats, livrables, informations de facturation et suivi des interventions.",
    purpose: "Exécuter la prestation, assurer son suivi, gérer la facturation, la comptabilité et les obligations associées.",
    legalBasis: "Exécution du contrat et respect des obligations légales.",
    recipients: "PixelProwlers, les prestataires indispensables à la mission, les services comptables et les autorités légalement habilitées.",
    retention: "Pendant la relation contractuelle, puis jusqu’à cinq ans pour les documents utiles à la preuve. Les pièces comptables sont conservées pendant dix ans.",
  },
  {
    title: "Sécurité du site et prévention des abus",
    data: "Adresse IP, date et heure, route demandée, informations techniques du navigateur, événements de sécurité et données nécessaires à la limitation des abus.",
    purpose: "Protéger le site, détecter les erreurs, prévenir les soumissions automatisées et analyser les incidents.",
    legalBasis: "Intérêt légitime de PixelProwlers à sécuriser son infrastructure et ses services.",
    recipients: "PixelProwlers et l’hébergeur technique.",
    retention: "Durée proportionnée au besoin de sécurité, avec un objectif maximal de douze mois sauf incident nécessitant une conservation plus longue et justifiée.",
  },
  {
    title: "Messages transactionnels",
    data: "Adresse électronique, identité, référence de dossier, statut d’envoi et contenu strictement nécessaire au message.",
    purpose: "Confirmer une demande, transmettre une référence ou informer sur le suivi d’un dossier.",
    legalBasis: "Mesures précontractuelles ou exécution du contrat, selon la nature du message.",
    recipients: "PixelProwlers et Brevo en qualité de prestataire d’envoi.",
    retention: "Pendant la durée nécessaire à l’envoi, au suivi et à la preuve du message, dans les limites configurées auprès du prestataire.",
  },
] as const;

const dataRights = [
  {
    title: "Accès",
    text: "Obtenir la confirmation qu’un traitement existe et recevoir une copie des données concernées.",
  },
  {
    title: "Rectification",
    text: "Faire corriger des données inexactes ou compléter des informations devenues incomplètes.",
  },
  {
    title: "Effacement",
    text: "Demander la suppression des données lorsque les conditions réglementaires sont réunies.",
  },
  {
    title: "Limitation",
    text: "Demander le gel temporaire de l’utilisation des données dans certaines situations.",
  },
  {
    title: "Opposition",
    text: "Vous opposer à un traitement fondé sur l’intérêt légitime pour des raisons tenant à votre situation.",
  },
  {
    title: "Portabilité",
    text: "Recevoir les données fournies dans un format structuré lorsque ce droit est applicable.",
  },
  {
    title: "Retrait du consentement",
    text: "Retirer votre consentement à tout moment lorsqu’un traitement repose effectivement sur cette base légale.",
  },
] as const;

const pageDescription =
  "Consultez la politique de confidentialité de PixelProwlers : données collectées, finalités, conservation, destinataires et exercice de vos droits.";

useSeoMeta({
  title: "Politique de confidentialité — PixelProwlers",
  description: pageDescription,
  robots: "index, follow",
  ogTitle: "Politique de confidentialité — PixelProwlers",
  ogDescription: pageDescription,
  ogType: "website",
  ogUrl: "https://pixelprowlers.io/confidentialite",
});

useHead({
  link: [
    {
      rel: "canonical",
      href: "https://pixelprowlers.io/confidentialite",
    },
  ],
});
</script>

<style scoped>
@reference "../assets/css/main.css";

.PrivacyPage {
  @apply bg-pxp-panel text-pxp-ink;
}

.PrivacyHero {
  @apply border-b border-pxp-green/15 bg-pxp-paper py-16;
}

.PrivacyHero h1 {
  @apply mt-4 text-4xl font-black leading-tight tracking-tight text-pxp-ink;
}

.BackLink {
  @apply mb-10 inline-flex rounded-md font-bold text-pxp-green underline decoration-pxp-green/30 underline-offset-4 transition hover:decoration-pxp-green focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-pxp-green;
}

.PrivacyIntroduction {
  @apply mt-6 text-lg leading-8 text-pxp-ink/80;
}

.PrivacyDate {
  @apply mt-5 text-sm font-bold text-pxp-green;
}

.PrivacySection {
  @apply border-b border-pxp-green/10 bg-pxp-panel py-16;
}

.PrivacySectionAlt {
  @apply bg-pxp-paper;
}

.PrivacySection h2,
.PrivacyContact h2 {
  @apply mt-4 text-3xl font-black leading-tight tracking-tight text-pxp-ink;
}

.SectionText {
  @apply mt-5 leading-8 text-pxp-ink/80;
}

.SectionText a,
.IdentityCard a,
.RightsContact a {
  @apply rounded-sm font-bold text-pxp-green underline decoration-pxp-green/30 underline-offset-4 transition hover:decoration-pxp-green focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-pxp-green;
}

.IdentityCard {
  @apply mt-8 rounded-lg border border-pxp-green/15 bg-white p-6 shadow-sm;
}

.IdentityCard dl {
  @apply grid gap-6;
}

.IdentityCard dl div {
  @apply border-b border-pxp-green/10 pb-5 last:border-b-0 last:pb-0;
}

.IdentityCard dt,
.ProcessingCard dt {
  @apply text-sm font-black uppercase tracking-wide text-pxp-green;
}

.IdentityCard dd,
.ProcessingCard dd {
  @apply mt-2 leading-7 text-pxp-ink/80;
}

.PrinciplesGrid {
  @apply mt-10 grid gap-5;
}

.PrincipleCard {
  @apply rounded-lg border border-pxp-green/15 bg-pxp-panel p-6;
}

.PrincipleCard h3 {
  @apply text-xl font-black text-pxp-ink;
}

.PrincipleCard p {
  @apply mt-3 leading-7 text-pxp-ink/75;
}

.SectionHeading {
  @apply max-w-3xl;
}

.SectionHeading h2 {
  @apply mt-4 text-3xl font-black leading-tight tracking-tight;
}

.SectionHeading > p:last-child {
  @apply mt-5 text-lg leading-8 text-pxp-ink/75;
}

.ProcessingGrid {
  @apply mt-10 grid gap-6;
}

.ProcessingCard {
  @apply rounded-lg border border-pxp-green/15 bg-white p-6 shadow-sm;
}

.ProcessingCard h3 {
  @apply text-2xl font-black leading-tight text-pxp-ink;
}

.ProcessingCard dl {
  @apply mt-6 grid gap-5;
}

.ProcessingCard dl div {
  @apply border-t border-pxp-green/10 pt-5;
}

.PlainList,
.RightsList {
  @apply mt-8 space-y-4;
}

.PlainList li {
  @apply relative m-0 border-0 bg-transparent py-0 pl-7 pr-0 font-normal leading-8 text-pxp-ink/80;
}

.PlainList li::before {
  @apply absolute left-0 top-0 font-black text-pxp-green;
  content: "✓";
}

.SecurityWarning {
  @apply mt-8 rounded-lg border border-pxp-orange/30 bg-white p-6;
}

.SecurityWarning h3 {
  @apply text-xl font-black text-pxp-ink;
}

.SecurityWarning p {
  @apply mt-3 leading-7 text-pxp-ink/80;
}

.RightsList li {
  @apply m-0 rounded-lg border border-pxp-green/15 bg-white p-5;
}

.RightsList h3 {
  @apply text-lg font-black text-pxp-ink;
}

.RightsList p {
  @apply mt-2 font-normal leading-7 text-pxp-ink/75;
}

.RightsContact {
  @apply mt-8 rounded-lg border border-pxp-green/20 bg-primary-50 p-6;
}

.RightsContact h3 {
  @apply text-xl font-black text-pxp-ink;
}

.RightsContact p {
  @apply mt-4 leading-7 text-pxp-ink/80;
}

.PrivacyContact {
  @apply bg-pxp-blue py-16 text-white;
}

.PrivacyContact h2 {
  @apply text-white;
}

.PrivacyEyebrow {
  @apply text-primary-100;
}

.PrivacyContact p {
  @apply mt-5 text-lg leading-8 text-white/75;
}

.ContactButton {
  @apply mt-8 inline-flex min-h-12 items-center justify-center rounded-lg bg-white px-6 py-3 font-black text-pxp-blue transition hover:bg-primary-50 focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-white;
}

@media (min-width: 768px) {
  .PrivacyHero,
  .PrivacySection,
  .PrivacyContact {
    @apply py-24;
  }

  .PrivacyHero h1 {
    @apply text-6xl;
  }

  .PrivacySection h2,
  .PrivacyContact h2,
  .SectionHeading h2 {
    @apply text-4xl;
  }

  .PrinciplesGrid,
  .ProcessingGrid,
  .RightsList {
    @apply grid-cols-2;
  }

  .IdentityCard dl {
    @apply grid-cols-2;
  }

  .RightsList {
    @apply grid gap-4 space-y-0;
  }
}
</style>