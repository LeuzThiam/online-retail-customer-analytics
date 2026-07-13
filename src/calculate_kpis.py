import pandas as pd


def ajouter_variables_temporelles(donnees: pd.DataFrame) -> pd.DataFrame:
    donnees = donnees.copy()
    donnees["year"] = donnees["invoice_date"].dt.year
    donnees["quarter"] = donnees["invoice_date"].dt.quarter
    donnees["month"] = donnees["invoice_date"].dt.month
    donnees["month_name"] = donnees["invoice_date"].dt.month_name()
    donnees["year_month"] = donnees["invoice_date"].dt.to_period("M")
    donnees["week"] = donnees["invoice_date"].dt.isocalendar().week
    donnees["day_of_week"] = donnees["invoice_date"].dt.day_name()
    donnees["hour"] = donnees["invoice_date"].dt.hour

    donnees["is_complete_month"] = ~(
        (donnees["invoice_date"].dt.year == 2011)
        & (donnees["invoice_date"].dt.month == 12)
    )

    return donnees


def calculer_kpi_commerciaux(donnees: pd.DataFrame, commandes: pd.DataFrame) -> dict:
    chiffre_affaires_brut = donnees.loc[donnees["line_revenue"] > 0, "line_revenue"].sum()
    valeur_annulations = -donnees.loc[donnees["line_revenue"] < 0, "line_revenue"].sum()
    chiffre_affaires_net = donnees["line_revenue"].sum()

    nombre_commandes = commandes["invoice_no"].nunique()
    clients_actifs = donnees["customer_id"].nunique()

    return {
        "chiffre_affaires_brut": float(chiffre_affaires_brut),
        "valeur_annulations": float(valeur_annulations),
        "chiffre_affaires_net": float(chiffre_affaires_net),
        "nombre_commandes": int(nombre_commandes),
        "panier_moyen": (
            float(chiffre_affaires_net / nombre_commandes) if nombre_commandes else 0.0
        ),
        "articles_par_commande": (
            float(donnees["quantity"].sum() / nombre_commandes) if nombre_commandes else 0.0
        ),
        "prix_unitaire_moyen": float(donnees["unit_price"].mean()),
        "clients_actifs": int(clients_actifs),
        "revenu_moyen_par_client": (
            float(chiffre_affaires_net / clients_actifs) if clients_actifs else 0.0
        ),
        "frequence_moyenne": (
            float(nombre_commandes / clients_actifs) if clients_actifs else 0.0
        ),
    }


def calculer_ventes_mensuelles(donnees: pd.DataFrame) -> pd.DataFrame:
    """Chiffre d'affaires net mensuel, en excluant les mois incomplets
    (décembre 2011) pour ne pas fausser les comparaisons."""
    mensuel = (
        donnees[donnees["is_complete_month"]]
        .groupby(["year", "month", "month_name"], as_index=False)
        .agg(net_revenue=("line_revenue", "sum"))
        .sort_values(["year", "month"])
        .reset_index(drop=True)
    )
    return mensuel


def calculer_ventes_quotidiennes(donnees: pd.DataFrame, commandes: pd.DataFrame) -> pd.DataFrame:
    """Table agrégée par jour : CA brut/net, annulations, commandes,
    clients actifs, unités vendues, panier moyen.

    Ne calcule pas encore new_customers/returning_customers (nécessite
    l'historique complet par client — voir l'analyse de cohortes, Phase 6)."""
    donnees = donnees.copy()
    donnees["date"] = donnees["invoice_date"].dt.date

    quotidien = donnees.groupby("date").agg(
        gross_revenue=("line_revenue", lambda s: s[s > 0].sum()),
        cancelled_value=("line_revenue", lambda s: -s[s < 0].sum()),
        net_revenue=("line_revenue", "sum"),
        active_customers=("customer_id", "nunique"),
        units_sold=("quantity", "sum"),
    ).reset_index()

    commandes = commandes.copy()
    commandes["date"] = commandes["invoice_date"].dt.date
    commandes_par_jour = (
        commandes.groupby("date")["invoice_no"].nunique().rename("orders")
    )

    quotidien = quotidien.merge(commandes_par_jour, on="date", how="left")
    quotidien["average_order_value"] = quotidien["net_revenue"] / quotidien["orders"]

    return quotidien
