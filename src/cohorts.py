import pandas as pd


def ajouter_cohortes(transactions: pd.DataFrame) -> pd.DataFrame:
    """Ajoute le mois de commande (order_month), le mois de cohorte
    (cohort_month = mois du premier achat du client) et le nombre de mois
    écoulés depuis l'acquisition (cohort_index, démarrant à 1), à partir des
    ventes valides et des clients connus uniquement."""
    ventes = transactions[
        (transactions["transaction_type"] == "sale")
        & transactions["customer_id"].notna()
    ].copy()

    ventes["order_month"] = ventes["invoice_date"].dt.to_period("M").dt.to_timestamp()
    ventes["cohort_month"] = ventes.groupby("customer_id")["order_month"].transform(
        "min"
    )

    ventes["cohort_index"] = (
        (ventes["order_month"].dt.year - ventes["cohort_month"].dt.year) * 12
        + (ventes["order_month"].dt.month - ventes["cohort_month"].dt.month)
        + 1
    )

    return ventes


def construire_table_retention(ventes_cohortes: pd.DataFrame) -> pd.DataFrame:
    """Matrice de rétention : une ligne par cohorte, une colonne par mois
    écoulé depuis l'acquisition, valeur = proportion de clients encore actifs."""
    cohort_counts = (
        ventes_cohortes.groupby(["cohort_month", "cohort_index"])["customer_id"]
        .nunique()
        .unstack(fill_value=0)
    )

    cohort_sizes = cohort_counts.iloc[:, 0]
    retention = cohort_counts.divide(cohort_sizes, axis=0)

    return retention


def revenu_moyen_par_cohorte(ventes_cohortes: pd.DataFrame) -> pd.DataFrame:
    """Revenu net moyen par client actif, par cohorte et par mois écoulé."""
    revenu = ventes_cohortes.groupby(["cohort_month", "cohort_index"]).agg(
        revenu_total=("line_revenue", "sum"),
        clients_actifs=("customer_id", "nunique"),
    )
    revenu["revenu_moyen_par_client"] = (
        revenu["revenu_total"] / revenu["clients_actifs"]
    )
    return revenu.reset_index()
