import pandas as pd


def valider_transactions(donnees: pd.DataFrame) -> pd.DataFrame:
    """Vérifie les règles de qualité de données définies dans docs/data_quality_report.md."""

    revenu_coherent = True
    if "line_revenue" in donnees.columns:
        ecart = (
            donnees["line_revenue"] - donnees["quantity"] * donnees["unit_price"]
        ).abs()
        revenu_coherent = bool(ecart.max() < 1e-9)

    regles = {
        "facture_avec_date": bool(donnees["invoice_date"].notna().all()),
        "facture_avec_pays": bool(donnees["country"].notna().all()),
        "stock_code_present": bool(donnees["stock_code"].notna().all()),
        "prix_numerique": pd.api.types.is_numeric_dtype(donnees["unit_price"]),
        "quantite_numerique": pd.api.types.is_numeric_dtype(donnees["quantity"]),
        "type_transaction_defini": "transaction_type" in donnees.columns,
        "revenu_ligne_coherent": revenu_coherent,
    }

    return pd.DataFrame(
        {"regle": list(regles.keys()), "respectee": list(regles.values())}
    )


def resumer_annulations(donnees: pd.DataFrame) -> pd.DataFrame:
    """Compare volumes et valeurs entre ventes et annulations."""
    return donnees.groupby("is_cancellation").agg(
        lignes=("invoice_no", "size"),
        factures=("invoice_no", "nunique"),
        quantite=("quantity", "sum"),
        valeur=("line_revenue", "sum"),
    )
