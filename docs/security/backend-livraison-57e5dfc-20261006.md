# Livraison backend historique — 6 octobre 2026

## Déployé et vérifié en ligne, exploitation encore partiellement qualifiée

URL : https://pixelprowlers.io.
Code livré : `57e5dfc19e0b3a9b90806d51a3b563dcb4b03a14`.
Branche publiée : `fix/backend-historique-securite-runtime-20261006`.
Les commits applicatifs `d0b1e24` et `57e5dfc` sont signés et vérifiés GPG.

Image exécutée : `pixelprowlers-django:security-57e5dfc19e0b`, ID
`sha256:0ed9588afceea5ff168d375eaa8efda8307924f84aaeca888a3732d7c5b24aae`.
Archive contrôlée avant import : SHA-256
`0de5a114028061bfead2403e02a4b5370ea81ee358f24d8406faa45b3781e95f`.
L'image n'a pas été reconstruite après ses vérifications.

## Périmètre effectivement livré

Django seul recréé : fermeture des opérations et relations privées GraphQL,
autorisation objet, diagnostics signés, analyse de refonte neutralisée,
secrets de secours supprimés, notifications console non présentées comme SMTP,
quotas atomiques partagés entre workers et proxy Caddy explicitement reconnu.
Les réglages réellement actifs ont été conservés en mémoire, avec surcharge
Compose externe ne contenant que des références. Pas de workflow global.

Aucune migration, installation de dépendance, modification de modèle ou
déploiement du backend récent. Conteneurs, images et montages PostgreSQL/Nuxt
inchangés. Frontend conservé à `1205eeb78e4985930f0a326dcb403052be222482`.
Dépôt principal et fichiers non suivis préservés.

Le runtime livré est Python **3.13.13**, contre **3.13.14** précédemment actif.
Cet écart est déclaré et l'image exécutée est celle effectivement qualifiée.

## Vérifications exécutées

- Image portant le SHA livré : **34 tests Django réussis**, DEBUG=False,
  PostgreSQL isolé ; **16/16 contrats frontend** ; aucune migration détectée.
- HTTPS local, trois workers et rôle SQL réduit de qualification : contact →
  ticket → réponse à 390/768/1440 px ; diagnostic signé ; cookie de session
  Secure/HttpOnly/SameSite=Lax ; refus d'accès refonte après perte du cookie.
- Production : image/label vérifiés, Django sain, connexion PostgreSQL confirmée
  par `SELECT 1`, champs privés absents du schéma chargé, moteur d'analyse manuel.
- HTTP public : pages accessibles, lectures CRM/suppression/introspection
  refusées ; capacités/signatures/sessions invalides refusées sans données,
  réponses `no-store` et `no-referrer`. Aucun dossier client consulté.
- Navigateur en ligne à 390/768/1440 px : accueil/réparation/contact, images,
  police, absence de débordement et focus clavier ; ouverture/fermeture du menu
  mobile au clavier avec retour du focus. Aucune soumission réelle de formulaire.

Preuves locales protégées : `/tmp/pixelprowlers-backend-ops-20261006/`, notamment
`delivery-tests.txt`, `delivery-contracts.json`, `delivery-migrations.txt`,
`delivery-browser-*.txt`, `production-http-checks.txt`, `production-denials.json`,
`production-menu-browser.txt` et `deployed-manifest.json`.
Manifeste serveur protégé :
`/opt/pixelprowlers-deploy-backups/backend-operations-20261006/deployed-manifest.json`.

## Sauvegarde et retour arrière

Avant livraison, sauvegarde réelle de production et restauration isolée sur
la même image PostgreSQL réussies : schéma normalisé, contraintes, migrations
et agrégats concordants, sans publication de contenu client. Archive protégée
conservée sur le VPS ; copie externe encore absente.

Image précédente conservée :
`sha256:1fd7de0d2b3028177417e877683cced740ac40955ec1ce25aba93027e671d139`.
La procédure impose le confinement persistant et trois contrôles HTTP 503
**avant** le retour à cette image vulnérable. Configuration adaptée et routes
testées isolément ; interface 503 qualifiée sans perte de saisie ni faux succès.
Le retour arrière réel n'a pas été exécuté, faute de régression nécessitant cette action.

Commande sur le VPS identifié :

```bash
python3 /opt/pixelprowlers-deploy-backups/backend-operations-20261006/delivery-scripts/rollback-confined.py /opt/pixelprowlers-deploy-backups/backend-operations-20261006
```

Aucune restauration de la base active pour un retour d'image. Ne pas utiliser
le Compose de base seul ou le workflow global : ils ne reproduisent pas cette livraison.

## Fonctionnalités et exploitation différées

- SMTP reste **console**, aucun email réel envoyé ni réception affirmée.
  Identifiant Django personnel, boîte de test contrôlée et destinataires internes
  toujours attendus pour le lot d'exploitation.
- Rôle PostgreSQL réduit qualifié sur fixtures, **non activé en production** ;
  le rôle courant conserve ses privilèges historiques. Accès de maintenance
  séparé à préserver lors de ce changement ultérieur.
- Clé indépendante `AUDIT_SIGNATURE_KEY` encore absente : finalisation refusée
  avant écriture. Secret Django existant conservé ; aucun nouveau secret public.
- Notifications des réponses et reprise durable des échecs non implémentées.
- Écran résultat refonte encore mal routé ; API manuelle protégée qualifiée,
  aucune analyse automatique ni lien email inter-navigateurs promis.
- Quotas partagés dans un conteneur, éphémères après recréation ; plusieurs
  réplicas demanderaient un stockage central distinct.
- Destination de sauvegarde externe et conservation externe à fournir.

La fermeture privée/SSRF et l'anti-abus sont livrés. Le traitement complet des
demandes par un opérateur et une boîte email reste **non qualifié de bout en bout**.
