/** Grille publique : aucun montant n’est publié sans confirmation métier. */
export type DeviceFamily = 'laptop' | 'desktop' | 'phone' | 'tablet' | 'console' | 'controller' | 'other';
export type Estimate =
  | { kind: 'fixed'; amount: number; includes: string[]; excludes: string[] }
  | { kind: 'range'; min: number; max: number; includes: string[]; excludes: string[] }
  | { kind: 'diagnostic'; amount: number; deduction: string; includes: string[]; excludes: string[] }
  | { kind: 'unavailable'; reason: string };
export type RepairOffer = {
  id: string; families: DeviceFamily[]; symptoms: string[]; label: string; estimate: Exclude<Estimate, { kind: 'unavailable' }>;
  scope: string; condition?: string; quoteCases: string[]; published: boolean; replacesPart: boolean; precision?: string;
};
export type RepairGrid = { version: string; date: string; source: string; offers: RepairOffer[] };
export const deviceFamilies: readonly { id: DeviceFamily; label: string; active: boolean }[] = [
  { id: 'laptop', label: 'Ordinateur portable', active: true },
  { id: 'desktop', label: 'Ordinateur fixe', active: true },
  { id: 'phone', label: 'Téléphone', active: true },
  { id: 'tablet', label: 'Tablette', active: true },
  { id: 'console', label: 'Console de jeu', active: true },
  { id: 'controller', label: 'Manette', active: true },
  { id: 'other', label: 'Autre appareil', active: false },
];
export type Symptom = { id: string; label: string; electronic?: boolean };
const common: Symptom[] = [{ id: 'other', label: 'Autre problème' }, { id: 'unknown', label: 'Je ne sais pas' }];
const computer: Symptom[] = [
  { id: 'power', label: 'Ne démarre plus', electronic: true }, { id: 'heat', label: 'Chauffe ou fait du bruit' },
  { id: 'slow', label: 'Ralentit' }, { id: 'screen', label: 'Écran endommagé' },
  { id: 'charge', label: 'Ne charge plus', electronic: true }, { id: 'keyboard', label: 'Clavier défaillant' }, ...common,
];
const mobile: Symptom[] = [
  { id: 'screen', label: 'Écran cassé' }, { id: 'battery', label: 'Autonomie faible' },
  { id: 'charge', label: 'Ne charge plus', electronic: true }, { id: 'power', label: 'Ne s’allume plus', electronic: true },
  { id: 'sound', label: 'Problème de son' }, { id: 'liquid', label: 'Contact avec un liquide', electronic: true }, ...common,
];
export const symptomsByFamily: Record<DeviceFamily, readonly Symptom[]> = {
  laptop: [...computer.slice(0, 6), { id: 'battery', label: 'Autonomie faible' }, { id: 'liquid', label: 'Contact avec un liquide', electronic: true }, ...common], desktop: [...computer.filter(s => s.id !== 'charge' && !['other', 'unknown'].includes(s.id)), { id: 'charge', label: 'Prise d’alimentation endommagée', electronic: true }, { id: 'liquid', label: 'Contact avec un liquide', electronic: true }, ...common], phone: mobile, tablet: mobile,
  console: [{ id: 'power', label: 'Ne démarre plus', electronic: true }, { id: 'image', label: 'Aucune image' }, { id: 'heat', label: 'Surchauffe' }, { id: 'read', label: 'Problème de lecture' }, { id: 'connector', label: 'Connecteur endommagé', electronic: true }, { id: 'liquid', label: 'Contact avec un liquide', electronic: true }, ...common],
  controller: [{ id: 'drift', label: 'Joystick qui dérive' }, { id: 'button', label: 'Bouton défaillant' }, { id: 'charge', label: 'Ne charge plus', electronic: true }, { id: 'connection', label: 'Problème de connexion' }, { id: 'liquid', label: 'Contact avec un liquide', electronic: true }, ...common], other: common,
};
/** Montants consommateurs autorisés par l’instruction métier du 6 octobre 2026, en centimes. Aucun modèle techniquement validé n’est déduit de cette autorisation. */
export const publishedRepairGrid: RepairGrid = {
  "version": "reparation-20261006-v2-tarifs",
  "date": "2026-10-06",
  "source": "Instruction métier Pixelprowlers du 6 octobre 2026",
  "offers": [
    {
      "id": "orientation",
      "families": [
        "laptop",
        "desktop",
        "phone",
        "tablet",
        "console",
        "controller"
      ],
      "symptoms": [],
      "label": "Orientation à partir du modèle et du symptôme",
      "estimate": {
        "kind": "fixed",
        "includes": [
          "Première estimation sans démontage ni recherche technique"
        ],
        "excludes": [],
        "amount": 0
      },
      "scope": "Première estimation sans démontage ni recherche technique",
      "quoteCases": [],
      "published": true,
      "replacesPart": false
    },
    {
      "id": "diagnostic-standard",
      "families": [
        "laptop",
        "desktop",
        "phone",
        "tablet",
        "console",
        "controller"
      ],
      "symptoms": [
        "unknown",
        "other"
      ],
      "label": "Diagnostic standard",
      "estimate": {
        "kind": "diagnostic",
        "includes": [
          "Jusqu’à 30 minutes de travail actif, tests initiaux et devis ou bilan"
        ],
        "excludes": [],
        "amount": 4900,
        "deduction": "Le diagnostic est déduit du montant total si vous faites réaliser la réparation."
      },
      "scope": "Jusqu’à 30 minutes de travail actif, tests initiaux et devis ou bilan",
      "quoteCases": [],
      "published": true,
      "replacesPart": false
    },
    {
      "id": "diagnostic-electronique",
      "families": [
        "laptop",
        "desktop",
        "phone",
        "tablet",
        "console",
        "controller"
      ],
      "symptoms": [
        "power",
        "liquid"
      ],
      "label": "Diagnostic électronique approfondi",
      "estimate": {
        "kind": "diagnostic",
        "includes": [
          "Jusqu’à 60 minutes de travail actif, mesures sur carte mère et devis ou bilan"
        ],
        "excludes": [],
        "amount": 8900,
        "deduction": "Le diagnostic est déduit du montant total si vous faites réaliser la réparation."
      },
      "scope": "Jusqu’à 60 minutes de travail actif, mesures sur carte mère et devis ou bilan",
      "quoteCases": [],
      "published": true,
      "replacesPart": false
    },
    {
      "id": "phone-port-clean",
      "families": [
        "phone"
      ],
      "symptoms": [
        "charge"
      ],
      "label": "Nettoyage du port de charge",
      "estimate": {
        "kind": "fixed",
        "includes": [
          "Port encrassé, sans remplacement ni réparation électronique"
        ],
        "excludes": [],
        "amount": 3900
      },
      "scope": "Port encrassé, sans remplacement ni réparation électronique",
      "quoteCases": [],
      "published": true,
      "replacesPart": false
    },
    {
      "id": "phone-battery",
      "families": [
        "phone"
      ],
      "symptoms": [
        "battery"
      ],
      "label": "Batterie compatible",
      "estimate": {
        "kind": "range",
        "includes": [
          "Batterie documentée, adhésifs, pose et tests"
        ],
        "excludes": [
          "Pièce constructeur chiffrée séparément.",
          "Modèles très récents, pièces coûteuses, cartes empilées complexes et dégâts multiples : devis spécifique."
        ],
        "min": 8900,
        "max": 12900
      },
      "scope": "Batterie documentée, adhésifs, pose et tests",
      "quoteCases": [
        "Pièce constructeur chiffrée séparément.",
        "Modèles très récents, pièces coûteuses, cartes empilées complexes et dégâts multiples : devis spécifique."
      ],
      "published": true,
      "replacesPart": true,
      "condition": "Batterie compatible documentée ; pièce constructeur chiffrée séparément."
    },
    {
      "id": "phone-screen-lcd",
      "families": [
        "phone"
      ],
      "symptoms": [
        "screen"
      ],
      "label": "Écran LCD compatible",
      "estimate": {
        "kind": "range",
        "includes": [
          "Appareil équipé de LCD ; pose et tests"
        ],
        "excludes": [
          "Aucun remplacement d’un écran OLED par un LCD.",
          "Modèles très récents, pièces coûteuses, cartes empilées complexes et dégâts multiples : devis spécifique."
        ],
        "min": 9900,
        "max": 15900
      },
      "scope": "Appareil équipé de LCD ; pose et tests",
      "quoteCases": [
        "Aucun remplacement d’un écran OLED par un LCD.",
        "Modèles très récents, pièces coûteuses, cartes empilées complexes et dégâts multiples : devis spécifique."
      ],
      "published": true,
      "replacesPart": true,
      "precision": "lcd",
      "condition": "Appareil LCD uniquement ; jamais de LCD à la place d’un OLED."
    },
    {
      "id": "phone-screen-oled",
      "families": [
        "phone"
      ],
      "symptoms": [
        "screen"
      ],
      "label": "Écran OLED compatible",
      "estimate": {
        "kind": "range",
        "includes": [
          "Technologie et référence précisées ; pose et tests"
        ],
        "excludes": [
          "Modèles très récents, pièces coûteuses, cartes empilées complexes et dégâts multiples : devis spécifique."
        ],
        "min": 14900,
        "max": 23900
      },
      "scope": "Technologie et référence précisées ; pose et tests",
      "quoteCases": [
        "Modèles très récents, pièces coûteuses, cartes empilées complexes et dégâts multiples : devis spécifique."
      ],
      "published": true,
      "replacesPart": true,
      "precision": "oled",
      "condition": "Technologie et référence précisées au devis."
    },
    {
      "id": "phone-screen-original",
      "families": [
        "phone"
      ],
      "symptoms": [
        "screen"
      ],
      "label": "Écran d’origine ou reconditionné d’origine",
      "estimate": {
        "kind": "range",
        "includes": [
          "Origine et état documentés ; origine reconditionnée et Service Pack distingués au devis"
        ],
        "excludes": [
          "Modèles très récents, pièces coûteuses, cartes empilées complexes et dégâts multiples : devis spécifique."
        ],
        "min": 21900,
        "max": 44900
      },
      "scope": "Origine et état documentés ; origine reconditionnée et Service Pack distingués au devis",
      "quoteCases": [
        "Modèles très récents, pièces coûteuses, cartes empilées complexes et dégâts multiples : devis spécifique."
      ],
      "published": true,
      "replacesPart": true,
      "precision": "original",
      "condition": "Origine et état documentés ; type d’origine précisé au devis."
    },
    {
      "id": "phone-charge-module",
      "families": [
        "phone"
      ],
      "symptoms": [
        "charge"
      ],
      "label": "Module de charge amovible",
      "estimate": {
        "kind": "range",
        "includes": [
          "Nappe ou module, pose et tests"
        ],
        "excludes": [
          "Carte mère hors périmètre.",
          "Modèles très récents, pièces coûteuses, cartes empilées complexes et dégâts multiples : devis spécifique."
        ],
        "min": 9900,
        "max": 15900
      },
      "scope": "Nappe ou module, pose et tests",
      "quoteCases": [
        "Carte mère hors périmètre.",
        "Modèles très récents, pièces coûteuses, cartes empilées complexes et dégâts multiples : devis spécifique."
      ],
      "published": true,
      "replacesPart": true,
      "condition": "Carte mère hors périmètre."
    },
    {
      "id": "phone-charge-soldered",
      "families": [
        "phone"
      ],
      "symptoms": [
        "charge"
      ],
      "label": "Connecteur de charge soudé",
      "estimate": {
        "kind": "range",
        "includes": [
          "Connecteur, micro-soudure et tests ; pistes intactes"
        ],
        "excludes": [
          "Modèles très récents, pièces coûteuses, cartes empilées complexes et dégâts multiples : devis spécifique."
        ],
        "min": 13900,
        "max": 20900
      },
      "scope": "Connecteur, micro-soudure et tests ; pistes intactes",
      "quoteCases": [
        "Modèles très récents, pièces coûteuses, cartes empilées complexes et dégâts multiples : devis spécifique."
      ],
      "published": true,
      "replacesPart": true,
      "condition": "Pistes intactes ; cas complexes sur devis spécifique."
    },
    {
      "id": "phone-board",
      "families": [
        "phone"
      ],
      "symptoms": [
        "power",
        "charge"
      ],
      "label": "Réparation électronique de carte mère",
      "estimate": {
        "kind": "range",
        "includes": [
          "Défaut localisé, recherche, composants courants et tests"
        ],
        "excludes": [
          "Modèles très récents, pièces coûteuses, cartes empilées complexes et dégâts multiples : devis spécifique.",
          "Remplacement complet de carte, intervention lourde CPU/GPU/BGA et récupération de données hors périmètre."
        ],
        "min": 16900,
        "max": 29900
      },
      "scope": "Défaut localisé, recherche, composants courants et tests",
      "quoteCases": [
        "Modèles très récents, pièces coûteuses, cartes empilées complexes et dégâts multiples : devis spécifique.",
        "Remplacement complet de carte, intervention lourde CPU/GPU/BGA et récupération de données hors périmètre."
      ],
      "published": true,
      "replacesPart": true,
      "condition": "Défaut localisé ; carte complète, CPU/GPU/BGA et récupération de données exclus."
    },
    {
      "id": "tablet-battery",
      "families": [
        "tablet"
      ],
      "symptoms": [
        "battery"
      ],
      "label": "Batterie",
      "estimate": {
        "kind": "range",
        "includes": [
          "Batterie, adhésifs, démontage, remontage et tests sur modèle accessible"
        ],
        "excludes": [],
        "min": 13900,
        "max": 21900
      },
      "scope": "Batterie, adhésifs, démontage, remontage et tests sur modèle accessible",
      "quoteCases": [],
      "published": true,
      "replacesPart": true,
      "condition": "Sur modèle accessible."
    },
    {
      "id": "tablet-screen-lcd",
      "families": [
        "tablet"
      ],
      "symptoms": [
        "screen"
      ],
      "label": "Écran LCD ou ensemble vitre et LCD",
      "estimate": {
        "kind": "range",
        "includes": [
          "Ensemble correspondant à la panne, pose et tests"
        ],
        "excludes": [
          "Aucun remplacement d’un écran OLED par un LCD."
        ],
        "min": 14900,
        "max": 24900
      },
      "scope": "Ensemble correspondant à la panne, pose et tests",
      "quoteCases": [
        "Aucun remplacement d’un écran OLED par un LCD."
      ],
      "published": true,
      "replacesPart": true,
      "precision": "lcd",
      "condition": "Ensemble adapté à la panne ; pas de LCD à la place d’un OLED."
    },
    {
      "id": "tablet-screen-oled",
      "families": [
        "tablet"
      ],
      "symptoms": [
        "screen"
      ],
      "label": "Écran OLED ou haut de gamme",
      "estimate": {
        "kind": "range",
        "includes": [
          "Pièce, pose et tests"
        ],
        "excludes": [
          "Certains modèles nécessitent un devis spécifique."
        ],
        "min": 22900,
        "max": 47900
      },
      "scope": "Pièce, pose et tests",
      "quoteCases": [
        "Certains modèles nécessitent un devis spécifique."
      ],
      "published": true,
      "replacesPart": true,
      "precision": "oled",
      "condition": "Certains modèles nécessitent un devis spécifique."
    },
    {
      "id": "tablet-charge-soldered",
      "families": [
        "tablet"
      ],
      "symptoms": [
        "charge"
      ],
      "label": "Connecteur de charge soudé",
      "estimate": {
        "kind": "range",
        "includes": [
          "Connecteur, soudures et tests ; pistes intactes"
        ],
        "excludes": [],
        "min": 15900,
        "max": 24900
      },
      "scope": "Connecteur, soudures et tests ; pistes intactes",
      "quoteCases": [],
      "published": true,
      "replacesPart": true,
      "condition": "Pistes intactes."
    },
    {
      "id": "desktop-thermal",
      "families": [
        "desktop"
      ],
      "symptoms": [
        "heat"
      ],
      "label": "Entretien thermique standard PC fixe",
      "estimate": {
        "kind": "fixed",
        "includes": [
          "Dépoussiérage, pâte thermique CPU et tests ; refroidissement standard"
        ],
        "excludes": [],
        "amount": 7900
      },
      "scope": "Dépoussiérage, pâte thermique CPU et tests ; refroidissement standard",
      "quoteCases": [],
      "published": true,
      "replacesPart": false
    },
    {
      "id": "laptop-thermal",
      "families": [
        "laptop"
      ],
      "symptoms": [
        "heat"
      ],
      "label": "Entretien thermique standard PC portable",
      "estimate": {
        "kind": "fixed",
        "includes": [
          "Portable accessible, dépoussiérage, pâte thermique et tests"
        ],
        "excludes": [
          "Métal liquide et ventilateur neuf exclus."
        ],
        "amount": 9900
      },
      "scope": "Portable accessible, dépoussiérage, pâte thermique et tests",
      "quoteCases": [
        "Métal liquide et ventilateur neuf exclus."
      ],
      "published": true,
      "replacesPart": false
    },
    {
      "id": "laptop-thermal-complex",
      "families": [
        "laptop"
      ],
      "symptoms": [
        "heat"
      ],
      "label": "Entretien thermique complexe PC portable",
      "estimate": {
        "kind": "range",
        "includes": [
          "Démontage avancé et produits thermiques adaptés"
        ],
        "excludes": [],
        "min": 14900,
        "max": 19900
      },
      "scope": "Démontage avancé et produits thermiques adaptés",
      "quoteCases": [],
      "published": true,
      "replacesPart": false
    },
    {
      "id": "computer-software",
      "families": [
        "laptop",
        "desktop"
      ],
      "symptoms": [
        "slow"
      ],
      "label": "Nettoyage logiciel et optimisation",
      "estimate": {
        "kind": "range",
        "includes": [
          "Recherche de causes logicielles, nettoyage et tests"
        ],
        "excludes": [
          "Pièces et réinstallation exclues."
        ],
        "min": 8900,
        "max": 12900
      },
      "scope": "Recherche de causes logicielles, nettoyage et tests",
      "quoteCases": [
        "Pièces et réinstallation exclues."
      ],
      "published": true,
      "replacesPart": false
    },
    {
      "id": "computer-reinstall",
      "families": [
        "laptop",
        "desktop"
      ],
      "symptoms": [],
      "label": "Réinstallation du système",
      "estimate": {
        "kind": "fixed",
        "includes": [
          "Installation, pilotes et tests avec licence valide existante"
        ],
        "excludes": [
          "Sauvegarde et licence nouvelle exclues."
        ],
        "amount": 11900
      },
      "scope": "Installation, pilotes et tests avec licence valide existante",
      "quoteCases": [
        "Sauvegarde et licence nouvelle exclues."
      ],
      "published": true,
      "replacesPart": false
    },
    {
      "id": "computer-reinstall-transfer",
      "families": [
        "laptop",
        "desktop"
      ],
      "symptoms": [],
      "label": "Réinstallation avec transfert de fichiers",
      "estimate": {
        "kind": "range",
        "includes": [
          "Jusqu’à 250 Go de fichiers lisibles sur support sain"
        ],
        "excludes": [
          "Récupération de données et licence nouvelle exclues."
        ],
        "min": 16900,
        "max": 21900
      },
      "scope": "Jusqu’à 250 Go de fichiers lisibles sur support sain",
      "quoteCases": [
        "Récupération de données et licence nouvelle exclues."
      ],
      "published": true,
      "replacesPart": false
    },
    {
      "id": "computer-ssd",
      "families": [
        "laptop",
        "desktop"
      ],
      "symptoms": [],
      "label": "SSD 500 Go installé, sans transfert",
      "estimate": {
        "kind": "range",
        "includes": [
          "SSD compatible, montage et tests"
        ],
        "excludes": [
          "Système et transfert exclus."
        ],
        "min": 9900,
        "max": 16900
      },
      "scope": "SSD compatible, montage et tests",
      "quoteCases": [
        "Système et transfert exclus."
      ],
      "published": true,
      "replacesPart": true,
      "condition": "Système et transfert exclus."
    },
    {
      "id": "computer-ssd-clone",
      "families": [
        "laptop",
        "desktop"
      ],
      "symptoms": [
        "slow"
      ],
      "label": "SSD 500 Go installé avec clonage",
      "estimate": {
        "kind": "range",
        "includes": [
          "SSD compatible, clonage jusqu’à 250 Go sur source saine et tests"
        ],
        "excludes": [],
        "min": 14900,
        "max": 22900
      },
      "scope": "SSD compatible, clonage jusqu’à 250 Go sur source saine et tests",
      "quoteCases": [],
      "published": true,
      "replacesPart": true,
      "condition": "Clonage jusqu’à 250 Go depuis une source saine."
    },
    {
      "id": "laptop-battery",
      "families": [
        "laptop"
      ],
      "symptoms": [
        "battery"
      ],
      "label": "Batterie PC portable",
      "estimate": {
        "kind": "range",
        "includes": [
          "Batterie compatible documentée, pose et tests"
        ],
        "excludes": [],
        "min": 9900,
        "max": 16900
      },
      "scope": "Batterie compatible documentée, pose et tests",
      "quoteCases": [],
      "published": true,
      "replacesPart": true,
      "condition": "Batterie compatible documentée."
    },
    {
      "id": "laptop-screen",
      "families": [
        "laptop"
      ],
      "symptoms": [
        "screen"
      ],
      "label": "Écran PC portable standard",
      "estimate": {
        "kind": "range",
        "includes": [
          "Dalle LCD standard compatible, pose et tests"
        ],
        "excludes": [
          "Tactile, OLED et ensemble Apple exclus."
        ],
        "min": 14900,
        "max": 25900
      },
      "scope": "Dalle LCD standard compatible, pose et tests",
      "quoteCases": [
        "Tactile, OLED et ensemble Apple exclus."
      ],
      "published": true,
      "replacesPart": true,
      "condition": "LCD standard ; tactile, OLED et ensemble Apple exclus."
    },
    {
      "id": "laptop-keyboard",
      "families": [
        "laptop"
      ],
      "symptoms": [
        "keyboard"
      ],
      "label": "Clavier PC portable accessible",
      "estimate": {
        "kind": "range",
        "includes": [
          "Clavier remplaçable, pièce et pose"
        ],
        "excludes": [
          "Topcase complet et clavier riveté : devis spécifique."
        ],
        "min": 12900,
        "max": 21900
      },
      "scope": "Clavier remplaçable, pièce et pose",
      "quoteCases": [
        "Topcase complet et clavier riveté : devis spécifique."
      ],
      "published": true,
      "replacesPart": true,
      "condition": "Topcase complet et clavier riveté sur devis."
    },
    {
      "id": "laptop-dcjack",
      "families": [
        "laptop",
        "desktop"
      ],
      "symptoms": [
        "charge"
      ],
      "label": "Connecteur d’alimentation DC-Jack soudé",
      "estimate": {
        "kind": "range",
        "includes": [
          "Connecteur, soudures et tests ; pistes intactes"
        ],
        "excludes": [],
        "min": 11900,
        "max": 17900
      },
      "scope": "Connecteur, soudures et tests ; pistes intactes",
      "quoteCases": [],
      "published": true,
      "replacesPart": true,
      "precision": "dcjack",
      "condition": "Pistes intactes."
    },
    {
      "id": "laptop-usbc",
      "families": [
        "laptop",
        "desktop"
      ],
      "symptoms": [
        "charge"
      ],
      "label": "Connecteur USB-C soudé",
      "estimate": {
        "kind": "range",
        "includes": [
          "Connecteur, soudures et tests"
        ],
        "excludes": [
          "Circuit de charge et pistes arrachées : devis spécifique."
        ],
        "min": 14900,
        "max": 22900
      },
      "scope": "Connecteur, soudures et tests",
      "quoteCases": [
        "Circuit de charge et pistes arrachées : devis spécifique."
      ],
      "published": true,
      "replacesPart": true,
      "precision": "usbc",
      "condition": "Circuit de charge et pistes arrachées sur devis."
    },
    {
      "id": "computer-bios",
      "families": [
        "laptop",
        "desktop"
      ],
      "symptoms": [],
      "label": "Reprogrammation BIOS au programmateur",
      "estimate": {
        "kind": "range",
        "includes": [
          "Reprogrammation compatible et tests"
        ],
        "excludes": [
          "EC et autres cas complexes : devis spécifique."
        ],
        "min": 14900,
        "max": 19900
      },
      "scope": "Reprogrammation compatible et tests",
      "quoteCases": [
        "EC et autres cas complexes : devis spécifique."
      ],
      "published": true,
      "replacesPart": false
    },
    {
      "id": "computer-board",
      "families": [
        "laptop",
        "desktop"
      ],
      "symptoms": [
        "power"
      ],
      "label": "Réparation électronique de carte mère PC",
      "estimate": {
        "kind": "range",
        "includes": [
          "Défaut localisé, recherche, composants courants, micro-soudure et tests"
        ],
        "excludes": [
          "Remplacement complet de carte, intervention lourde CPU/GPU/BGA et récupération de données hors périmètre."
        ],
        "min": 21900,
        "max": 37900
      },
      "scope": "Défaut localisé, recherche, composants courants, micro-soudure et tests",
      "quoteCases": [
        "Remplacement complet de carte, intervention lourde CPU/GPU/BGA et récupération de données hors périmètre."
      ],
      "published": true,
      "replacesPart": true,
      "precision": "pc",
      "condition": "Défaut localisé ; carte complète, CPU/GPU/BGA et récupération de données exclus."
    },
    {
      "id": "macbook-board",
      "families": [
        "laptop"
      ],
      "symptoms": [
        "power"
      ],
      "label": "Réparation électronique de carte mère MacBook",
      "estimate": {
        "kind": "range",
        "includes": [
          "Recherche et réparation d’un circuit localisé"
        ],
        "excludes": [
          "Remplacement complet de carte, intervention lourde CPU/GPU/BGA et récupération de données hors périmètre."
        ],
        "min": 29900,
        "max": 49900
      },
      "scope": "Recherche et réparation d’un circuit localisé",
      "quoteCases": [
        "Remplacement complet de carte, intervention lourde CPU/GPU/BGA et récupération de données hors périmètre."
      ],
      "published": true,
      "replacesPart": true,
      "precision": "macbook",
      "condition": "Circuit localisé ; carte complète, CPU/GPU/BGA et récupération de données exclus."
    },
    {
      "id": "console-thermal",
      "families": [
        "console"
      ],
      "symptoms": [
        "heat"
      ],
      "label": "Entretien thermique standard",
      "estimate": {
        "kind": "range",
        "includes": [
          "Nettoyage, produits thermiques adaptés et tests"
        ],
        "excludes": [
          "Traitement complexe au métal liquide et ventilateur neuf exclus."
        ],
        "min": 9900,
        "max": 14900
      },
      "scope": "Nettoyage, produits thermiques adaptés et tests",
      "quoteCases": [
        "Traitement complexe au métal liquide et ventilateur neuf exclus."
      ],
      "published": true,
      "replacesPart": false
    },
    {
      "id": "console-hdmi-ps4-xbox",
      "families": [
        "console"
      ],
      "symptoms": [
        "image",
        "connector"
      ],
      "label": "Port HDMI PS4 / Xbox",
      "estimate": {
        "kind": "range",
        "includes": [
          "Connecteur, micro-soudure et tests ; pistes intactes"
        ],
        "excludes": [],
        "min": 12900,
        "max": 17900
      },
      "scope": "Connecteur, micro-soudure et tests ; pistes intactes",
      "quoteCases": [],
      "published": true,
      "replacesPart": true,
      "precision": "ps4-xbox",
      "condition": "Pistes intactes."
    },
    {
      "id": "console-hdmi-ps5",
      "families": [
        "console"
      ],
      "symptoms": [
        "image",
        "connector"
      ],
      "label": "Port HDMI PS5",
      "estimate": {
        "kind": "range",
        "includes": [
          "Connecteur, micro-soudure et tests ; pistes intactes"
        ],
        "excludes": [],
        "min": 15900,
        "max": 19900
      },
      "scope": "Connecteur, micro-soudure et tests ; pistes intactes",
      "quoteCases": [],
      "published": true,
      "replacesPart": true,
      "precision": "ps5",
      "condition": "Pistes intactes."
    },
    {
      "id": "console-usbc-switch",
      "families": [
        "console"
      ],
      "symptoms": [
        "connector"
      ],
      "label": "Port USB-C Nintendo Switch",
      "estimate": {
        "kind": "range",
        "includes": [
          "Connecteur et tests"
        ],
        "excludes": [
          "Batterie, circuit de charge et pistes arrachées hors périmètre."
        ],
        "min": 13900,
        "max": 18900
      },
      "scope": "Connecteur et tests",
      "quoteCases": [
        "Batterie, circuit de charge et pistes arrachées hors périmètre."
      ],
      "published": true,
      "replacesPart": true,
      "precision": "switch",
      "condition": "Batterie, circuit de charge et pistes arrachées hors périmètre."
    },
    {
      "id": "console-board",
      "families": [
        "console"
      ],
      "symptoms": [
        "power"
      ],
      "label": "Réparation électronique de carte mère",
      "estimate": {
        "kind": "range",
        "includes": [
          "Défaut localisé, composants courants et tests"
        ],
        "excludes": [
          "APU/BGA et carte complète hors périmètre."
        ],
        "min": 21900,
        "max": 34900
      },
      "scope": "Défaut localisé, composants courants et tests",
      "quoteCases": [
        "APU/BGA et carte complète hors périmètre."
      ],
      "published": true,
      "replacesPart": true,
      "condition": "Défaut localisé ; APU/BGA et carte complète exclus."
    },
    {
      "id": "controller-drift-one",
      "families": [
        "controller"
      ],
      "symptoms": [
        "drift"
      ],
      "label": "Drift : un joystick",
      "estimate": {
        "kind": "range",
        "includes": [
          "Module conventionnel compatible, pose, calibration et tests"
        ],
        "excludes": [],
        "min": 5900,
        "max": 7900
      },
      "scope": "Module conventionnel compatible, pose, calibration et tests",
      "quoteCases": [],
      "published": true,
      "replacesPart": true,
      "precision": "one",
      "condition": "Module conventionnel compatible ; calibration comprise."
    },
    {
      "id": "controller-drift-two",
      "families": [
        "controller"
      ],
      "symptoms": [
        "drift"
      ],
      "label": "Drift : deux joysticks",
      "estimate": {
        "kind": "range",
        "includes": [
          "Deux modules conventionnels compatibles, pose, calibration et tests"
        ],
        "excludes": [],
        "min": 8900,
        "max": 10900
      },
      "scope": "Deux modules conventionnels compatibles, pose, calibration et tests",
      "quoteCases": [],
      "published": true,
      "replacesPart": true,
      "precision": "two",
      "condition": "Modules conventionnels compatibles ; calibration comprise."
    },
    {
      "id": "controller-charge",
      "families": [
        "controller"
      ],
      "symptoms": [
        "charge"
      ],
      "label": "Port de charge",
      "estimate": {
        "kind": "range",
        "includes": [
          "Connecteur ou module, pose et tests sur modèle accessible"
        ],
        "excludes": [],
        "min": 5900,
        "max": 8900
      },
      "scope": "Connecteur ou module, pose et tests sur modèle accessible",
      "quoteCases": [],
      "published": true,
      "replacesPart": true,
      "condition": "Sur modèle accessible."
    },
    {
      "id": "controller-hall-tmr",
      "families": [
        "controller"
      ],
      "symptoms": [
        "drift"
      ],
      "label": "Deux joysticks Hall/TMR compatibles",
      "estimate": {
        "kind": "range",
        "includes": [
          "Kit, compatibilité, calibration et prestation réelle à valider"
        ],
        "excludes": [],
        "min": 8900,
        "max": 11900
      },
      "scope": "Kit, compatibilité, calibration et prestation réelle à valider",
      "quoteCases": [],
      "published": false,
      "replacesPart": true
    },
    {
      "id": "liquid-treatment",
      "families": [
        "laptop",
        "desktop",
        "phone",
        "tablet",
        "console",
        "controller"
      ],
      "symptoms": [
        "liquid"
      ],
      "label": "Traitement après contact avec un liquide",
      "estimate": {
        "kind": "range",
        "includes": [
          "Démontage, nettoyage des zones atteintes et tests"
        ],
        "excludes": [
          "Réparation de composants chiffrée séparément. Aucune remise en fonctionnement promise."
        ],
        "min": 14900,
        "max": 24900
      },
      "scope": "Démontage, nettoyage des zones atteintes et tests",
      "quoteCases": [
        "Réparation de composants chiffrée séparément. Aucune remise en fonctionnement promise."
      ],
      "published": true,
      "replacesPart": false
    }
  ]
};
export const consumerPriceNote = 'Prix consommateurs, toutes taxes comprises lorsqu’une TVA s’applique.';
export const diagnosticDeduction = 'Le diagnostic est déduit du montant total si vous faites réaliser la réparation.';
/** Valide des montants entiers en centimes, sans convertir une absence en zéro. */
export function validEstimate(estimate: Estimate): boolean {
  if (estimate.kind === 'unavailable') return true;
  const money = (value: number) => Number.isSafeInteger(value) && value >= 0;
  return estimate.kind === 'range' ? money(estimate.min) && money(estimate.max) && estimate.max >= estimate.min : money(estimate.amount);
}
/** Formate des centimes en euros, sans conversion de TVA ni addition d’alternatives. */
export function budgetLabel(estimate: Estimate): string {
  const euro = (cents: number) => new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR', minimumFractionDigits: 0, maximumFractionDigits: 2 }).format(cents / 100);
  if (!validEstimate(estimate)) return 'Estimation indisponible';
  if (estimate.kind === 'unavailable') return 'Estimation après diagnostic';
  if (estimate.kind === 'range') return `${euro(estimate.min)} à ${euro(estimate.max)}`;
  return estimate.amount === 0 ? 'Gratuite' : euro(estimate.amount);
}
/** Calcule seulement le solde de l’exemple : le diagnostic payé est déduit, jamais ajouté. */
export function diagnosticSettlement(totalCents: number, paidCents: number) {
  if (![totalCents, paidCents].every(n => Number.isSafeInteger(n) && n >= 0)) throw new Error('Montants invalides');
  return { remaining: Math.max(0, totalCents - paidCents), refundOrCredit: Math.max(0, paidCents - totalCents) };
}
export type PrecisionOption = { id: string; label: string };
/** Demande uniquement une information observable qui change les scénarios, jamais une référence obligatoire. */
export function precisionOptions(family: DeviceFamily | '', symptom: string): PrecisionOption[] {
  let choices: PrecisionOption[] = [];
  if ((family === 'phone' || family === 'tablet') && symptom === 'screen') choices = [{ id: 'lcd', label: 'LCD, si mon appareil en est équipé' }, { id: 'oled', label: 'OLED ou haut de gamme' }, ...(family === 'phone' ? [{ id: 'original', label: 'Écran d’origine ou reconditionné d’origine' }] : [])];
  if (family === 'console' && ['image', 'connector'].includes(symptom)) choices = [{ id: 'ps4-xbox', label: 'PS4 ou Xbox' }, { id: 'ps5', label: 'PS5' }, { id: 'switch', label: 'Nintendo Switch' }];
  if (family === 'controller' && symptom === 'drift') choices = [{ id: 'one', label: 'Un joystick' }, { id: 'two', label: 'Deux joysticks' }];
  if (family === 'laptop' && symptom === 'power') choices = [{ id: 'pc', label: 'PC portable' }, { id: 'macbook', label: 'MacBook' }];
  if ((family === 'laptop' || family === 'desktop') && symptom === 'charge') choices = [{ id: 'dcjack', label: 'Prise ronde DC-Jack' }, { id: 'usbc', label: 'USB-C' }];
  return choices.length ? [...choices, { id: 'unknown', label: 'Je ne sais pas' }] : [];
}
/** Filtre les offres publiables, sans considérer un modèle saisi comme une preuve de compatibilité. */
export function offersForFamily(grid: RepairGrid, family: DeviceFamily | '') {
  return grid.offers.filter(o => o.published && o.families.includes(family as DeviceFamily) && validEstimate(o.estimate));
}
/** Retourne des scénarios alternatifs, jamais une somme ni une cause de panne affirmée. */
export function resolveScenarios(grid: RepairGrid, family: DeviceFamily | '', symptom: string, precision = ''): { offers: RepairOffer[]; possible: RepairOffer[]; diagnosticFirst: boolean } {
  if (!deviceFamilies.some(f => f.id === family && f.active) || !symptomsByFamily[family as DeviceFamily]?.some(s => s.id === symptom)) return { offers: [], possible: [], diagnosticFirst: true };
  const all = offersForFamily(grid, family);
  const diagnostic = all.filter(o => o.estimate.kind === 'diagnostic');
  let matching = all.filter(o => o.estimate.kind !== 'diagnostic' && o.symptoms.includes(symptom));
  const allowedPrecision = precisionOptions(family, symptom).some(p => p.id === precision) && precision !== 'unknown';
  if (allowedPrecision) matching = matching.filter(o => !o.precision || o.precision === precision);
  if (symptom === 'liquid') return { offers: diagnostic, possible: matching, diagnosticFirst: true };
  if (family === 'console' && ['image', 'connector'].includes(symptom) && !allowedPrecision) return { offers: diagnostic, possible: matching, diagnosticFirst: true };
  if (symptom === 'power') return { offers: diagnostic.filter(o => o.id === 'diagnostic-electronique'), possible: matching, diagnosticFirst: true };
  if (!matching.length) return { offers: diagnostic, possible: [], diagnosticFirst: true };
  return { offers: matching.slice(0, 3), possible: matching.slice(3), diagnosticFirst: false };
}

/** Données de l’exemple autorisé : aucune facturation ni conversion de TVA. */
export const diagnosticExampleTotalCents = 21900;
/** Lit les deux diagnostics de la source publique et calcule uniquement la déduction explicative. */
export function diagnosticPresentation(grid: RepairGrid) {
  const standard = grid.offers.find(o => o.id === 'diagnostic-standard');
  const deep = grid.offers.find(o => o.id === 'diagnostic-electronique');
  if (!standard || !deep || standard.estimate.kind !== 'diagnostic' || deep.estimate.kind !== 'diagnostic') throw new Error('Diagnostics manquants');
  const supplement = deep.estimate.amount - standard.estimate.amount;
  const settlement = diagnosticSettlement(diagnosticExampleTotalCents, deep.estimate.amount);
  const label = (amount: number) => budgetLabel({ kind: 'fixed', amount, includes: [], excludes: [] });
  return { standard: label(standard.estimate.amount), deep: label(deep.estimate.amount), supplement: label(supplement), total: label(diagnosticExampleTotalCents), remaining: label(settlement.remaining) };
}
