from __future__ import annotations

from typing import Any, Dict, List, Optional
import pandas as pd
from .config import DATA_CLEAN_CSV

_DATA_CACHE: Optional[pd.DataFrame] = None

# Carrega novamente o dataset limpo de houses_clean.csv (com cache)
def load_dataset() -> pd.DataFrame:
    global _DATA_CACHE

    if _DATA_CACHE is None:
        print(f"[houses_service] A carregar dataset de: {DATA_CLEAN_CSV}")
        df = pd.read_csv(DATA_CLEAN_CSV)

        int_cols = [
            "id",
            "year_built",
            "size_sqft",
            "price",
            "owners_before",
            "rooms",
            "bathrooms",
            "garage",
            "garden",
            "crime_cases",
            "legal_cases",
            "salary",
            "loan_amount",
            "loan_years",
            "monthly_expenses",
            "down_payment",
            "satisfaction",
            "neighbourhood",
            "connectivity",
            "decision",
        ]
        for col in int_cols:
            df[col] = df[col].astype("int64")

        df["emi_ratio"] = df["emi_ratio"].astype("float64")
        _DATA_CACHE = df

    return _DATA_CACHE


# =====================================================
#  Funções de consulta (usadas pelos servidores)
# =====================================================

# Retorna uma lista de casas num país específico
def get_houses_by_country(country: str, limit: int | None = 50) -> List[Dict[str, Any]]:
    df = load_dataset()
    mask = df["country"].str.lower() == country.lower()
    result_df = df[mask]
    if limit:
        result_df = result_df.head(limit)
    return result_df.to_dict(orient="records")


# Retorna uma lista de casas num intervalo de preços, opcionalmente filtrado por país
def get_houses_by_price_range(
    min_price: int, max_price: int, country: Optional[str] = None, limit: int | None = 50
) -> List[Dict[str, Any]]:
    df = load_dataset()
    mask = (df["price"] >= min_price) & (df["price"] <= max_price)
    if country:
        mask &= df["country"].str.lower() == country.lower()
    result_df = df[mask]
    if limit:
        result_df = result_df.head(limit)
    return result_df.to_dict(orient="records")


# Retorna o preço médio das casas num país específico
def get_average_price_by_country(country: str) -> float:
    df = load_dataset()
    mask = df["country"].str.lower() == country.lower()
    subset = df[mask]
    return float(subset["price"].mean()) if not subset.empty else 0.0


# Retorna estatísticas globais sobre decisões de compra
def get_decision_stats() -> Dict[str, Any]:
    df = load_dataset()
    total = len(df)
    bought = int((df["decision"] == 1).sum())
    not_bought = total - bought
    percent_bought = (bought / total * 100) if total > 0 else 0.0
    return {
        "total": total,
        "bought": bought,
        "not_bought": not_bought,
        "percent_bought": round(percent_bought, 2),
    }


# =====================================================
#  Testes para evidenciar o funcionamento
# =====================================================

def _demo() -> None:
    print("=== Demo houses_service ===")
    print("\n-> Estatísticas globais de decisão:")
    print(get_decision_stats())

    print("\n-> Preço médio em 'France':")
    print(get_average_price_by_country("France"))

    print("\n-> 3 casas em 'Portugal' (se existirem):")
    for h in get_houses_by_country("Portugal", limit=3):
        print(f"- id={h['id']}, city={h['city']}, price={h['price']}")


if __name__ == "__main__":
    _demo()

    