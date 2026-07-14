# Instructions pour Claude Code — PixelProwlers

## Autonomie

Sur ce dépôt, Grégory a explicitement autorisé le niveau d'autonomie suivant (pas besoin de redemander confirmation à chaque fois) :

**Autorisé sans confirmation préalable** : corriger des bugs, créer/modifier des fichiers, committer, lancer builds/tests/migrations, ajuster de la config non secrète (CORS, variables d'environnement, settings), lancer des sous-agents, pousser sur `master` (déclenche le déploiement automatique vers le VPS via `.github/workflows/deploy-preprod.yml`).

**Toujours interdit sans feu vert explicite** : toute action destructrice ou difficile à annuler — `git push --force`, suppression de données/tables/containers/volumes, révocation d'accès, `rm -rf`, réécriture d'historique git.

**Strictement hors-limites, en toutes circonstances** : tout ce qui touche à **Odoo** ou **Multibike**, même de façon incidentale (containers Docker, bases de données, dépôts, fichiers de config). Ne jamais interagir avec ces systèmes, même accidentellement croisés sur la machine.

Cette machine héberge plusieurs projets clients distincts (containers Docker visibles au-delà de pixelprowlers) — rester strictement dans le périmètre de ce dépôt et de ses containers (`pixelprowlers-*`).
