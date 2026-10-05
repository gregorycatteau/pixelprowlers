# Livraison des textes et du parcours contact — 5 octobre 2026

## Base et périmètre

Branche `release/pixelprowlers-contact-ux-20261005`, issue de la version effectivement publiée `abd7b958d66627f591620e863051b4a41fc4e273`, attestée par `https://pixelprowlers.io/_delivery.json` et l’image Nuxt exécutée. Le dépôt initial et ses modifications backend/non suivies restent préservés dans leur répertoire. Aucun backend, migration, volume ni donnée de production ne fait partie du lot.

Le workflow GitHub sur `master` reconstruit aussi Django et applique ses migrations. Il ne doit pas être utilisé pour cette livraison. La procédure frontend séparée décrite dans `livraison-vitrine-20261005.md` reste applicable : artefact Nitro, image dérivée de l’image exécutée sans installation, prévalidation, override Compose exclusivement Nuxt, puis contrôles publics. La branche de livraison ne déclenche pas ce workflow.

## Contrat du contact

Seul le paramètre non personnel `besoin` est utilisé. Valeurs autorisées : `reparation`, `reemploi`, `conseil`, `developpement`, `formation`, `autre`. Valeurs inconnues, répétées ou héritées : aucune présélection. Aucun symptôme ni coordonnée n’est ajouté à l’URL.

| Besoin public | serviceType existant | demandType existant |
| --- | --- | --- |
| Réparation | materiel | diagnostic |
| Réemploi | materiel | partnership |
| Conseil / assistance / cybersécurité | maintenance_documentation | transmission |
| Développement | developpement | refonte |
| Formation | formation | transmission |
| Autre | autre | partnership |

Le libellé complet du besoin reste dans le message : les catégories historiques partnership/transmission ne doivent pas masquer la demande réelle. Les détails optionnels du besoin actif sont ajoutés au message, sans troncature ; les champs d’un besoin inactif ne sont pas transmis. Description : 20–500 caractères ; message enrichi : au plus 4000, limite de l’API. Nom : 160, email : 254, téléphone : 40. Champs optionnels : appareil/modèle ou usage/budget. État d’attente, refus du double envoi, erreur accessible, saisie conservée et suivi après enregistrement sont maintenus. Les protections serveur et le mécanisme antispam existant ne sont pas modifiés.

Les empreintes de crm/models.py, crm/schema.py, pixelprowlers/settings.py et pixelprowlers/urls.py sont identiques entre le backend testé et le conteneur de production exécuté. Cela confirme le contrat contrôlé ; cela ne prouve pas le fonctionnement du SMTP de production.

## Contenus et observations

Comptage du texte rendu dans main, hors navigation/footer, mots séparés par espaces, FAQ ouverte pour inclure ses réponses : accueil 318 → 323 ; réparation 684 → 378 ; À propos 776 → 295. Les légendes et libellés des liens sont inclus. Pas de données produits sur ces pages.

Réparation : micro-soudure, appareils, symptômes, trois étapes, FAQ, batteries et données ; un seul CTA principal sélectionne réparation. À propos : uniquement les éléments du parcours présents dans la version antérieure, portrait en randonnée déjà utilisé, sans dates ou qualifications nouvelles. Réemploi : demande de disponibilité sans stock ni prix inventés. Footer : deux phrases. Les illustrations éditoriales conservent leur mention générée.

Défaut confirmé sur la version publiée : un lien du menu mobile fermé reçoit le focus malgré aria-hidden. Avec inert, il ne le reçoit plus. Ouverture clavier, Échap, retour au déclencheur et aria-expanded ont été vérifiés. Contact et Urgence web ont leurs propres titres, descriptions et URL canoniques, y compris après navigation Vue.

## Validations exécutées avant livraison

- 34 tests Vitest réussis : présélection, refus des paramètres invalides, mapping, enrichissement sans troncature, champs inactifs, attente/double envoi, erreurs et nouvel envoi.
- Build Nuxt réussi, sans installation de dépendances.
- Navigateur Chromium à 390, 768 et 1440 px : dix pages, images chargées, cadrages et titres, aucun débordement ni exception JavaScript ; contrôle clavier du menu et lien d’évitement.
- Formulaire navigateur : attente puis HTTP 503 simulé, saisie conservée, nouvel envoi réel vers Django isolé et arrivée sur le suivi.
- Six mappings exécutés contre Django avec vérification des lignes Contact/ContactMessage et des notifications en mémoire. Base SQLite dédiée uniquement ; connexions sortantes interdites ; adresses réservées example.invalid ; aucun SMTP ni message à un tiers.
- Métadonnées Contact/Urgence vérifiées après navigation côté client. La livraison doit également vérifier leur HTML public rendu.

Captures avant : `/tmp/pixelprowlers-release-captures-0o4xnqna` ; revue après à trois largeurs : `/tmp/pixelprowlers-release-captures-tf1ckz2h`. Les captures finales après correction du contraste seront référencées dans le compte rendu. Les copies de travail et captures ne sont pas des assets applicatifs et ne sont pas ajoutées automatiquement.

## Informations encore à confirmer

Zone d’intervention, dépôt/envoi/déplacement et éventuel accueil sur rendez-vous : non confirmés, donc non publiés. Aucune adresse administrative n’est assimilée à un lieu de dépôt. Aucun asset confirmé de machine prête à l’usage n’a été identifié ; l’illustration de réemploi reste explicitement générée et distincte d’une fiche de vente. Livraison SMTP réelle non testée, afin de ne pas envoyer de message à un tiers.

## Retour arrière

Avant bascule, conserver le SHA précédent ci-dessus et l’image exécutée. Le déploiement crée `/opt/pixelprowlers-deploy-backups/frontend-20261005-<SHA-livré>/rollback.yml` et une étiquette locale de l’image précédente. Depuis `/opt/pixelprowlers` :

```sh
docker compose -f compose.yml -f /opt/pixelprowlers-deploy-backups/frontend-20261005-<SHA-livré>/rollback.yml up -d --no-deps --no-build nuxt
```

Le retour arrière ne touche ni Django ni PostgreSQL. Après toute relance opérationnelle, conserver l’override de livraison actif pour ne pas revenir involontairement à l’image définie dans le checkout historique. Vérifier ensuite le SHA dans `_delivery.json` et les parcours publics. Ce document décrit la préparation et les validations ; le compte rendu final établira le SHA effectivement déployé et ses preuves en ligne.
