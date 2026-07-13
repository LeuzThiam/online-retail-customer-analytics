import pandas as pd


def calculer_rfm(transactions: pd.DataFrame) -> pd.DataFrame:
    """Calcule Récence, Fréquence, Montant par client à partir des seules
    lignes de vente valides (transaction_type == 'sale'), pour les clients
    connus uniquement."""
    ventes = transactions[
        (transactions["transaction_type"] == "sale")
        & transactions["customer_id"].notna()
    ]

    date_reference = ventes["invoice_date"].max() + pd.Timedelta(days=1)

    rfm = (
        ventes.groupby("customer_id")
        .agg(
            last_purchase=("invoice_date", "max"),
            frequency=("invoice_no", "nunique"),
            monetary=("line_revenue", "sum"),
        )
        .reset_index()
    )

    rfm["recency"] = (date_reference - rfm["last_purchase"]).dt.days

    return rfm


def attribuer_scores_rfm(rfm: pd.DataFrame) -> pd.DataFrame:
    """Découpe récence/fréquence/montant en quintiles (1 à 5). Pour la
    récence, un score élevé = achat récent (donc les quintiles sont inversés)."""
    rfm = rfm.copy()

    rfm["r_score"] = pd.qcut(rfm["recency"], q=5, labels=[5, 4, 3, 2, 1])
    rfm["f_score"] = pd.qcut(
        rfm["frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5]
    )
    rfm["m_score"] = pd.qcut(rfm["monetary"], q=5, labels=[1, 2, 3, 4, 5])

    return rfm


def _assigner_segment(ligne: pd.Series) -> str:
    r_score = int(ligne["r_score"])
    f_score = int(ligne["f_score"])
    m_score = int(ligne["m_score"])

    if r_score >= 4 and f_score >= 4:
        return "Champions"
    if f_score >= 4:
        return "Clients fidèles"
    if m_score == 5:
        return "Gros acheteurs"
    if r_score == 5 and ligne["frequency"] == 1:
        return "Nouveaux clients"
    if r_score <= 2 and f_score >= 3:
        return "À risque"
    if r_score == 1 and f_score <= 2:
        return "Perdus"
    return "Clients réguliers"


def segmenter_clients(transactions: pd.DataFrame) -> pd.DataFrame:
    """Pipeline complet : calcule RFM, attribue les scores, assigne un segment."""
    rfm = calculer_rfm(transactions)
    rfm = attribuer_scores_rfm(rfm)
    rfm["segment"] = rfm.apply(_assigner_segment, axis=1)
    return rfm
