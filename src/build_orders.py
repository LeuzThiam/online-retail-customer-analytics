import pandas as pd


def construire_commandes(donnees: pd.DataFrame) -> pd.DataFrame:
    """Agrège les lignes de transactions (sorties de nettoyer_transactions) en
    une table d'une ligne par facture (invoice_no)."""
    donnees = donnees.copy()
    donnees["gross_line_value"] = donnees["line_revenue"].clip(lower=0)
    donnees["cancelled_line_value"] = (-donnees["line_revenue"]).clip(lower=0)

    commandes = donnees.groupby("invoice_no", as_index=False).agg(
        customer_id=("customer_id", "first"),
        invoice_date=("invoice_date", "min"),
        country=("country_clean", "first"),
        number_of_products=("stock_code", "nunique"),
        total_quantity=("quantity", "sum"),
        gross_order_value=("gross_line_value", "sum"),
        cancelled_value=("cancelled_line_value", "sum"),
        net_order_value=("line_revenue", "sum"),
        is_cancelled=("is_cancellation", "any"),
    )

    return commandes
