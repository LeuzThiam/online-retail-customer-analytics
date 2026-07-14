import pandas as pd

from src.clean_transactions import (
    ajouter_type_transaction,
    detecter_doublons,
    nettoyer_descriptions,
    normaliser_pays,
    separer_ventes_clients,
)


def _donnees_exemple():
    return pd.DataFrame(
        {
            "invoice_no": ["489434", "489434", "C489435", "489436"],
            "stock_code": ["A1", "A1", "A2", "A3"],
            "description": ["Produit A", None, "Produit B", "Produit C"],
            "quantity": [12, 5, -2, 0],
            "invoice_date": pd.to_datetime(
                [
                    "2009-12-01 07:45:00",
                    "2009-12-01 07:45:00",
                    "2009-12-01 08:00:00",
                    "2009-12-02 09:00:00",
                ]
            ),
            "unit_price": [6.95, 6.95, 4.5, 3.0],
            "customer_id": [13085.0, 13085.0, None, 13086.0],
            "country": ["United Kingdom", "United Kingdom", "EIRE", "USA"],
        }
    )


def test_ajouter_type_transaction_classe_correctement():
    donnees = ajouter_type_transaction(_donnees_exemple())

    assert list(donnees["transaction_type"]) == [
        "sale",
        "sale",
        "cancellation",
        "zero_quantity",
    ]


def test_nettoyer_descriptions_comble_les_manquantes():
    donnees = nettoyer_descriptions(_donnees_exemple())

    assert donnees.loc[1, "description_clean"] == "PRODUIT A"


def test_normaliser_pays_corrige_les_valeurs_connues():
    donnees = normaliser_pays(_donnees_exemple())

    assert donnees.loc[2, "country_clean"] == "Ireland"
    assert donnees.loc[3, "country_clean"] == "United States"


def test_separer_ventes_clients_filtre_les_clients_connus():
    ventes, clients = separer_ventes_clients(_donnees_exemple())

    assert len(ventes) == 4
    assert len(clients) == 3


def test_detecter_doublons_compte_les_lignes_identiques():
    donnees = pd.concat([_donnees_exemple(), _donnees_exemple().iloc[[0]]])

    resultat = detecter_doublons(donnees)

    assert resultat["doublons_exacts"] == 1
