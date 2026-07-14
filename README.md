# Online Retail Customer Analytics

Analyse de plus d'un million de transactions e-commerce avec Python, MySQL
et Power BI : nettoyage, ventes, segmentation RFM, cohortes, produits et
recommandations commerciales.

## Présentation

Ce projet analyse le dataset public **Online Retail II** (UCI), des
transactions d'un commerce électronique britannique entre décembre 2009 et
décembre 2011. L'entreprise vend principalement des articles-cadeaux et
compte une part importante de clients grossistes.

## Problématique métier

> Comment améliorer le chiffre d'affaires, la fidélisation des clients et
> la gestion des produits à partir des données transactionnelles
> disponibles ?

## Objectifs

1. Comprendre les ventes (évolution, saisonnalité, meilleurs pays/produits)
2. Comprendre les clients (récurrence, valeur, inactivité)
3. Mesurer la fidélisation (RFM, cohortes, taux de réachat)
4. Étudier les produits (top ventes, classification ABC, annulations)
5. Aider à la prise de décision (ciblage, marchés à développer)

## Dataset

- Source : [Online Retail II — UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
- 1 067 371 lignes brutes, 8 colonnes (`Invoice`, `StockCode`, `Description`,
  `Quantity`, `InvoiceDate`, `Price`, `Customer ID`, `Country`)
- Une ligne = un produit à l'intérieur d'une facture, pas une commande
  complète
- Le fichier brut (`data/raw/online_retail_II.csv`) n'est pas versionné —
  téléchargez-le et placez-le dans `data/raw/` avant d'exécuter le pipeline

## Architecture du projet

```
online-retail-customer-analytics/
├── data/               # raw (non versionné) / interim / processed / reference
├── notebooks/          # 01 à 08, exécutés dans l'ordre
├── src/                # code réutilisable (chargement, nettoyage, KPI, RFM, cohortes)
├── sql/                # schéma en étoile MySQL + requêtes d'analyse
├── dashboard/          # mesures DAX, documentation, captures d'écran
├── docs/               # dictionnaire de données, qualité, méthodologie, limites
└── requirements.txt
```

## Méthodologie

Voir [`docs/methodology.md`](docs/methodology.md) pour le détail de
l'approche (audit → nettoyage → analyse → modélisation → dashboard).

## Nettoyage des données

Voir [`docs/data_quality_report.md`](docs/data_quality_report.md) pour le
détail des décisions de nettoyage (classification des transactions,
descriptions incohérentes, pays, doublons, valeurs extrêmes).

## Indicateurs (KPI)

Chiffre d'affaires net/brut, valeur annulée, nombre de commandes, panier
moyen, clients actifs, taux d'annulation, récence/fréquence/montant (RFM),
taux de rétention par cohorte, classification ABC des produits.

## Analyses réalisées

| Analyse | Notebook / fichier |
|---|---|
| Inventaire initial | `notebooks/01_data_inventory.ipynb` |
| Qualité des données | `notebooks/02_data_quality_assessment.ipynb` |
| Nettoyage des transactions | `notebooks/03_transaction_cleaning.ipynb` |
| Analyse des ventes | `notebooks/04_sales_analysis.ipynb` |
| Analyse des clients | `notebooks/05_customer_analysis.ipynb` |
| Segmentation RFM | `notebooks/06_rfm_segmentation.ipynb` |
| Analyse de cohortes | `notebooks/07_cohort_analysis.ipynb` |
| Analyse des produits (ABC) | `notebooks/08_product_analysis.ipynb` |
| Modèle SQL en étoile | `sql/01` à `sql/07` |
| Tableau de bord | `dashboard/` |

## Résultats principaux

- Chiffre d'affaires net total : ~18,86 M £ sur la période
- ~5 942 clients uniques, ~34 % à achat unique
- Le Royaume-Uni concentre la grande majorité du chiffre d'affaires
- Segmentation RFM en 7 groupes (Champions, Clients fidèles, À risque...) ;
  les Champions génèrent une part disproportionnée du revenu malgré un
  effectif réduit
- Taux d'annulation global d'environ 8 %

## Tableau de bord

Dashboard Power BI (4 pages : Vue exécutive, RFM, Cohortes, Clients).
Voir [`dashboard/README.md`](dashboard/README.md) et les captures d'écran
dans `dashboard/screenshots/`.

## Installation

```bash
git clone git@github.com:LeuzThiam/online-retail-customer-analytics.git
cd online-retail-customer-analytics
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

Téléchargez `online_retail_II.csv` depuis UCI/Kaggle et placez-le dans
`data/raw/`.

## Exécution

```bash
jupyter notebook
```

Exécutez les notebooks dans l'ordre (`01` à `08`). Pour le modèle SQL,
exécutez les scripts `sql/01` à `sql/04` dans un client MySQL (8.0+), puis
`sql/05` à `sql/07` pour les requêtes d'analyse.

## Limites

Voir [`docs/limitations.md`](docs/limitations.md) (absence de coûts/marge,
de données marketing et démographiques, période historique 2009-2011,
chargement SQL complet non testé en conditions de ressources limitées).

## Améliorations futures

- Pages de dashboard supplémentaires (ventes approfondies, produits, pays,
  annulations)
- Market Basket Analysis (règles d'association, `mlxtend`)
- Prévision des ventes (validation temporelle, pas de split aléatoire)
- Prédiction du réachat client (machine learning)
