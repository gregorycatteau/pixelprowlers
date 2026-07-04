<template>
  <main>
    <section id="probleme" class="hero-section" aria-labelledby="hero-title">
      <div class="container">
        <div class="hero-copy">
          <h1 id="hero-title">
            Votre site ralentit l'équipe. Vos accès sont partout. Et si demain, la personne qui sait
            comment ça marche n'est pas là ?
          </h1>
          <p>
            PixelProwlers remet ça en ordre. Sites qui tiennent la route. Accès qui se voient.
            Sauvegardes qui sauvent vraiment.
          </p>
          <div class="hero-actions" aria-label="Actions principales">
            <AppButton href="/diagnostic-situation">Diagnostic gratuit - clarifions votre situation</AppButton>
            <AppButton variant="validate" href="/urgence">Urgence maintenant ? Décrivez-moi votre problème</AppButton>
          </div>
        </div>
      </div>
    </section>

    <section id="solutions" class="section section-alt" aria-labelledby="offers-title">
      <div class="container">
        <div class="section-heading">
          <p class="eyebrow">Offres principales</p>
          <h2 id="offers-title">Trois chemins selon où vous en êtes.</h2>
        </div>

        <div class="card-grid three">
          <article v-for="offer in offers" :key="offer.title" class="card offer-card">
            <p class="eyebrow">{{ offer.kicker }}</p>
            <h3>{{ offer.title }}</h3>
            <p>{{ offer.description }}</p>
            <ul>
              <li v-for="point in offer.points" :key="point">{{ point }}</li>
            </ul>
            <AppButton class="card-action" :href="offer.href">{{ offer.cta }}</AppButton>
          </article>
        </div>
      </div>
    </section>

    <section id="angles-morts" class="section" aria-labelledby="mirror-title">
      <div class="container">
        <div class="section-heading">
          <p class="eyebrow">Angles morts</p>
          <h2 id="mirror-title">Ça vous parle ?</h2>
          <p>On commence par nommer ce qui fatigue l'équipe, puis on distingue ce qui est urgent.</p>
        </div>

        <div class="card-grid three">
          <article v-for="problem in problems" :key="problem.title" class="card">
            <h3>{{ problem.title }}</h3>
            <p class="zone-impact">Zone impactée : <strong>{{ problem.zone }}</strong>, {{ problem.description }}</p>
          </article>
        </div>
      </div>
    </section>

    <section id="methode" class="section" aria-labelledby="method-title">
      <div class="container method-grid">
        <div class="section-heading">
          <p class="eyebrow">Méthode</p>
          <h2 id="method-title">On avance étape par étape.</h2>
          <p>Comprendre, rendre visible, décider, puis transmettre.</p>
        </div>

        <div class="steps">
          <article v-for="step in steps" :key="step.title" class="step-card">
            <span>{{ step.number }}</span>
            <div>
              <h3>{{ step.title }}</h3>
              <p>{{ step.description }}</p>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section id="cadre" class="section section-alt" aria-labelledby="audience-title">
      <div class="container">
        <div class="section-heading">
          <p class="eyebrow">Cadre de collaboration</p>
          <h2 id="audience-title">C'est pour vous ? Ou pas.</h2>
        </div>

        <div class="card-grid two">
          <article class="card">
            <h3>Pour vous si...</h3>
            <ul>
              <li v-for="item in goodFits" :key="item">{{ item }}</li>
            </ul>
          </article>

          <article class="card">
            <h3>Pas idéal si...</h3>
            <ul>
              <li v-for="item in badFits" :key="item">{{ item }}</li>
            </ul>
          </article>
        </div>
      </div>
    </section>

    <section id="contact" class="final-section" aria-labelledby="final-title">
      <div class="container">
        <div class="final-panel">
          <p class="eyebrow light">Premier échange</p>
          <h2 id="final-title">Vous êtes prêts ? On démarre.</h2>
          <p>Un diagnostic simple : comprendre ce que vous faites, ce qui vous stresse, par quoi commencer.</p>
          <AppButton href="/diagnostic-situation">Lancer le diagnostic</AppButton>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';
import { badFits, goodFits, offers, problems, steps } from '~/utils/siteContent';
</script>

<style scoped>
.hero-section {
  padding: 72px 0;
  background:
    linear-gradient(90deg, rgba(247, 244, 234, 0.94), rgba(247, 244, 234, 0.76)),
    url("/fond.jpg") center / cover;
}

.hero-copy {
  max-width: 940px;
}

.hero-copy h1 {
  max-width: 880px;
  font-size: clamp(2.25rem, 5vw, 4.9rem);
  line-height: 1.02;
  font-weight: 900;
}

.hero-copy > p {
  max-width: 760px;
  margin-top: 28px;
  color: #445046;
  font-size: 1.18rem;
  line-height: 1.75;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-top: 34px;
}

.offer-card {
  display: flex;
  min-height: 100%;
  flex-direction: column;
}

.card-action {
  margin-top: auto;
}

.zone-impact {
  margin-top: 14px;
  color: #596158;
  line-height: 1.65;
}

.method-grid {
  display: grid;
  grid-template-columns: 0.85fr 1.15fr;
  gap: 40px;
  align-items: start;
}

.steps {
  display: grid;
  gap: 16px;
}

.step-card {
  display: grid;
  grid-template-columns: 64px 1fr;
  gap: 18px;
  border: 1px solid rgba(43, 112, 83, 0.16);
  border-radius: 8px;
  background: #f7f4ea;
  padding: 20px;
}

.step-card > span {
  display: flex;
  width: 56px;
  height: 56px;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: #2b7053;
  color: white;
  font-weight: 900;
}

.final-section {
  padding: 76px 0;
  background: #fbfaf5;
}

.final-panel {
  border-radius: 8px;
  background: #102033;
  padding: 34px;
  color: white;
}

.final-panel p:not(.eyebrow) {
  max-width: 680px;
  margin-top: 18px;
  color: rgba(255, 255, 255, 0.76);
  font-size: 1.08rem;
  line-height: 1.7;
}

.final-panel .ButtonBase {
  margin-top: 28px;
}

@media (max-width: 900px) {
  .method-grid {
    grid-template-columns: 1fr;
  }
}
</style>
