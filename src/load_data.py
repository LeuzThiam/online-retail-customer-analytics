from pathlib import Path
import pandas as pd

CHEMIN_DONNEES_BRUTES = Path(__file__).resolve().parent.parent / "data" / "raw" / "online_retail_II.csv"

CORRESPONDANCE_COLONNES = {
    "invoice": "invoice_no",
    "stockcode": "stock_code",
    "description": "description",
    "quantity": "quantity",
    "invoicedate": "invoice_date",
    "price": "unit_price",
    "customerid": "customer_id",
    "country": "country",
}

def charger_ventes_en_ligne(chemin: Path = CHEMIN_DONNEES_BRUTES) -> pd.DataFrame:
    if not chemin.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {chemin}. "
            "Téléchargez online_retail_II.csv depuis UCI/Kaggle et placez-le dans data/raw/."
        )

    donnees = pd.read_csv(chemin)

    donnees.columns = (
        donnees.columns.str.strip().str.lower().str.replace(" ", "")
    )
    donnees = donnees.rename(columns=CORRESPONDANCE_COLONNES)

    donnees["invoice_date"] = pd.to_datetime(donnees["invoice_date"])

    return donnees