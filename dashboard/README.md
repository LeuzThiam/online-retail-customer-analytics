# Tableau de bord Power BI — Online Retail II

`online_retail_dashboard.pbix` (non versionné, voir `.gitignore` — fichier
binaire volumineux). Ce README documente son contenu pour quiconque n'a pas
accès au fichier lui-même.

## Sources de données

Le dashboard se connecte directement aux fichiers CSV dans `data/processed/` :

- `transactions_clean.csv` — table principale (grain = ligne de transaction),
  1 033 036 lignes
- `customers_rfm.csv` — segmentation RFM par client
- `cohort_retention.csv` — matrice de rétention par cohorte d'acquisition

Une table de dates (`DimDate`) est générée dans Power BI via DAX
(`CALENDAR`), avec une colonne `YearMonth` triée par `YearMonthSort` pour
garantir l'ordre chronologique des graphiques temporels.

## Pages

### 1. Vue exécutive
- KPI : chiffre d'affaires net, nombre de commandes, panier moyen, clients
  actifs, articles vendus, taux d'annulation
- Évolution mensuelle du chiffre d'affaires (décembre 2011 exclu, mois
  incomplet)
- Chiffre d'affaires par pays
- Top 10 produits par chiffre d'affaires

### 2. RFM
- Répartition des clients par segment (Champions, Clients fidèles, Gros
  acheteurs, Nouveaux clients, À risque, Perdus, Clients réguliers)
- Chiffre d'affaires par segment
- Liste des clients Champions et des clients à risque (triés par valeur)

### 3. Cohortes
- Matrice de rétention (mois d'acquisition × mois écoulés depuis le premier
  achat)

### 4. Clients
- KPI : nombre de clients, clients à achat unique, fréquence moyenne, valeur
  moyenne par client
- Top 10 clients par chiffre d'affaires

## Mesures DAX

Voir `dashboard/measures.dax` pour le détail. Mesures principales :
`Net Revenue`, `Gross Revenue`, `Cancelled Value`, `Number of Orders`,
`Average Order Value`, `Active Customers`, `Units Sold`, `Cancellation Rate`,
`Revenue Previous Year`, `Revenue YoY Growth`, `One-Time Customers`,
`Average Frequency`.

## Limites / améliorations futures

Le plan initial prévoyait 8 pages (voir notes de projet) ; 4 ont été
réalisées pour cette version. Pages non construites, possibles en
prolongement :
- Analyse des ventes approfondie (saisonnalité, jours/heures, panier moyen
  par période)
- Produits (classification ABC, annulations par produit)
- Pays (comparaison Royaume-Uni / international, taux d'annulation par pays)
- Annulations et qualité des données (suivi dédié)

La matrice de rétention (page Cohortes) n'a pas de mise en forme
conditionnelle (carte de chaleur colorée) — laissée en valeurs brutes pour
cette version.
