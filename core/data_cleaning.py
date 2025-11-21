import pandas as pd
from .config import DATA_RAW_CSV, DATA_CLEAN_CSV

# Carrega o dataset original transferido do Kaggle
def load_raw_dataset() -> pd.DataFrame:
    print(f"A carregar CSV de: {DATA_RAW_CSV}")
    df = pd.read_csv(DATA_RAW_CSV)
    return df

# Renomeia algumas colunas para nomes mais simples
def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "property_id": "id",
        "country": "country",
        "city": "city",
        "property_type": "type",
        "furnishing_status": "furnishing",
        "property_size_sqft": "size_sqft",
        "price": "price",
        "constructed_year": "year_built",
        "previous_owners": "owners_before",
        "rooms": "rooms",
        "bathrooms": "bathrooms",
        "garage": "garage",
        "garden": "garden",
        "crime_cases_reported": "crime_cases",
        "legal_cases_on_property": "legal_cases",
        "customer_salary": "salary",
        "loan_amount": "loan_amount",
        "loan_tenure_years": "loan_years",
        "monthly_expenses": "monthly_expenses",
        "down_payment": "down_payment",
        "emi_to_income_ratio": "emi_ratio",
        "satisfaction_score": "satisfaction",
        "neighbourhood_rating": "neighbourhood",
        "connectivity_score": "connectivity",
        "decision": "decision",
    }

    df = df.rename(columns=rename_map)

    print("\n=== Verificação de valores em falta por coluna ===")
    print(df.isna().sum())

    return df

# Guarda o novo dataset limpo na pasta clean 
def save_clean_dataset(df: pd.DataFrame) -> None:
    DATA_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_CLEAN_CSV, index=False)
    print(f"\nDataset limpo guardado em: {DATA_CLEAN_CSV}")


def main():
    # 1) Carregar dados originais
    df_raw = load_raw_dataset()

    print("\n=== Dimensões do dataset original (linhas, colunas) ===")
    print(df_raw.shape)

    # 2) Limpar / renomear
    df_clean = clean_dataset(df_raw)

    print("\n=== Nomes das colunas após limpeza ===")
    print(list(df_clean.columns))

    print("\n=== Tipos de dados após limpeza ===")
    print(df_clean.dtypes)

    print("\n=== Primeiras 5 linhas (dataset limpo) ===")
    print(df_clean.head())

    # 3) Guardar CSV limpo
    save_clean_dataset(df_clean)


if __name__ == "__main__":
    main()

    