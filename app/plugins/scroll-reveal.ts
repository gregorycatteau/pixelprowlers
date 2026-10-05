/*
 * Directive v-reveal : révèle progressivement un élément lorsqu’il entre
 * dans le viewport, pour rythmer le défilement des sections longues sans
 * dépendre d’une bibliothèque externe. N’a aucun effet si l’élément est
 * déjà visible au montage (pas de flash de contenu caché) ni si
 * l’utilisateur préfère un mouvement réduit (géré par CSS, cf. main.css).
 */
export default defineNuxtPlugin((nuxtApp) => {
  const prefersReducedMotion = () =>
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const isAlreadyInViewport = (el: HTMLElement) => {
    const rect = el.getBoundingClientRect();
    return rect.top < window.innerHeight * 0.92;
  };

  nuxtApp.vueApp.directive('reveal', {
    mounted(el: HTMLElement) {
      if (prefersReducedMotion() || isAlreadyInViewport(el)) {
        return;
      }

      el.classList.add('reveal');

      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              el.classList.add('is-visible');
              observer.unobserve(el);
            }
          });
        },
        { threshold: 0.15, rootMargin: '0px 0px -8% 0px' },
      );

      observer.observe(el);
    },
  });
});
