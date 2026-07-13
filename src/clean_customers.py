import pandas as pd


def construire_clients(donnees: pd.DataFrame, commandes: pd.DataFrame) -> pd.DataFrame:
    """Agrège les transactions en une table d'une ligne par client connu
    (customer_id non manquant). Inclut récence/fréquence/montant, base
    commune pour l'analyse clients et, plus tard, la segmentation RFM."""
    clients_donnees = donnees[donnees["customer_id"].notna()].copy()
    clients_donnees["gross_line_value"] = clients_donnees["line_revenue"].clip(lower=0)
    clients_donnees["cancelled_line_value"] = (
        -clients_donnees["line_revenue"]
    ).clip(lower=0)

    date_reference = clients_donnees["invoice_date"].max() + pd.Timedelta(days=1)

    clients = clients_donnees.groupby("customer_id", as_index=False).agg(
        country=("country_clean", "first"),
        first_purchase_date=("invoice_date", "min"),
        last_purchase_date=("invoice_date", "max"),
        number_of_products=("stock_code", "nunique"),
        total_quantity=("quantity", "sum"),
        gross_revenue=("gross_line_value", "sum"),
        cancelled_value=("cancelled_line_value", "sum"),
        net_revenue=("line_revenue", "sum"),
    )

    commandes_clients = commandes[commandes["customer_id"].notna()]
    nb_commandes = (
        commandes_clients.groupby("customer_id")["invoice_no"]
        .nunique()
        .rename("number_of_orders")
    )
    clients = clients.merge(nb_commandes, on="customer_id", how="left")

    clients["recency_days"] = (
        date_reference - clients["last_purchase_date"]
    ).dt.days
    clients["frequency"] = clients["number_of_orders"]
    clients["monetary"] = clients["net_revenue"]
    clients["quantite_moyenne_par_commande"] = (
        clients["total_quantity"] / clients["number_of_orders"]
    )

    return clients


def calculer_delai_moyen_reachat(commandes: pd.DataFrame) -> float:
    """Délai moyen (en jours) entre deux commandes successives d'un même
    client, moyenné sur l'ensemble des clients ayant au moins 2 commandes."""
    commandes_clients = commandes[commandes["customer_id"].notna()].sort_values(
        ["customer_id", "invoice_date"]
    )
    delais = (
        commandes_clients.groupby("customer_id")["invoice_date"]
        .diff()
        .dt.days
        .dropna()
    )
    return float(delais.mean())
