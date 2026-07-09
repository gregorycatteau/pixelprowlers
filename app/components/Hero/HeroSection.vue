<template>
  <section
    class="HeroSection"
    aria-labelledby="hero-title"
    :style="{ '--hero-waves-image': `url('${heroWavesSvg}')` }"
  >
    <div class="HeroWaves" aria-hidden="true"></div>

    <div class="HeroContent">
      <h1 id="hero-title" v-html="title"></h1>
      <p>{{ subtitle }}</p>
      <a class="HeroCta" :href="ctaLink">{{ ctaText }}</a>
      <p v-if="ctaNote" class="HeroCtaNote">{{ ctaNote }}</p>
    </div>

    <img class="HeroSauveteur" :src="sauveteurSvg" alt="" aria-hidden="true">
  </section>
</template>

<script setup lang="ts">
import heroWavesSvg from '~/assets/images/hero-waves.svg?url';
import sauveteurSvg from '~/assets/images/sauveteur.svg?url';

interface Props {
  title: string;
  subtitle: string;
  ctaText: string;
  ctaLink: string;
  ctaNote?: string;
}

defineProps<Props>();
</script>

<style scoped>
.HeroSection {
  position: relative;
  display: flex;
  width: 100vw;
  max-width: 100vw;
  min-height: 85vh;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: linear-gradient(135deg, #0f172a, #1e3a8a 52%, #0891b2);
  color: white;
  padding: 6rem 1rem 7rem;
}

.HeroWaves {
  position: absolute;
  inset: auto 0 0;
  height: 10rem;
  background-image: var(--hero-waves-image);
  background-repeat: repeat-x;
  background-size: 2000px 160px;
  opacity: 0.92;
  animation: hero-wave 15s linear infinite reverse;
  will-change: background-position;
}

.HeroContent {
  position: relative;
  z-index: 2;
  width: min(100%, 62rem);
  max-width: 62rem;
  text-align: center;
}

.HeroContent h1 {
  margin-bottom: 1.5rem;
  max-width: 100%;
  font-size: clamp(2.05rem, 6vw, 5.35rem);
  font-weight: 900;
  line-height: 1;
  overflow-wrap: anywhere;
  text-shadow: 0 8px 26px rgba(2, 6, 23, 0.42);
}

.HeroContent h1 :deep(.HeroTitleLine) {
  display: block;
}

.HeroContent h1 :deep(.HeroTitleLineSecondary) {
  margin-top: clamp(1.1rem, 2.4vw, 2rem);
  color: rgba(224, 242, 254, 0.92);
  font-size: 0.82em;
}

.HeroContent h1 :deep(.HeroTitleAccent) {
  color: #fbbf24;
  text-shadow:
    0 0 26px rgba(251, 191, 36, 0.44),
    0 8px 26px rgba(2, 6, 23, 0.36);
  white-space: nowrap;
}

.HeroContent p {
  max-width: 48rem;
  margin: 0 auto 2.5rem;
  color: rgba(224, 242, 254, 0.92);
  font-size: clamp(1.1rem, 2.6vw, 1.55rem);
  line-height: 1.65;
  text-shadow: 0 4px 18px rgba(2, 6, 23, 0.32);
}

.HeroCta {
  position: relative;
  display: inline-block;
  overflow: hidden;
  border-radius: 999px;
  background: linear-gradient(135deg, #ff6b35, #e55a2b);
  color: white;
  padding: 1rem 2rem;
  font-size: 1.15rem;
  font-weight: 800;
  text-decoration: none;
  box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4);
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.HeroCta::after {
  content: "";
  position: absolute;
  inset: 0 auto 0 -100%;
  width: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.22), transparent);
  transition: left 0.5s ease;
}

.HeroCta:hover,
.HeroCta:focus-visible {
  transform: translateY(-0.5rem);
  box-shadow: 0 18px 36px rgba(255, 107, 53, 0.34);
}

.HeroCta:hover::after,
.HeroCta:focus-visible::after {
  left: 100%;
}

.HeroCtaNote {
  max-width: 36rem !important;
  margin: 1rem auto 0 !important;
  color: rgba(224, 242, 254, 0.9) !important;
  font-size: 0.98rem !important;
  font-weight: 800;
  line-height: 1.5 !important;
}

.HeroSauveteur {
  position: absolute;
  bottom: 0.8rem;
  left: clamp(1rem, 6vw, 4rem);
  z-index: 3;
  width: clamp(8rem, 17vw, 13rem);
  height: auto;
  animation: hero-float 3.4s ease-in-out infinite;
  filter: drop-shadow(0 20px 28px rgba(2, 6, 23, 0.32));
  will-change: transform;
}

@keyframes hero-wave {
  0% {
    background-position-x: 0;
  }

  100% {
    background-position-x: -2000px;
  }
}

@keyframes hero-float {
  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-10px);
  }
}

@media (max-width: 767px) {
  .HeroSection {
    min-height: 78vh;
    padding: 4rem 0.75rem 8rem;
  }

  .HeroContent {
    width: min(100%, 17rem);
  }

  .HeroContent h1 {
    font-size: clamp(1.85rem, 8vw, 2.3rem);
    line-height: 1.08;
  }

  .HeroContent h1 :deep(.HeroTitleLineSecondary) {
    font-size: 0.72em;
  }

  .HeroContent p {
    font-size: 1.05rem;
    line-height: 1.5;
  }

  .HeroCta {
    width: min(100%, 17rem);
    padding-inline: 1rem;
    text-align: center;
  }

  .HeroSauveteur {
    left: 50%;
    transform: translateX(-50%);
    width: 7rem;
    animation-name: hero-float-mobile;
  }
}

@keyframes hero-float-mobile {
  0%,
  100% {
    transform: translateX(-50%) translateY(0);
  }

  50% {
    transform: translateX(-50%) translateY(-8px);
  }
}
</style>
