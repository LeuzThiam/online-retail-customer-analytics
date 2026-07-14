import pandas as pd

from src.build_orders import construire_commandes
from src.calculate_kpis import ajouter_variables_temporelles, calculer_kpi_commerciaux
from src.clean_transactions import nettoyer_transactions


def _transactions_exemple():
    return pd.DataFrame(
        {
            "invoice_no": ["1001", "1001", "1002"],
            "stock_code": ["A1", "A2", "A1"],
            "description": ["Produit A", "Produit B", "Produit A"],
            "quantity": [2, 1, 3],
            "invoice_date": pd.to_datetime(
                ["2010-06-08 14:40:00", "2010-06-08 14:40:00", "2011-11-20 09:15:00"]
            ),
            "unit_price": [5.0, 10.0, 5.0],
            "customer_id": [100.0, 100.0, 200.0],
            "country": ["United Kingdom", "United Kingdom", "France"],
        }
    )


def test_ajouter_variables_temporelles():
    donnees = ajouter_variables_temporelles(_transactions_exemple())

    assert list(donnees["year"]) == [2010, 2010, 2011]
    assert donnees["is_complete_month"].all()


def test_calculer_kpi_commerciaux():
    donnees = nettoyer_transactions(_transactions_exemple())
    commandes = construire_commandes(donnees)

    kpi = calculer_kpi_commerciaux(donnees, commandes)

    assert kpi["nombre_commandes"] == 2
    assert kpi["chiffre_affaires_net"] == 35.0
    assert kpi["clients_actifs"] == 2
