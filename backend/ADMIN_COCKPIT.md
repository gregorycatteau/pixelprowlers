# Administration PixelProwlers 1.0

## Décision d'interface

Jazzmin 3.0.5 est conservé sur Django 6.0.6. Il est déjà intégré, compatible
avec les ModelAdmin existants et suffit pour le tableau de bord, la navigation,
les badges et les formulaires structurés. Unfold apporterait une seconde
dépendance d'interface, une reprise des templates et un risque de migration sans
gain opérationnel démontré. L'Admin natif personnalisé réduirait les dépendances
mais demanderait de reconstruire les fonctions responsive et de navigation déjà
fournies par Jazzmin.

Les polices Google, le constructeur visuel Jazzmin et toute dépendance CDN sont
désactivés. Les assets sont collectés à la construction de l'image et servis par
WhiteNoise, car les routes statiques Admin répondaient 404 avant ce lot.

## Inventaire opérationnel

| App | Modèle | Admin | Utilité / sensibilité | Rôle et actions | Priorité |
|---|---|---|---|---|---|
| crm | Contact | Oui | Demandes et coordonnées sensibles | Opérations/Commercial ; statut, lecture, recherche | Critique |
| crm | ContactMessage | Oui, protégé | Échanges client | Opérations ; lecture, ajout contrôlé | Haute |
| crm | DiagnosticTicket | Oui | Diagnostic et coordonnées | Opérations/Direction ; suivi | Haute |
| crm | Lead | Oui | Prospects sensibles | Commercial ; statut | Haute |
| crm | Formation, FormationRegistration | Oui | Offre et inscriptions | Éditorial/Opérations | Moyenne |
| crm | Service | Oui | Référentiel interne | Éditorial | Moyenne |
| crm | ContactDailyCounter | Masqué, lecture seule | Compteur technique | Superuser seulement | Technique |
| urgencies | UrgencyRequest | Oui | Incident, coordonnées, risque sécurité | Opérations ; prise en charge/résolution | Critique |
| audits | ClientDossier | Oui | Dossier transversal sensible | Opérations/Direction ; phase | Critique |
| audits | DossierLog | Oui, lecture seule | Traçabilité | Direction | Haute |
| audits | AuditDossier, AuditReponse | Oui | Audit et preuves sensibles | Opérations ; réponse en lecture seule | Haute |
| audits | RefonteAudit | Oui | Rapports techniques | Opérations/Direction | Haute |
| audits | Rdv, RdvContact, RdvRappel | Oui | Planning et coordonnées | Opérations ; confirmer/annuler | Haute |
| audits | CreneauCalendrier, Motif, RaisonAppel | Oui | Disponibilités | Opérations/Éditorial | Haute |
| audits | Citation | Oui | Contenu public | Éditorial | Moyenne |
| audits | Compteurs, RdvRaison | Masqués | Implémentation technique | Pas de gestion manuelle | Technique |
| catalogue | RefurbishedMachine | Oui | Catalogue, prix, notes internes | Éditorial/Commercial ; transitions métier | Critique |
| tracking | VisitorSession, TrackingEvent | Lecture seule | IP, user-agent, navigation | Direction, accès exceptionnel | Sensible |
| tracking | PageView, QuestionInteraction | Masqués, lecture seule | Fort volume, télémétrie brute | Aucun usage quotidien | Technique |
| admin | LogEntry | Lecture seule | Journal administratif | Direction | Haute |
| auth | User, Group, Permission | Oui natif | Contrôle d'accès critique | Superuser uniquement au départ | Critique |

Les modèles non cités séparément sont des tables de liaison ou compteurs et ne
doivent pas être édités manuellement. La rétention du tracking reste à définir ;
aucune suppression automatique n'est ajoutée sans politique validée.

## Sécurité et accès

Route actuelle : `https://pixelprowlers.io/admin/`. Django n'est pas publié sur
un port hôte ; seul le proxy HTTPS atteint le service interne. Les cookies sont
Secure, HttpOnly et SameSite=Lax en production, la session expire avec le
navigateur et après huit heures, CSRF reste actif et l'Admin refuse les frames.

Cible recommandée, non improvisée dans ce lot :

`admin.pixelprowlers.io` → Caddy HTTPS 443 → Authelia MFA et limitation → Django Admin.

Le DNS, Caddy et Authelia ne sont pas configurés dans le dépôt. Leur ajout exige
une décision DNS, une sauvegarde de configuration et une validation externe.
Aucun port supplémentaire ne doit être ouvert. `TRUSTED_PROXY_IPS` doit être
renseigné avec l'adresse réelle du proxy avant d'ajouter un filtrage IP strict
des en-têtes transférés.

## Lots métier suivants

1. **Atelier indispensable** : dépôt matériel, numéro de série, état entrant,
   consentement d'accès, chaîne de possession, diagnostic, sauvegarde demandée
   et réalisée, restitution.
2. **Devis et intervention** : devis versionné, acceptation, interventions,
   pièces, tests de sortie et garantie.
3. **Pilotage CRM** : responsable assigné, prochaine action, notes internes,
   historique et tags, avec permissions et audit dédiés.
4. **Contenus** : FAQ, fourchettes de prix, ressources et paramètres publics.
5. **Preuves marketing** : cas clients et témoignages uniquement avec preuve de
   consentement de publication.

Paiement, facturation complète, CMS séparé et export massif de données sont
prématurés ou à ne pas construire sans besoin et gouvernance démontrés.

## Provisionnement administrateur

`python manage.py provision_admin --username striker` crée les quatre groupes et
crée ou met à niveau le compte demandé. Un compte nouvellement créé reçoit un
mot de passe inutilisable. Un mot de passe existant n'est jamais remplacé.

Le réglage définitif doit être réalisé dans un terminal interactif sûr :

`python manage.py changepassword striker`

Le secret ne doit être transmis ni dans Git, ni dans une commande non
interactive, ni dans un journal. Le futur compte quotidien doit appartenir à un
groupe de moindre privilège plutôt qu'utiliser le superuser.
