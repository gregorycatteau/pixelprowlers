<template>
  <main class="LegalPage">
    <section class="LegalHero" aria-labelledby="legal-title">
      <div class="article-container">
        <NuxtLink to="/" class="BackLink">
          Retour à l’accueil
        </NuxtLink>

        <p class="eyebrow">Informations légales</p>

        <h1 id="legal-title">
          Mentions légales
        </h1>

        <p class="LegalIntroduction">
          Cette page présente l’identité de l’éditeur, les coordonnées de
          l’hébergeur et les principales règles applicables à l’utilisation
          du site PixelProwlers.
        </p>

        <p class="LegalDate">
          Dernière mise à jour :
          <time datetime="2026-07-17">17 juillet 2026</time>
        </p>
      </div>
    </section>

    <section class="LegalSection" aria-labelledby="publisher-title">
      <div class="article-container">
        <p class="eyebrow">Éditeur</p>

        <h2 id="publisher-title">
          Édition et responsabilité de publication
        </h2>

        <div class="LegalIdentityCard">
          <dl>
            <div>
              <dt>Nom commercial</dt>
              <dd>{{ publisher.tradeName }}</dd>
            </div>

            <div>
              <dt>Éditeur et responsable de publication</dt>
              <dd>{{ publisher.legalName }}</dd>
            </div>

            <div>
              <dt>Statut juridique</dt>
              <dd>{{ publisher.legalStatus }}</dd>
            </div>

            <div>
              <dt>Adresse postale professionnelle</dt>
              <dd>{{ publisher.postalAddress }}</dd>
            </div>

            <div>
              <dt>SIREN</dt>
              <dd>{{ publisher.siren }}</dd>
            </div>

            <div>
              <dt>SIRET</dt>
              <dd>{{ publisher.siret }}</dd>
            </div>

            <div>
              <dt>Immatriculation</dt>
              <dd>{{ publisher.registrationRegistry }}</dd>
            </div>

            <div>
              <dt>TVA</dt>
              <dd>{{ publisher.vatStatus }}</dd>
            </div>

            <div>
              <dt>Adresse électronique</dt>
              <dd>
                <a :href="`mailto:${publisher.email}`">
                  {{ publisher.email }}
                </a>
              </dd>
            </div>

            <div>
              <dt>Téléphone professionnel</dt>
              <dd>
                <a :href="publisher.phoneHref">
                  {{ publisher.phoneDisplay }}
                </a>
              </dd>
            </div>

            <div>
              <dt>Nom de domaine officiel</dt>
              <dd>
                <a
                  href="https://pixelprowlers.io"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  pixelprowlers.io
                </a>
              </dd>
            </div>
          </dl>
        </div>

        <p class="LegalText">
          PixelProwlers est le nom commercial sous lequel Grégory Catteau
          exerce son activité professionnelle.
        </p>
      </div>
    </section>

    <section
      class="LegalSection LegalSectionAlt"
      aria-labelledby="hosting-title"
    >
      <div class="article-container">
        <p class="eyebrow">Hébergement</p>

        <h2 id="hosting-title">
          Hébergeur du site
        </h2>

        <div class="HostingCard">
          <dl>
            <div>
              <dt>Prestataire</dt>
              <dd>{{ hostingProvider.legalEntity }}</dd>
            </div>

            <div>
              <dt>Service utilisé</dt>
              <dd>{{ hostingProvider.service }}</dd>
            </div>

            <div>
              <dt>Adresse</dt>
              <dd>{{ hostingProvider.postalAddress }}</dd>
            </div>

            <div>
              <dt>Numéro de TVA de l’hébergeur</dt>
              <dd>{{ hostingProvider.vatNumber }}</dd>
            </div>

            <div>
              <dt>Site internet</dt>
              <dd>
                <a
                  :href="hostingProvider.website"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  hostinger.fr
                </a>
              </dd>
            </div>

            <div>
              <dt>Assistance et contact</dt>
              <dd>
                <a
                  :href="hostingProvider.contactUrl"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Service de contact Hostinger
                </a>
              </dd>
            </div>
          </dl>
        </div>

        <p class="LegalText">
          Le site et ses services applicatifs sont exploités sur un serveur
          privé virtuel fourni par Hostinger.
        </p>
      </div>
    </section>

    <section class="LegalSection" aria-labelledby="access-title">
      <div class="article-container">
        <p class="eyebrow">Accès au site</p>

        <h2 id="access-title">
          Disponibilité et maintenance
        </h2>

        <p class="LegalText">
          PixelProwlers met en œuvre des moyens raisonnables pour assurer
          l’accès au site, sa sécurité et son bon fonctionnement. Une
          disponibilité permanente ou exempte de toute erreur ne peut
          toutefois pas être garantie.
        </p>

        <p class="LegalText">
          L’accès peut être temporairement interrompu pour une opération de
          maintenance, une mise à jour, un incident technique ou une mesure de
          sécurité. Lorsque cela est raisonnablement possible, PixelProwlers
          limite la durée et les conséquences de ces interruptions.
        </p>
      </div>
    </section>

    <section
      class="LegalSection LegalSectionAlt"
      aria-labelledby="content-title"
    >
      <div class="article-container">
        <p class="eyebrow">Contenus</p>

        <h2 id="content-title">
          Informations publiées
        </h2>

        <p class="LegalText">
          Les contenus du site présentent les activités, méthodes et services
          de PixelProwlers. Ils sont fournis à titre informatif et ne
          constituent pas, à eux seuls, une proposition contractuelle, un
          diagnostic définitif ou une garantie de résultat.
        </p>

        <p class="LegalText">
          Une intervention, un délai, un livrable ou un prix ne devient
          contractuel qu’après validation explicite du périmètre et des
          conditions applicables.
        </p>

        <p class="LegalText">
          PixelProwlers s’efforce de maintenir les informations à jour. Une
          erreur ou une information devenue obsolète peut être signalée à
          <a :href="`mailto:${publisher.email}`">
            {{ publisher.email }}
          </a>.
        </p>
      </div>
    </section>

    <section class="LegalSection" aria-labelledby="security-title">
      <div class="article-container">
        <p class="eyebrow">Sécurité numérique</p>

        <h2 id="security-title">
          Informations et pré-diagnostics de sécurité
        </h2>

        <p class="LegalText">
          Les informations de sécurité et résultats de pré-diagnostic
          disponibles sur le site constituent une première orientation. Ils
          ne remplacent pas une analyse humaine, un audit formel ou une
          intervention contractuellement définie.
        </p>

        <p class="LegalText">
          Toute vérification de sécurité est limitée aux systèmes appartenant
          au demandeur ou pour lesquels il dispose d’une autorisation
          explicite. Aucun test intrusif n’est engagé à partir d’une simple
          soumission de formulaire.
        </p>

        <div class="SecurityNotice">
          <h3>Ne transmettez aucun secret</h3>

          <p>
            Les formulaires ne doivent contenir aucun mot de passe, token,
            cookie de session, clé privée, sauvegarde, accès administrateur
            ou document sensible.
          </p>
        </div>
      </div>
    </section>

    <section
      class="LegalSection LegalSectionAlt"
      aria-labelledby="intellectual-property-title"
    >
      <div class="article-container">
        <p class="eyebrow">Propriété intellectuelle</p>

        <h2 id="intellectual-property-title">
          Textes, identité et éléments graphiques
        </h2>

        <p class="LegalText">
          Sauf indication contraire, la structure du site, les textes, le nom
          PixelProwlers, les éléments graphiques, les illustrations et les
          contenus originaux sont protégés par les règles applicables à la
          propriété intellectuelle.
        </p>

        <p class="LegalText">
          Toute reproduction, adaptation, représentation ou réutilisation
          substantielle nécessite une autorisation préalable, sauf lorsqu’une
          licence distincte ou une exception légale l’autorise.
        </p>

        <p class="LegalText">
          Les marques, logiciels, bibliothèques et contenus appartenant à des
          tiers restent soumis à leurs droits et licences respectifs.
        </p>
      </div>
    </section>

    <section class="LegalSection" aria-labelledby="links-title">
      <div class="article-container">
        <p class="eyebrow">Liens externes</p>

        <h2 id="links-title">
          Sites et services tiers
        </h2>

        <p class="LegalText">
          Le site peut contenir des liens vers des ressources externes.
          PixelProwlers ne contrôle pas en permanence leur disponibilité, leur
          contenu ou leurs pratiques de confidentialité.
        </p>

        <p class="LegalText">
          L’utilisateur reste invité à consulter les conditions et politiques
          applicables au service tiers avant de lui transmettre des données.
        </p>
      </div>
    </section>

    <section
      class="LegalSection LegalSectionAlt"
      aria-labelledby="privacy-title"
    >
      <div class="article-container">
        <p class="eyebrow">Données personnelles</p>

        <h2 id="privacy-title">
          Protection de vos données
        </h2>

        <p class="LegalText">
          Les informations relatives aux données collectées, aux finalités,
          aux bases légales, aux destinataires, aux durées de conservation et
          à l’exercice de vos droits sont présentées dans la politique de
          confidentialité.
        </p>

        <NuxtLink class="LegalButton" to="/confidentialite">
          Consulter la politique de confidentialité
        </NuxtLink>
      </div>
    </section>

    <section class="LegalSection" aria-labelledby="mediation-title">
      <div class="article-container">
        <p class="eyebrow">Consommateurs</p>

        <h2 id="mediation-title">
          Médiation de la consommation
        </h2>

        <p class="LegalText">
          En cas de litige, le client consommateur doit d’abord adresser une
          réclamation écrite à PixelProwlers afin de rechercher une solution
          amiable.
        </p>

        <p class="LegalText">
          Si cette démarche n’aboutit pas, le consommateur peut saisir
          gratuitement le médiateur de la consommation dont relève
          PixelProwlers :
        </p>

        <div class="MediationCard">
          <dl>
            <div>
              <dt>Médiateur</dt>
              <dd>{{ consumerMediator.name }}</dd>
            </div>

            <div>
              <dt>Adresse</dt>
              <dd>{{ consumerMediator.postalAddress }}</dd>
            </div>

            <div>
              <dt>Adresse électronique</dt>
              <dd>
                <a :href="`mailto:${consumerMediator.email}`">
                  {{ consumerMediator.email }}
                </a>
              </dd>
            </div>

            <div>
              <dt>Site internet</dt>
              <dd>
                <a
                  :href="consumerMediator.website"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  mediateur-consommation-smp.fr
                </a>
              </dd>
            </div>
          </dl>
        </div>

        <p class="LegalText">
          La médiation ne peut être sollicitée qu’après une réclamation écrite
          préalable auprès de PixelProwlers et dans les conditions prévues par
          le règlement du médiateur.
        </p>
      </div>
    </section>

    <section
      class="LegalSection LegalSectionAlt"
      aria-labelledby="law-title"
    >
      <div class="article-container">
        <p class="eyebrow">Droit applicable</p>

        <h2 id="law-title">
          Réclamations et litiges
        </h2>

        <p class="LegalText">
          Les présentes mentions légales sont soumises au droit français, sous
          réserve des règles impératives éventuellement applicables.
        </p>

        <p class="LegalText">
          Avant toute procédure, les parties sont invitées à rechercher une
          solution amiable en écrivant à
          <a :href="`mailto:${publisher.email}`">
            {{ publisher.email }}
          </a>.
        </p>

        <p class="LegalText">
          La juridiction compétente est déterminée conformément aux règles
          légales applicables. Aucune clause ne peut priver un consommateur des
          protections impératives dont il bénéficie.
        </p>
      </div>
    </section>

    <section class="LegalContact" aria-labelledby="legal-contact-title">
      <div class="article-container">
        <p class="eyebrow LegalEyebrow">Contact</p>

        <h2 id="legal-contact-title">
          Signaler une erreur ou demander une information
        </h2>

        <p>
          Pour toute question concernant le site ou ces mentions légales,
          contactez directement PixelProwlers.
        </p>

        <div class="ContactActions">
          <a
            class="ContactButton"
            :href="`mailto:${publisher.email}`"
          >
            {{ publisher.email }}
          </a>

          <a
            class="ContactButton ContactButtonSecondary"
            :href="publisher.phoneHref"
          >
            {{ publisher.phoneDisplay }}
          </a>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
const publisher = {
  tradeName: "PixelProwlers",
  legalName: "Grégory Catteau",
  legalStatus:
    "Entrepreneur individuel sous le régime de la micro-entreprise",
  postalAddress:
    "BP 10023, 102 rue Joseph et François Connord, 33341 Lesparre Cedex, France",
  siren: "520 890 336",
  siret: "520 890 336 00065",
  registrationRegistry:
    "Registre national des entreprises — RCS de Bordeaux, numéro 520 890 336",
  vatStatus: "TVA non applicable, article 293 B du Code général des impôts",
  email: "contact@pixelprowlers.io",
  phoneDisplay: "06 68 14 51 52",
  phoneHref: "tel:+33668145152",
} as const;

const hostingProvider = {
  legalEntity: "Hostinger International Ltd.",
  service: "Serveur privé virtuel — VPS",
  postalAddress:
    "61 Lordou Vironos Street, 6023 Larnaca, Chypre",
  vatNumber: "CY10301365E",
  website: "https://www.hostinger.fr/",
  contactUrl: "https://www.hostinger.fr/contact",
} as const;

const consumerMediator = {
  name:
    "Société de la Médiation Professionnelle — Médiation de la consommation",
  postalAddress:
    "24 rue Albert de Mun, 33000 Bordeaux, France",
  email: "contact@smpmediation.fr",
  website: "https://www.mediateur-consommation-smp.fr/",
} as const;

const pageDescription =
  "Consultez les mentions légales de PixelProwlers : éditeur, responsable de publication, hébergement, médiation et contact.";

useSeoMeta({
  title: "Mentions légales — PixelProwlers",
  description: pageDescription,
  robots: "index, follow",
  ogTitle: "Mentions légales — PixelProwlers",
  ogDescription: pageDescription,
  ogType: "website",
  ogUrl: "https://pixelprowlers.io/mentions-legales",
});

useHead({
  link: [
    {
      rel: "canonical",
      href: "https://pixelprowlers.io/mentions-legales",
    },
  ],
});
</script>

<style scoped>
@reference "../assets/css/main.css";

.LegalPage {
  @apply bg-pxp-panel text-pxp-ink;
}

.LegalHero {
  @apply border-b border-pxp-green/15 bg-pxp-paper py-16;
}

.LegalHero h1 {
  @apply mt-4 text-4xl font-black leading-tight tracking-tight text-pxp-ink;
}

.BackLink {
  @apply mb-10 inline-flex rounded-md font-bold text-pxp-green underline decoration-pxp-green/30 underline-offset-4 transition hover:decoration-pxp-green focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-pxp-green;
}

.LegalIntroduction {
  @apply mt-6 text-lg leading-8 text-pxp-ink/80;
}

.LegalDate {
  @apply mt-5 text-sm font-bold text-pxp-green;
}

.LegalSection {
  @apply border-b border-pxp-green/10 bg-pxp-panel py-16;
}

.LegalSectionAlt {
  @apply bg-pxp-paper;
}

.LegalSection h2,
.LegalContact h2 {
  @apply mt-4 text-3xl font-black leading-tight tracking-tight text-pxp-ink;
}

.LegalText {
  @apply mt-5 leading-8 text-pxp-ink/80;
}

.LegalText a,
.LegalIdentityCard a,
.HostingCard a,
.MediationCard a {
  @apply rounded-sm font-bold text-pxp-green underline decoration-pxp-green/30 underline-offset-4 transition hover:decoration-pxp-green focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-pxp-green;
}

.LegalIdentityCard,
.HostingCard,
.MediationCard {
  @apply mt-8 rounded-lg border border-pxp-green/15 bg-white p-6 shadow-sm;
}

.LegalIdentityCard dl,
.HostingCard dl,
.MediationCard dl {
  @apply grid gap-6;
}

.LegalIdentityCard dl div,
.HostingCard dl div,
.MediationCard dl div {
  @apply border-b border-pxp-green/10 pb-5 last:border-b-0 last:pb-0;
}

.LegalIdentityCard dt,
.HostingCard dt,
.MediationCard dt {
  @apply text-sm font-black uppercase tracking-wide text-pxp-green;
}

.LegalIdentityCard dd,
.HostingCard dd,
.MediationCard dd {
  @apply mt-2 leading-7 text-pxp-ink/80;
}

.SecurityNotice {
  @apply mt-8 rounded-lg border border-pxp-orange/30 bg-white p-6;
}

.SecurityNotice h3 {
  @apply text-xl font-black text-pxp-ink;
}

.SecurityNotice p {
  @apply mt-3 leading-7 text-pxp-ink/80;
}

.LegalButton {
  @apply mt-8 inline-flex min-h-12 items-center justify-center rounded-lg bg-pxp-green px-6 py-3 font-black text-white transition hover:bg-primary-900 focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-pxp-green;
}

.LegalContact {
  @apply bg-pxp-blue py-16 text-white;
}

.LegalContact h2 {
  @apply text-white;
}

.LegalEyebrow {
  @apply text-primary-100;
}

.LegalContact p {
  @apply mt-5 text-lg leading-8 text-white/75;
}

.ContactActions {
  @apply mt-8 flex flex-col gap-3;
}

.ContactButton {
  @apply inline-flex min-h-12 items-center justify-center rounded-lg bg-white px-6 py-3 font-black text-pxp-blue transition hover:bg-primary-50 focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-white;
}

.ContactButtonSecondary {
  @apply border border-white/50 bg-transparent text-white hover:border-white hover:bg-white/10;
}

@media (min-width: 640px) {
  .ContactActions {
    @apply flex-row flex-wrap;
  }
}

@media (min-width: 768px) {
  .LegalHero,
  .LegalSection,
  .LegalContact {
    @apply py-24;
  }

  .LegalHero h1 {
    @apply text-6xl;
  }

  .LegalSection h2,
  .LegalContact h2 {
    @apply text-4xl;
  }

  .LegalIdentityCard dl,
  .HostingCard dl,
  .MediationCard dl {
    @apply grid-cols-2;
  }
}
</style>