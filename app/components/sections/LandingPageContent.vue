<template>
  <main class="landing-page">
    <section class="landing-hero" aria-labelledby="landing-title">
      <div class="article-container">
        <p class="eyebrow">{{ landing.kicker }}</p>
        <h1 id="landing-title">{{ landing.title }}</h1>
        <p>{{ landing.subtitle }}</p>
        <div class="landing-actions">
          <AppButton :href="landing.primaryHref">{{ landing.heroCta }}</AppButton>
          <AppButton variant="secondary" :href="landing.secondaryHref">{{ landing.secondaryCta }}</AppButton>
        </div>
        <p v-if="landing.heroCtaNote" class="cta-note">{{ landing.heroCtaNote }}</p>
      </div>
    </section>

    <section
      v-for="section in landing.sections"
      :key="section.title"
      v-reveal
      class="landing-section"
      :class="{ 'section-alt': section.alt }"
      :aria-labelledby="section.id"
    >
      <div class="article-container">
        <h2 :id="section.id">{{ section.title }}</h2>
        <p v-if="section.intro" class="landing-intro">{{ section.intro }}</p>
        <div v-if="section.blocks" class="landing-block-grid">
          <article v-for="block in section.blocks" :key="block.title" class="landing-block">
            <h3>{{ block.title }}</h3>
            <p v-if="block.text">{{ block.text }}</p>
            <ul v-if="block.items">
              <li v-for="item in block.items" :key="item">{{ item }}</li>
            </ul>
          </article>
        </div>
        <ul v-if="section.items" class="plain-list good-list">
          <li v-for="item in section.items" :key="item">{{ item }}</li>
        </ul>
        <div v-if="section.paragraphs" class="manifest-copy">
          <p v-for="paragraph in section.paragraphs" :key="paragraph">{{ paragraph }}</p>
        </div>
      </div>
    </section>

    <section class="landing-final" aria-labelledby="landing-final-title">
      <div class="article-container">
        <h2 id="landing-final-title">{{ landing.finalTitle }}</h2>
        <p>{{ landing.finalText }}</p>
        <div class="landing-actions">
          <AppButton :href="landing.primaryHref">{{ landing.finalCta }}</AppButton>
          <AppButton variant="secondary" :href="landing.secondaryHref">{{ landing.secondaryCta }}</AppButton>
        </div>
        <p v-if="landing.finalCtaNote" class="cta-note final-note">{{ landing.finalCtaNote }}</p>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';
import type { Landing } from '~/utils/siteContent';

defineProps<{ landing: Landing }>();
</script>

<style scoped>
.landing-block-grid,
.landing-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  margin-top: 30px;
}

.landing-block {
  flex: 1 1 260px;
}

.cta-note {
  max-width: 640px;
  margin-top: 14px;
  color: #435046;
  font-size: 0.96rem;
  font-weight: 800;
  line-height: 1.55;
}

.final-note {
  color: rgba(255, 255, 255, 0.86);
}
</style>
