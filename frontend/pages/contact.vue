<template>
  <main class="bg-paper text-ink">
    <section class="page-hero">
      <div class="container-site max-w-4xl text-center">
        <p class="eyebrow">Contact</p>
        <h1>Décrivez la situation, pas une demande floue.</h1>
        <p>
          Site cassé, sauvegardes inconnues, accès dispersés, WordPress vieillissant, matériel à fiabiliser :
          on commence par comprendre ce qui tient encore debout.
        </p>
      </div>
    </section>

    <section class="contact-section">
      <div class="container-site contact-grid">
        <aside class="diagnostic-note" aria-labelledby="contact-note-title">
          <p class="eyebrow">Cadre de l’échange</p>
          <h2 id="contact-note-title">Utile, confidentiel, sans promesse impossible.</h2>
          <p>
            Le premier échange sert à clarifier le besoin, les accès, les risques et le niveau d’urgence.
            N’envoyez pas de mot de passe, clé privée, cookie, sauvegarde complète ou donnée sensible via ce formulaire.
          </p>
          <p class="privacy-reminder">
            Ce formulaire sert à qualifier une demande. Il ne doit pas être utilisé pour transmettre des secrets,
            accès, mots de passe, tokens, clés privées ou archives de site.
          </p>

          <div class="note-block">
            <h3>Ce qui aide vraiment</h3>
            <ul>
              <li>URL du site et CMS si vous le connaissez</li>
              <li>Hébergeur, sauvegardes et accès disponibles</li>
              <li>Ce qui casse, inquiète ou dépend d’une seule personne</li>
            </ul>
          </div>

          <div class="note-block">
            <h3>Ce qu’on ne vend pas</h3>
            <ul>
              <li>Une sécurité totale garantie</li>
              <li>Un site “vite fait” sans maintenance</li>
              <li>Du bling-bling qui complique la reprise en main</li>
            </ul>
          </div>
        </aside>

        <form class="contact-form" novalidate @submit.prevent="submitForm">
          <div
            v-if="formErrors.length"
            ref="errorSummary"
            class="error-summary"
            tabindex="-1"
            role="alert"
            aria-labelledby="error-summary-title"
          >
            <h2 id="error-summary-title">À corriger avant l’envoi</h2>
            <ul>
              <li v-for="error in formErrors" :key="error">{{ error }}</li>
            </ul>
          </div>

          <div class="honeypot-field" aria-hidden="true">
            <label>
              <span>Site de votre entreprise</span>
              <input
                v-model="form.website_company"
                type="text"
                autocomplete="off"
                tabindex="-1"
              />
            </label>
          </div>

          <fieldset>
            <legend>Vous</legend>
            <div class="grid gap-6 md:grid-cols-2">
              <label class="block">
                <span>Votre nom</span>
                <input
                  v-model="form.name"
                  required
                  type="text"
                  autocomplete="name"
                  maxlength="160"
                  placeholder="Jean Dupont"
                  class="field"
                  :aria-invalid="Boolean(fieldErrors.name)"
                  aria-describedby="name-help"
                />
                <small id="name-help">Au moins 2 caractères.</small>
              </label>

              <label class="block">
                <span>Votre email</span>
                <input
                  v-model="form.email"
                  required
                  type="email"
                  autocomplete="email"
                  maxlength="254"
                  placeholder="jean@example.com"
                  class="field"
                  :aria-invalid="Boolean(fieldErrors.email)"
                />
              </label>

              <label class="block">
                <span>Structure</span>
                <input v-model="form.company" type="text" autocomplete="organization" maxlength="180" placeholder="Association, TPE, école..." class="field" />
              </label>

              <label class="block">
                <span>Téléphone</span>
                <input
                  v-model="form.phone"
                  type="tel"
                  autocomplete="tel"
                  maxlength="30"
                  placeholder="+33 6 XX XX XX XX"
                  class="field"
                  :aria-invalid="Boolean(fieldErrors.phone)"
                />
              </label>
            </div>
          </fieldset>

          <fieldset>
            <legend>Qualification</legend>
            <div class="grid gap-6 md:grid-cols-2">
              <label class="block">
                <span>Type de structure</span>
                <select v-model="form.structure_type" required class="field" :aria-invalid="Boolean(fieldErrors.structure_type)">
                  <option value="">Sélectionnez</option>
                  <option value="Association">Association</option>
                  <option value="TPE">TPE</option>
                  <option value="Indépendant">Indépendant</option>
                  <option value="École alternative">École alternative</option>
                  <option value="Collectif">Collectif</option>
                  <option value="Autre petite structure">Autre petite structure</option>
                </select>
              </label>

              <label class="block">
                <span>Besoin principal</span>
                <select v-model="form.service_type" required class="field" :aria-invalid="Boolean(fieldErrors.service_type)">
                  <option value="">Sélectionnez</option>
                  <option value="audit_site">Audit sécurité de site web</option>
                  <option value="site_maintenable">Site sobre, sécurisé, maintenable</option>
                  <option value="maintenance_documentation">Maintenance, accès et documentation</option>
                  <option value="materiel">Réparation ou reconditionnement</option>
                  <option value="formation">Formation et hygiène numérique</option>
                  <option value="urgence">Urgence : site cassé, piraté ou inaccessible</option>
                  <option value="autre">Autre</option>
                </select>
              </label>

              <label class="block">
                <span>Niveau d’urgence</span>
                <select v-model="form.urgency" required class="field" :aria-invalid="Boolean(fieldErrors.urgency)">
                  <option value="">Sélectionnez</option>
                  <option value="Urgent : activité bloquée">Urgent : activité bloquée</option>
                  <option value="À traiter rapidement">À traiter rapidement</option>
                  <option value="Prévention / diagnostic">Prévention / diagnostic</option>
                  <option value="Projet à cadrer">Projet à cadrer</option>
                </select>
              </label>

              <label class="block">
                <span>Préférence de contact</span>
                <select v-model="form.contact_preference" required class="field" :aria-invalid="Boolean(fieldErrors.contact_preference)">
                  <option value="">Sélectionnez</option>
                  <option value="Email">Email</option>
                  <option value="Téléphone">Téléphone</option>
                  <option value="Email puis appel si nécessaire">Email puis appel si nécessaire</option>
                </select>
              </label>
            </div>
          </fieldset>

          <fieldset>
            <legend>Contexte technique</legend>
            <div class="grid gap-6 md:grid-cols-2">
              <label class="block">
                <span>URL du site</span>
                <input
                  v-model="form.website_url"
                  type="url"
                  maxlength="240"
                  placeholder="https://example.org"
                  class="field"
                  :aria-invalid="Boolean(fieldErrors.website_url)"
                  aria-describedby="website-url-help"
                />
                <small id="website-url-help">Optionnel. N’ajoutez pas d’identifiant, token ou URL d’administration privée.</small>
              </label>

              <label class="block">
                <span>CMS si connu</span>
                <select v-model="form.cms" class="field">
                  <option value="">Je ne sais pas</option>
                  <option value="WordPress">WordPress</option>
                  <option value="Prestashop">Prestashop</option>
                  <option value="Drupal">Drupal</option>
                  <option value="Site statique">Site statique</option>
                  <option value="Nuxt / Vue">Nuxt / Vue</option>
                  <option value="Autre">Autre</option>
                </select>
              </label>

              <label class="block">
                <span>Hébergeur si connu</span>
                <input v-model="form.hosting" type="text" maxlength="120" placeholder="OVH, Infomaniak, o2switch..." class="field" />
              </label>

              <label class="block">
                <span>Sauvegardes connues ?</span>
                <select v-model="form.backups" required class="field" :aria-invalid="Boolean(fieldErrors.backups)">
                  <option value="">Sélectionnez</option>
                  <option value="Oui, restauration déjà testée">Oui, restauration déjà testée</option>
                  <option value="Oui, mais jamais testée">Oui, mais jamais testée</option>
                  <option value="Je ne sais pas">Je ne sais pas</option>
                  <option value="Probablement aucune">Probablement aucune</option>
                </select>
              </label>

              <label class="block">
                <span>Accès disponibles ?</span>
                <select v-model="form.access" required class="field" :aria-invalid="Boolean(fieldErrors.access)">
                  <option value="">Sélectionnez</option>
                  <option value="Oui, accès admin et hébergement">Oui, accès admin et hébergement</option>
                  <option value="Accès partiels">Accès partiels</option>
                  <option value="Je ne sais pas qui les a">Je ne sais pas qui les a</option>
                  <option value="Non">Non</option>
                </select>
              </label>

              <label class="block">
                <span>Budget indicatif optionnel</span>
                <select v-model="form.budget" class="field">
                  <option value="">Non précisé</option>
                  <option value="Moins de 500 €">Moins de 500 €</option>
                  <option value="500 à 1 500 €">500 à 1 500 €</option>
                  <option value="1 500 à 4 000 €">1 500 à 4 000 €</option>
                  <option value="Plus de 4 000 €">Plus de 4 000 €</option>
                  <option value="À cadrer ensemble">À cadrer ensemble</option>
                </select>
              </label>
            </div>
          </fieldset>

          <label class="mt-6 block">
            <span>Comment avez-vous connu PixelProwlers ?</span>
            <select v-model="form.found_us" class="field">
              <option value="">Non précisé</option>
              <option value="Recherche web">Recherche web</option>
              <option value="Bouche-à-oreille">Bouche-à-oreille</option>
              <option value="Réseau local">Réseau local</option>
              <option value="Ressources PixelProwlers">Ressources PixelProwlers</option>
              <option value="Autre">Autre</option>
            </select>
          </label>

          <label class="mt-6 block">
            <span>Décrivez votre situation</span>
            <textarea
              v-model="form.message"
              required
              rows="7"
              maxlength="4000"
              placeholder="Ce qui bloque, ce qui inquiète, ce qui doit changer. Ne collez pas de mot de passe ni de secret technique."
              class="field resize-y"
              :aria-invalid="Boolean(fieldErrors.message)"
              aria-describedby="message-help"
            ></textarea>
            <small id="message-help">
              Vous pouvez coller ici le résumé non sensible de votre diagnostic si vous le souhaitez.
              Si votre site est compromis, décrivez les symptômes sans envoyer d’identifiants ni de fichiers sensibles.
            </small>
          </label>

          <label class="consent-row">
            <input v-model="form.privacy_consent" required type="checkbox" />
            <span>
              J’accepte que PixelProwlers utilise ces informations pour me répondre. Je n’envoie pas de
              mot de passe, clé privée, cookie, sauvegarde complète ou donnée sensible via ce formulaire.
            </span>
          </label>

          <div v-if="statusMessage" :class="[
            'mt-6 rounded-lg border p-4 text-sm font-semibold',
            isSuccess ? 'border-forest/25 bg-forest/10 text-forest' : 'border-action/40 bg-action/10 text-ink'
          ]">
            {{ statusMessage }}
          </div>

          <button type="submit" :disabled="isSubmitting" class="submit-button">
            {{ isSubmitting ? 'Envoi en cours...' : 'Envoyer ma demande qualifiée' }}
          </button>
        </form>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { nextTick, ref } from 'vue';

const config = useRuntimeConfig();

usePixelSeo({
  title: 'Contact qualifié | PixelProwlers',
  description: 'Décrire une urgence, demander un audit site web ou cadrer une maintenance : formulaire qualifié PixelProwlers sans envoi de secrets.',
  path: '/contact',
});

type ContactForm = {
  name: string;
  email: string;
  company: string;
  phone: string;
  structure_type: string;
  service_type: string;
  urgency: string;
  contact_preference: string;
  website_url: string;
  cms: string;
  hosting: string;
  backups: string;
  access: string;
  budget: string;
  found_us: string;
  message: string;
  privacy_consent: boolean;
  website_company: string;
  started_at: number;
};

type FieldErrors = Partial<Record<keyof ContactForm, string>>;

// Crée l’état initial du formulaire de contact qualifié.
const createEmptyForm = (): ContactForm => ({
  name: '',
  email: '',
  company: '',
  phone: '',
  structure_type: '',
  service_type: '',
  urgency: '',
  contact_preference: '',
  website_url: '',
  cms: '',
  hosting: '',
  backups: '',
  access: '',
  budget: '',
  found_us: '',
  message: '',
  privacy_consent: false,
  website_company: '',
  started_at: Date.now(),
});

const form = ref<ContactForm>(createEmptyForm());
const isSubmitting = ref(false);
const statusMessage = ref('');
const isSuccess = ref(false);
const fieldErrors = ref<FieldErrors>({});
const formErrors = ref<string[]>([]);
const errorSummary = ref<HTMLElement | null>(null);

// Réinitialise le formulaire après une soumission réussie.
const resetForm = () => {
  form.value = createEmptyForm();
};

// Nettoie les champs texte avant validation et soumission.
const normalizeForm = () => {
  Object.entries(form.value).forEach(([key, value]) => {
    if (typeof value === 'string') {
      form.value[key as keyof ContactForm] = value.trim() as never;
    }
  });
};

// Vérifie localement les champs nécessaires pour éviter les demandes inexploitables.
const validateForm = () => {
  const errors: FieldErrors = {};

  if (form.value.name.length < 2) {
    errors.name = 'Indiquez votre nom avec au moins 2 caractères.';
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
    errors.email = 'Indiquez une adresse email valide.';
  }
  if (!form.value.structure_type) {
    errors.structure_type = 'Sélectionnez un type de structure.';
  }
  if (!form.value.service_type) {
    errors.service_type = 'Sélectionnez le besoin principal.';
  }
  if (!form.value.urgency) {
    errors.urgency = 'Sélectionnez un niveau d’urgence.';
  }
  if (!form.value.contact_preference) {
    errors.contact_preference = 'Sélectionnez une préférence de contact.';
  }
  if (form.value.website_url && !isValidUrl(form.value.website_url)) {
    errors.website_url = 'Indiquez une URL valide, ou laissez le champ vide.';
  }
  if (form.value.phone && !/^[0-9+().\s-]{6,30}$/.test(form.value.phone)) {
    errors.phone = 'Indiquez un numéro de téléphone valide, ou laissez le champ vide.';
  }
  if (!form.value.backups) {
    errors.backups = 'Précisez l’état connu des sauvegardes.';
  }
  if (!form.value.access) {
    errors.access = 'Précisez si les accès sont disponibles.';
  }
  if (form.value.message.length < 20) {
    errors.message = 'Décrivez la situation en au moins 20 caractères.';
  }
  if (form.value.message.length > 4000) {
    errors.message = 'Le message est trop long.';
  }
  if (!form.value.privacy_consent) {
    errors.privacy_consent = 'Le consentement confidentialité est requis.';
  }

  fieldErrors.value = errors;
  formErrors.value = Object.values(errors);

  return formErrors.value.length === 0;
};

// Vérifie qu’une URL optionnelle est syntaxiquement exploitable.
const isValidUrl = (value: string) => {
  try {
    const url = new URL(value);
    return ['http:', 'https:'].includes(url.protocol);
  } catch {
    return false;
  }
};

// Place le focus sur le résumé des erreurs pour les utilisateurs clavier et lecteurs d’écran.
const focusErrors = async () => {
  await nextTick();
  errorSummary.value?.focus();
};

// Construit le payload attendu par l’API sans ajouter de champ sensible.
const buildPayload = () => {
  const {
    name,
    email,
    company,
    phone,
    structure_type,
    service_type,
    urgency,
    contact_preference,
    website_url,
    cms,
    hosting,
    backups,
    access,
    budget,
    found_us,
    message,
    privacy_consent,
    website_company,
    started_at,
  } = form.value;

  return {
    name,
    email,
    company,
    phone,
    structure_type,
    service_type,
    urgency,
    contact_preference,
    website_url,
    cms,
    hosting,
    backups,
    access,
    budget,
    found_us,
    message,
    privacy_consent,
    website_company,
    started_at,
  };
};

// Envoie la demande de contact à l’API Django et affiche le retour utilisateur.
const submitForm = async () => {
  normalizeForm();
  statusMessage.value = '';
  isSuccess.value = false;

  if (!validateForm()) {
    await focusErrors();
    return;
  }

  isSubmitting.value = true;

  try {
    const response = await fetch(`${config.public.apiBase}/api/contacts/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(buildPayload()),
    });

    if (response.ok) {
      isSuccess.value = true;
      statusMessage.value = 'Merci. Nous vous recontacterons avec une première lecture claire.';
      fieldErrors.value = {};
      formErrors.value = [];
      resetForm();
    } else {
      isSuccess.value = false;
      statusMessage.value = response.status === 429
        ? 'Trop de demandes rapprochées. Réessayez un peu plus tard.'
        : 'La demande n’a pas pu être envoyée pour le moment. Vous pouvez réessayer plus tard.';
    }
  } catch (error) {
    isSuccess.value = false;
    statusMessage.value = 'Erreur de connexion. Vérifiez votre connexion et réessayez.';
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
.page-hero {
  @apply border-b border-forest/15 bg-paper py-16 md:py-24;
}

.eyebrow {
  @apply font-mono text-xs font-bold uppercase tracking-[0.24em] text-trust;
}

.page-hero h1 {
  @apply mx-auto mt-5 max-w-4xl font-heading text-4xl font-black leading-[1.04] text-ink sm:text-5xl md:text-6xl;
}

.page-hero p:not(.eyebrow) {
  @apply mx-auto mt-6 max-w-[21rem] text-base leading-8 text-muted md:max-w-3xl md:text-lg;
}

.contact-section {
  @apply bg-sand py-16 md:py-24;
}

.contact-grid {
  @apply grid gap-8 lg:grid-cols-[0.75fr_1.25fr] lg:items-start;
}

.diagnostic-note {
  @apply rounded-lg border border-forest/15 bg-paper p-6 shadow-sm md:p-8;
}

.diagnostic-note h2 {
  @apply mt-4 font-heading text-3xl font-black text-ink;
}

.diagnostic-note p {
  @apply mt-4 leading-7 text-muted;
}

.diagnostic-note .privacy-reminder {
  @apply rounded-lg border border-action/25 bg-action/10 px-4 py-3 text-sm font-bold leading-6 text-ink;
}

.note-block {
  @apply mt-6 rounded-lg border border-trust/15 bg-sand p-5;
}

.note-block h3 {
  @apply font-heading text-xl font-extrabold text-ink;
}

.note-block ul {
  @apply mt-4 space-y-3;
}

.note-block li {
  @apply text-sm font-semibold leading-6 text-forest;
}

.contact-form {
  @apply rounded-lg border border-forest/15 bg-paper p-6 shadow-soft md:p-10;
}

.error-summary {
  @apply mb-8 rounded-lg border border-action/35 bg-action/10 p-5 outline-none;
}

.error-summary:focus {
  @apply ring-2 ring-action ring-offset-2 ring-offset-paper;
}

.error-summary h2 {
  @apply font-heading text-2xl font-black text-ink;
}

.error-summary ul {
  @apply mt-4 grid gap-2;
}

.error-summary li {
  @apply text-sm font-semibold leading-6 text-ink;
}

.honeypot-field {
  @apply pointer-events-none absolute h-px w-px overflow-hidden opacity-0;
}

fieldset {
  @apply mt-8 border-0 p-0 first:mt-0;
}

legend {
  @apply mb-5 font-heading text-2xl font-black text-ink;
}

label span {
  @apply text-sm font-bold text-ink;
}

label small {
  @apply mt-2 block text-xs font-semibold leading-5 text-muted;
}

.field {
  @apply mt-2 w-full rounded-lg border border-forest/20 bg-white/70 px-4 py-3 text-ink outline-none transition;
}

.field::placeholder {
  @apply text-placeholder;
}

.field:focus {
  @apply border-trust bg-white;
  box-shadow: 0 0 0 4px rgba(44, 125, 160, 0.14);
}

.field[aria-invalid='true'] {
  @apply border-action bg-action/5;
}

.consent-row {
  @apply mt-6 grid cursor-pointer grid-cols-[1.25rem_1fr] gap-3 rounded-lg border border-forest/15 bg-sand p-4;
}

.consent-row input {
  @apply mt-1 h-5 w-5 rounded border-forest/30 accent-trust;
}

.consent-row span {
  @apply text-sm leading-6 text-muted;
}

.submit-button {
  @apply mt-8 inline-flex min-h-12 w-full items-center justify-center rounded-lg bg-action px-7 py-3 text-center font-extrabold text-white shadow-orange outline-none transition hover:bg-[#FF9F2D] focus-visible:ring-2 focus-visible:ring-action focus-visible:ring-offset-2 focus-visible:ring-offset-paper disabled:cursor-not-allowed disabled:opacity-60;
}
</style>
