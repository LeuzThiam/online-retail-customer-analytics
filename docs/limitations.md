# Limites méthodologiques et techniques

## Limites du dataset

### Absence de coûts
Le dataset fournit le prix de vente mais aucune donnée de coût (achat,
fabrication, expédition, marketing). Le chiffre d'affaires peut être
analysé, pas la rentabilité réelle ni la marge.

### Absence de données marketing
Aucune information sur la campagne d'acquisition, le canal publicitaire,
le coût d'acquisition ou le trafic du site — impossible d'expliquer
pourquoi un client est arrivé, seulement d'observer son comportement une
fois client.

### Absence de données démographiques
Ni âge, ni sexe, ni revenu, ni profession. La segmentation (RFM) est
nécessairement comportementale, pas démographique.

### Annulations non expliquées
Une facture commençant par `C` est identifiable comme annulation, mais le
dataset ne précise jamais la raison (retour produit, erreur de saisie,
insatisfaction...).

### Clients anonymes
Environ 23 % des lignes n'ont pas de `Customer ID`. Ces transactions
restent utiles pour l'analyse des ventes/produits/pays, mais sont exclues
de toute analyse de fidélisation (RFM, cohortes) — voir
`sales_df`/`customer_df` dans `src/clean_transactions.py`.

### Période historique
Les données couvrent décembre 2009 à décembre 2011. Le projet démontre une
méthode d'analyse ; il ne décrit pas le e-commerce actuel (comportements
d'achat, canaux, concurrence ayant beaucoup évolué depuis).

## Limites techniques de ce projet

### Base de données MySQL testée sur échantillon uniquement
Le schéma en étoile (`sql/`) a été validé de bout en bout sur un
échantillon de 50 000 lignes (`data/processed/transactions_sample.csv`),
pas sur les 1 033 036 lignes complètes. Le chargement complet a rencontré
des limites de performance sur la machine de développement (opérations de
plusieurs minutes, y compris pour un simple `CREATE INDEX`). Les requêtes
sont correctes et fonctionnelles ; seul le volume testé est réduit.

### Matrice de cohortes sans mise en forme visuelle
Le tableau de rétention (page Cohortes du dashboard) affiche les valeurs
brutes sans carte de chaleur colorée (mise en forme conditionnelle non
appliquée dans cette version).

### Dashboard partiel
4 pages sur les 8 initialement prévues (Vue exécutive, RFM, Cohortes,
Clients). Ventes approfondies, Produits, Pays et Annulations/qualité ne
sont pas encore construites en pages dédiées — voir "Améliorations
futures" dans le README.

### Couverture de tests limitée
Une suite `pytest` (`tests/`) couvre les fonctions clés de nettoyage, de
calcul des KPI et de RFM, avec une CI GitHub Actions (`.github/workflows/tests.yml`)
exécutée à chaque push/PR sur `main`/`develop`. La couverture reste
partielle : les fonctions de cohortes et de validation n'ont pas encore de
tests dédiés.
