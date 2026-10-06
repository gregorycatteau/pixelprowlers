# Tarifs et parcours de réparation — 6 octobre 2026

## Base observée et périmètre

Production vérifiée par _delivery.json : 14f858a9d691c70bbca744da3c732cca2de6817a. Image Nuxt exécutée : sha256:64931c795ff834ae35f9a44ec4fa6a0e2049a7bd341e09e0f412cfe6f1f9601e. Branche dédiée release/pixelprowlers-tarifs-reparation-20261006, worktree distinct depuis cette version. Dépôt principal c0d9c13 et tous ses changements, dont backend/.dockerignore et fichiers non suivis, conservés.

Frontend uniquement : grille, parcours existant, cartes de prix, illustrations SVG originales console/manette, CTA accueil/menu et textes. Aucun changement Django, PostgreSQL, volume, migration de production ou dépendance. Le workflow master/workflow_dispatch redéploie aussi Django et reste exclu.

## Autorisation et données publiques

Source : instruction métier jointe du 6 octobre 2026. Version reparation-20261006-v2-tarifs. 41 offres centralisées, dont 40 publiables ; montants entiers en centimes, identifiants stables, familles, symptômes, périmètre, inclusions/exclusions, cas sur devis et publication. Les prestations PC communes alimentent fixe et portable sans septième famille. Aucune donnée de rentabilité, fournisseur ou validation technique fictive. L’autorisation d’afficher les montants n’est pas assimilée à une qualification de modèles/pièces.

Six familles actives : portable, fixe, téléphone, tablette, console de jeu, manette. 50 observations, avec cas inconnu et liquide. Choix appareil → symptôme → une précision utile au besoin → budget → modèle facultatif et contact. Précisions allowlist : écran LCD/OLED/origine, console PS4/Xbox/PS5/Switch, un/deux joysticks, PC/MacBook, DC-Jack/USB-C. Une option inconnue permet toujours un repère sans référence technique obligatoire.

Montants conservés sans conversion HT/TTC. Formulation consommateurs conditionnelle à la TVA, aucun taux ou statut d’exonération supposé. L’ancienne affirmation « TVA non applicable, article 293 B » des mentions légales a été retirée, faute de preuve disponible, conformément à l’instruction. Aucun autre statut juridique n’est déduit de cette modification.

Distinction forfait, budget indicatif et diagnostic. Scénarios alternatifs sans addition ; trois scénarios principaux au maximum, autre possibilité dans un dépliable. Écran LCD proposé uniquement pour un appareil LCD, sans substitution implicite à l’OLED. Liquide : diagnostics d’abord, traitement possible et sans garantie de remise en fonctionnement. HDMI seulement dans son périmètre console, sans cause vidéo affirmée. Modèle libre au contact, sans effet tarifaire ou compatibilité supposée.

Hall/TMR 89–119 € conservé dans les données mais publié=false : absent des scénarios et du catalogue affichés. Kit, compatibilité, calibration et prestation réelle non qualifiés.

## Diagnostic et contact

Orientation gratuite sans démontage/recherche technique. Standard 49 € : jusqu’à 30 minutes actives, tests et devis/bilan. Approfondi 89 € : jusqu’à 60 minutes actives, mesures sur carte mère et devis/bilan. Non cumulés ; passage standard → approfondi pour 40 € après accord. Déduction du montant total : 219 € moins 89 € = 130 €. Si le total est inférieur au diagnostic payé : remboursement ou avoir convenu. Entretien défini et nettoyage de port à forfait sans diagnostic séparé systématique ; recherche hors périmètre après accord complémentaire. Aucune facturation, paiement ou réservation créée.

Contact existant réutilisé : reparation → materiel/diagnostic. Famille, observation, précision, modèle indiqué avec compatibilité à vérifier, tous les scénarios montrés et leurs budgets/périmètres, déduction et version dans le message. Description et coordonnées conservées après erreur/retour ; aucune resélection du besoin. Message enrichi plafonné à 4000 sans troncature ; aucun état global mutable, donnée personnelle en URL, stockage persistant ou rendu HTML brut. Les liens directs historiques restent utilisables.

## Vérifications et limites

56 tests : les 41 montants exacts, valeurs absentes/incohérentes, alternatives sans total, OLED/LCD, console, joysticks, Hall/TMR désactivé, groupes PC, liquide, déduction/avoir, allowlist, retours, invalidations, modèle inconnu et contact existant. Build Nuxt. Vue-tsc comparé à la base fraîche : les mêmes 22 erreurs historiques ; contrôle global en échec, aucune nouvelle erreur identifiée.

Navigateur 390, 768, 1440 px : cartes, montants, distinction, clavier/focus, précision inconnue, retours, modification, modèle facultatif après budget, images, police, canoniques, absence de débordement et d’exception observée. Les 50 observations atteignent un budget. Contact : échec 503 simulé, protection double envoi, champs conservés, symptôme/budget actualisé puis enregistrement réel en environnement dédié. Django compatible monté en lecture seule, SQLite /tmp dédiée, e-mails en mémoire et connexions sortantes bloquées ; aucune migration de production ni envoi réel à un tiers.

SMTP distinct : dernier constat disponible backend console et CONTACT_TO absent ; délivrabilité et réception non testées. Aucune soumission de production.

## Procédure de livraison

Revue diff et ajout explicite ; branche dédiée seulement. SHA de commit inclus dans la métadonnée avant build, archive .output contrôlée par SHA-256 après transfert. Image construite depuis le runtime Nuxt effectivement exécuté sans installation/pull. Préflight sans réseau, puis surcharge externe delivery.yml conservée et up -d --no-deps --no-build nuxt. Comparer images ET conteneurs Django/PostgreSQL avant/après. Préparer rollback.yml vers l’image 14f858a avant bascule. Les SHA exacts, captures finales et contrôles publics figurent dans le compte rendu de livraison ; un contrôle isolé ne vaut pas preuve de mise en ligne.
