# Rapport de qualité des données — Online Retail II

Ce rapport documente les constats de qualité (notebooks `01` et `02`) et les
décisions de nettoyage appliquées (`src/clean_transactions.py`, notebook `03`).

## Méthodologie

Le nettoyage suit le principe : **ne rien supprimer par défaut sans l'avoir
d'abord caractérisé**. Une valeur inhabituelle (quantité négative, prix nul,
doublon potentiel) n'est pas nécessairement une erreur — voir la section
"Décisions et justifications" ci-dessous.

## Constats

| Constat | Valeur | Source |
|---|---|---|
| Lignes totales | 1 067 371 | `01_data_inventory.ipynb` |
| Valeurs manquantes — `description` | 4 382 | `01_data_inventory.ipynb` |
| Valeurs manquantes — `customer_id` | 243 007 | `01_data_inventory.ipynb` |
| Doublons exacts | 34 335 | `01_data_inventory.ipynb` |
| Prix ≤ 0 | 6 207 | `01_data_inventory.ipynb` |
| Pays nécessitant une normalisation | EIRE, RSA, USA, Unspecified | `02_data_quality_assessment.ipynb` |
| StockCode avec descriptions multiples | à compléter après exécution du notebook 02 | `02_data_quality_assessment.ipynb` |

## Décisions et justifications

### Classification des transactions
Chaque ligne est classée en `sale`, `cancellation`, `negative_adjustment` ou
`zero_quantity` (`ajouter_type_transaction`). Une facture commençant par `C`
est toujours considérée comme une annulation ; une quantité négative hors
annulation est un ajustement, pas automatiquement un retour.

### Descriptions manquantes ou incohérentes
La description manquante est complétée avec la description la plus fréquente
observée pour le même `stock_code` (`nettoyer_descriptions`). La colonne
originale `description` est conservée intacte à côté de `description_clean` —
aucune perte d'information brute.

Les descriptions légèrement différentes pour un même `stock_code` ne sont
**pas** fusionnées automatiquement au-delà de la normalisation basique
(majuscules, espaces) : une fusion plus fine nécessiterait une vérification
manuelle au cas par cas, hors périmètre de cette version.

### Pays incohérents
Une table de correspondance minimale (`CORRESPONDANCE_PAYS`) normalise les
valeurs connues pour être incohérentes (EIRE → Ireland, RSA → South Africa,
USA → United States, Unspecified → Unknown) dans `country_clean`, sans
toucher à `country` (conservée).

### Clients manquants
`customer_id` manquant n'entraîne **pas** la suppression de la ligne : elle
reste utile pour l'analyse des ventes, produits et pays. `separer_ventes_clients`
produit deux jeux de données distincts :
- `sales_df` : toutes les transactions (analyse ventes/produits/pays)
- `customer_df` : uniquement les transactions avec client connu (RFM, cohortes,
  fidélisation)

### Doublons
Seuls les **doublons exacts** (ligne strictement identique) sont supprimés
dans le notebook `03`. Les doublons potentiels (même facture/produit/quantité/
prix/client/pays mais pas forcément la même ligne complète) sont conservés :
ils peuvent correspondre à deux saisies légitimes du même produit dans une
même facture.

### Valeurs extrêmes
Un indicateur `quantity_outlier` marque les quantités au-delà du 99,9e
percentile en valeur absolue, sans suppression automatique. Une grande partie
de la clientèle étant composée de grossistes, une quantité très élevée peut
être parfaitement légitime.

## Règles de validation appliquées (`src/validation.py`)

| Règle | Description |
|---|---|
| `facture_avec_date` | Chaque ligne a une `invoice_date` |
| `facture_avec_pays` | Chaque ligne a un `country` |
| `stock_code_present` | Chaque ligne a un `stock_code` |
| `prix_numerique` | `unit_price` est de type numérique |
| `quantite_numerique` | `quantity` est de type numérique |
| `type_transaction_defini` | `transaction_type` a été calculé |
| `revenu_ligne_coherent` | `line_revenue == quantity × unit_price` pour toutes les lignes |

## Jeu de données en sortie

`data/processed/transactions_clean.csv` — transactions nettoyées avec
`transaction_type`, `description_clean`, `country_clean`, `quantity_outlier`,
`line_revenue` ajoutés, doublons exacts supprimés. Fichier gitignoré (voir
`.gitignore`), généré localement en exécutant `03_transaction_cleaning.ipynb`.
