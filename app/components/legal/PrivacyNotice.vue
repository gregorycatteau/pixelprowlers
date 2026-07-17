<template>
  <aside
    :id="noticeId"
    class="PrivacyNotice"
    :aria-labelledby="titleId"
    role="note"
  >
    <div class="PrivacyHeader">
      <p class="PrivacyKicker">Protection de vos données</p>

      <h3 :id="titleId">
        {{ title }}
      </h3>
    </div>

    <p class="PrivacyPurpose">
      {{ purpose }}
    </p>

    <dl class="PrivacyDetails">
      <div>
        <dt>Base légale</dt>
        <dd>{{ legalBasis }}</dd>
      </div>

      <div>
        <dt>Destinataires</dt>
        <dd>{{ recipients }}</dd>
      </div>

      <div>
        <dt>Conservation</dt>
        <dd>{{ retention }}</dd>
      </div>

      <div>
        <dt>Champs obligatoires</dt>
        <dd>{{ requiredFields }}</dd>
      </div>
    </dl>

    <p v-if="showSecurityReminder" class="SecurityReminder">
      <strong>Ne transmettez aucun secret dans ce formulaire.</strong>
      N’envoyez pas de mot de passe, token, clé privée, cookie de session,
      sauvegarde, accès administrateur ou document sensible.
    </p>

    <p class="PrivacyRights">
      Vous pouvez exercer vos droits d’accès, de rectification, d’effacement,
      de limitation ou d’opposition en écrivant à
      <a href="mailto:contact@pixelprowlers.io">
        contact@pixelprowlers.io
      </a>.
      Consultez la
      <NuxtLink to="/confidentialite">
        politique de confidentialité
      </NuxtLink>
      pour connaître le détail des traitements et de vos droits.
    </p>

    <p class="MarketingNotice">
      L’envoi de ce formulaire ne vous inscrit à aucune communication
      promotionnelle.
    </p>
  </aside>
</template>

<script setup lang="ts">
interface PrivacyNoticeProps {
  noticeId: string;
  purpose: string;
  legalBasis: string;
  retention: string;
  title?: string;
  recipients?: string;
  requiredFields?: string;
  showSecurityReminder?: boolean;
}

const props = withDefaults(defineProps<PrivacyNoticeProps>(), {
  title: "Comment ces informations seront-elles utilisées ?",
  recipients:
    "PixelProwlers et, lorsque cela est nécessaire, ses prestataires techniques autorisés.",
  requiredFields:
    "Les champs signalés comme obligatoires sont nécessaires pour traiter la demande. Sans eux, le formulaire ne peut pas être envoyé.",
  showSecurityReminder: true,
});

const titleId = computed(() => `${props.noticeId}-title`);
</script>

<style scoped>
@reference "../../assets/css/main.css";

.PrivacyNotice {
  @apply mt-6 rounded-lg border border-pxp-green/20 bg-primary-50 p-5 text-pxp-ink;
}

.PrivacyHeader {
  @apply border-b border-pxp-green/15 pb-4;
}

.PrivacyKicker {
  @apply text-xs font-black uppercase tracking-widest text-pxp-green;
}

.PrivacyHeader h3 {
  @apply mt-2 text-lg font-black leading-snug text-pxp-ink;
}

.PrivacyPurpose {
  @apply mt-4 leading-7 text-pxp-ink/80;
}

.PrivacyDetails {
  @apply mt-5 grid gap-4;
}

.PrivacyDetails div {
  @apply rounded-md border border-pxp-green/15 bg-white p-4;
}

.PrivacyDetails dt {
  @apply text-xs font-black uppercase tracking-wide text-pxp-green;
}

.PrivacyDetails dd {
  @apply mt-2 text-sm leading-6 text-pxp-ink/80;
}

.SecurityReminder {
  @apply mt-5 rounded-md border border-pxp-orange/30 bg-white p-4 text-sm leading-6 text-pxp-ink/80;
}

.SecurityReminder strong {
  @apply block font-black text-pxp-ink;
}

.PrivacyRights,
.MarketingNotice {
  @apply mt-5 text-sm leading-6 text-pxp-ink/75;
}

.PrivacyRights a {
  @apply rounded-sm font-bold text-pxp-green underline decoration-pxp-green/30 underline-offset-4 transition hover:decoration-pxp-green focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-pxp-green;
}

.MarketingNotice {
  @apply border-t border-pxp-green/15 pt-4 font-bold;
}

@media (min-width: 768px) {
  .PrivacyNotice {
    @apply p-6;
  }

  .PrivacyDetails {
    @apply grid-cols-2;
  }
}
</style>