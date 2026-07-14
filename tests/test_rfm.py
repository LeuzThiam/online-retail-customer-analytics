import pandas as pd

from src.rfm import calculer_rfm


def test_calculer_rfm():
    donnees = pd.DataFrame(
        {
            "invoice_no": ["1001", "1002", "2001"],
            "customer_id": [100.0, 100.0, 200.0],
            "invoice_date": pd.to_datetime(["2011-01-01", "2011-01-10", "2011-01-05"]),
            "line_revenue": [50.0, 30.0, 100.0],
            "transaction_type": ["sale", "sale", "sale"],
        }
    )

    rfm = calculer_rfm(donnees).set_index("customer_id")

    assert rfm.loc[100.0, "frequency"] == 2
    assert rfm.loc[100.0, "monetary"] == 80.0
    assert rfm.loc[200.0, "frequency"] == 1
    # date de reference = max(invoice_date) + 1 jour = 2011-01-11
    assert rfm.loc[100.0, "recency"] == 1
    assert rfm.loc[200.0, "recency"] == 6
