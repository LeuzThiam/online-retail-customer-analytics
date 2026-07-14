import pandas as pd
import pytest

from src.load_data import charger_ventes_en_ligne


def test_charger_ventes_en_ligne_renomme_les_colonnes(tmp_path):
    chemin = tmp_path / "sample.csv"
    chemin.write_text(
        "Invoice,StockCode,Description,Quantity,InvoiceDate,Price,Customer ID,Country\n"
        "489434,85048,TEST PRODUCT,12,2009-12-01 07:45:00,6.95,13085.0,United Kingdom\n"
    )

    donnees = charger_ventes_en_ligne(chemin)

    assert list(donnees.columns) == [
        "invoice_no",
        "stock_code",
        "description",
        "quantity",
        "invoice_date",
        "unit_price",
        "customer_id",
        "country",
    ]
    assert pd.api.types.is_datetime64_any_dtype(donnees["invoice_date"])


def test_charger_ventes_en_ligne_fichier_introuvable(tmp_path):
    chemin_inexistant = tmp_path / "absent.csv"

    with pytest.raises(FileNotFoundError):
        charger_ventes_en_ligne(chemin_inexistant)
