type PixelSeoOptions = {
  title: string;
  description: string;
  path: string;
  type?: 'website' | 'article';
};

const siteUrl = 'https://pixelprowlers.fr';
const defaultImage = `${siteUrl}/og-pixelprowlers.png`;

// Applique les métadonnées SEO, Open Graph, Twitter et canonical pour une page publique.
export const usePixelSeo = ({ title, description, path, type = 'website' }: PixelSeoOptions) => {
  const url = `${siteUrl}${path}`;

  useHead({
    title,
    link: [
      { rel: 'canonical', href: url },
    ],
    meta: [
      { name: 'description', content: description },
      { property: 'og:type', content: type },
      { property: 'og:title', content: title },
      { property: 'og:description', content: description },
      { property: 'og:url', content: url },
      { property: 'og:image', content: defaultImage },
      { property: 'og:site_name', content: 'PixelProwlers' },
      { name: 'twitter:card', content: 'summary_large_image' },
      { name: 'twitter:title', content: title },
      { name: 'twitter:description', content: description },
      { name: 'twitter:image', content: defaultImage },
    ],
  });
};
