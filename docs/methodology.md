# Méthodologie

## Principe général

Chaque étape s'appuie sur la précédente et est validée avant de passer à la
suivante — pas de nettoyage ni d'analyse à l'aveugle. Principe directeur du
nettoyage : **ne rien supprimer par défaut sans l'avoir d'abord
caractérisé** (une quantité négative ou un prix nul n'est pas
automatiquement une erreur, voir `data_quality_report.md`).

## Étapes suivies

### 1. Audit initial
Inventaire brut du dataset (dimensions, types, période, valeurs manquantes,
doublons, prix nuls, quantités négatives, factures annulées, cardinalités)
avant toute décision de nettoyage. Objectif : constater, pas corriger.

### 2. Évaluation approfondie de la qualité
Approfondissement ciblé sur les points sensibles identifiés à l'étape 1 :
pays incohérents, descriptions multiples par produit, distributions des
quantités/prix, doublons exacts vs potentiels.

### 3. Nettoyage
Application des règles de nettoyage décidées, sous forme de fonctions
réutilisables (`src/clean_transactions.py`) plutôt que de code one-off dans
un notebook — testables et applicables de façon identique à chaque
exécution.

### 4. Analyse descriptive
Ventes, clients, produits — construction d'indicateurs à partir des
transactions nettoyées, sans encore de modélisation prédictive (conforme à
la section "Périmètre de la première version" du plan de projet).

### 5. Segmentation et rétention
RFM (Récence, Fréquence, Montant) calculé sur les ventes valides
uniquement, scores par quintile ; cohortes définies par le mois du premier
achat.

### 6. Modélisation SQL
Schéma en étoile (dimensions + table de faits) pour démontrer une
architecture de données relationnelle, indépendamment de l'analyse Python.

### 7. Restitution
Dashboard Power BI construit sur les données nettoyées (CSV), pas sur la
base SQL (voir `limitations.md` — la base SQL n'a été validée que sur un
échantillon).

## Séparation notebooks / code réutilisable

Le code stabilisé est déplacé de `notebooks/` vers `src/` dès qu'il est
réutilisé plusieurs fois (ex. chargement, classification des transactions,
calcul RFM) — les notebooks appellent ce code, ils ne dupliquent pas la
logique.

## Workflow Git

Développement par branches de fonctionnalité (`feature/...`), fusionnées
dans `develop` via Pull Request ; `main` ne reçoit que des versions
stables. Commits par petite unité logique, préfixés (`feat`, `fix`, `docs`,
`test`, `chore`).
