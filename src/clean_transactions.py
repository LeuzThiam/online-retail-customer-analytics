from typing import Tuple

import pandas as pd

CORRESPONDANCE_PAYS = {
    "EIRE": "Ireland",
    "RSA": "South Africa",
    "USA": "United States",
    "Unspecified": "Unknown",
}


def ajouter_type_transaction(donnees: pd.DataFrame) -> pd.DataFrame:
    donnees = donnees.copy()
    donnees["is_cancellation"] = (
        donnees["invoice_no"].astype(str).str.startswith("C")
    )
    donnees["transaction_type"] = donnees.apply(_classifier_transaction, axis=1)
    return donnees


def _classifier_transaction(ligne: pd.Series) -> str:
    if ligne["is_cancellation"]:
        return "cancellation"
    if ligne["quantity"] < 0:
        return "negative_adjustment"
    if ligne["quantity"] == 0:
        return "zero_quantity"
    return "sale"


def nettoyer_descriptions(donnees: pd.DataFrame) -> pd.DataFrame:
    donnees = donnees.copy()

    descriptions_frequentes = (
        donnees.dropna(subset=["description"])
        .groupby("stock_code")["description"]
        .agg(lambda valeurs: valeurs.mode().iloc[0])
    )

    donnees["description_clean"] = donnees["description"].fillna(
        donnees["stock_code"].map(descriptions_frequentes)
    )

    donnees["description_clean"] = (
        donnees["description_clean"]
        .astype("string")
        .str.strip()
        .str.upper()
        .str.replace(r"\s+", " ", regex=True)
    )

    return donnees


def normaliser_pays(donnees: pd.DataFrame) -> pd.DataFrame:
    donnees = donnees.copy()
    donnees["country_clean"] = donnees["country"].replace(CORRESPONDANCE_PAYS)
    return donnees


def separer_ventes_clients(donnees: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    ventes_df = donnees.copy()
    clients_df = donnees[donnees["customer_id"].notna()].copy()
    return ventes_df, clients_df


def detecter_doublons(donnees: pd.DataFrame) -> dict:
    doublons_exacts = donnees.duplicated().sum()
    doublons_potentiels = donnees.duplicated(
        subset=[
            "invoice_no",
            "stock_code",
            "quantity",
            "invoice_date",
            "unit_price",
            "customer_id",
            "country",
        ],
        keep=False,
    ).sum()
    return {
        "doublons_exacts": int(doublons_exacts),
        "doublons_potentiels": int(doublons_potentiels),
    }


def detecter_valeurs_extremes(donnees: pd.DataFrame, seuil: float = 0.999) -> pd.DataFrame:
    donnees = donnees.copy()
    limite = donnees["quantity"].abs().quantile(seuil)
    donnees["quantity_outlier"] = donnees["quantity"].abs() > limite
    return donnees


def nettoyer_transactions(donnees: pd.DataFrame) -> pd.DataFrame:
    """Applique le pipeline complet de nettoyage sur les transactions brutes."""
    donnees = ajouter_type_transaction(donnees)
    donnees = nettoyer_descriptions(donnees)
    donnees = normaliser_pays(donnees)
    donnees = detecter_valeurs_extremes(donnees)
    donnees["line_revenue"] = donnees["quantity"] * donnees["unit_price"]
    return donnees
