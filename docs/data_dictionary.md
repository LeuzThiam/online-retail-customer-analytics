# Dictionnaire de données — Online Retail II

## Source

Dataset UCI "Online Retail II" : transactions d'un commerce électronique
britannique entre le 1er décembre 2009 et le 9 décembre 2011.

- Fichier : `data/raw/online_retail_II.csv`
- 1 067 371 lignes, 8 colonnes
- Une ligne ne correspond pas à une commande complète, mais à **un produit
  à l'intérieur d'une facture donnée**. Une facture avec cinq produits
  apparaît donc sur cinq lignes.

## Colonnes

| Colonne originale | Colonne normalisée | Type       | Signification                        | Remarques |
|--------------------|--------------------|------------|---------------------------------------|-----------|
| Invoice             | invoice_no          | texte      | Numéro de facture                     | Commence par `C` si la transaction est une annulation |
| StockCode           | stock_code          | texte      | Code du produit                       | Certains codes ne correspondent pas à un produit classique (frais de port, ajustements) |
| Description         | description          | texte      | Description du produit                | 4 382 valeurs manquantes |
| Quantity            | quantity             | entier     | Quantité achetée ou annulée           | Peut être négative (retour, annulation, correction d'inventaire) |
| InvoiceDate         | invoice_date         | date/heure | Date et heure de la transaction       | Période couverte : 2009-12-01 à 2011-12-09 (décembre 2011 incomplet) |
| Price               | unit_price           | décimal    | Prix unitaire en livres sterling (£)  | 6 207 valeurs ≤ 0 (cadeaux, échantillons, corrections possibles) |
| Customer ID         | customer_id          | décimal    | Identifiant du client                 | 243 007 valeurs manquantes — un client anonyme peut quand même servir à l'analyse produits/pays, mais pas à l'analyse de fidélisation |
| Country             | country              | texte      | Pays de résidence du client           | Valeurs à normaliser (ex. "EIRE" → Ireland, "USA" → United States) |

## Constats de l'audit initial (`notebooks/01_data_inventory.ipynb`)

- Doublons exacts : 34 335 lignes
- Aucune valeur manquante sur `invoice_no`, `stock_code`, `quantity`,
  `invoice_date`, `unit_price`, `country`
- Les seules colonnes avec valeurs manquantes sont `description` et
  `customer_id`

## Notes

- Ce fichier CSV contient déjà les deux années fusionnées (contrairement à
  certaines versions du dataset distribuées en `.xlsx` avec deux feuilles
  séparées par année).
- Voir `src/load_data.py` pour la logique de normalisation des noms de
  colonnes appliquée automatiquement au chargement.
