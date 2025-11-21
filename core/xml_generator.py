import pandas as pd
from lxml import etree as ET

from .config import DATA_CLEAN_CSV, XML_OUTPUT

# Carrega o dataset previamente limpo
def load_clean_dataset() -> pd.DataFrame:
    print(f"A carregar dataset limpo de: {DATA_CLEAN_CSV}")
    df = pd.read_csv(DATA_CLEAN_CSV)
    return df

# Constrói um elemento <house> a partir de uma linha do DataFrame.
def build_house_element(row: pd.Series) -> ET.Element:

    # atributos principais
    house_el = ET.Element(
        "house",
        id=str(row["id"]),
        country=str(row["country"]),
        city=str(row["city"]),
    )

    # campos que vão ser sub-elementos
    fields_as_elements = [
        "type",
        "furnishing",
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
        "emi_ratio",
        "satisfaction",
        "neighbourhood",
        "connectivity",
        "decision",
    ]

    for field in fields_as_elements:
        value = row[field]
        child = ET.SubElement(house_el, field)
        child.text = str(value)

    return house_el

# Gera o ficheiro XML com todas as casas do dataset limpo.
def generate_xml() -> None:
    df = load_clean_dataset()
    print(f"Gerar XML com todas as {len(df)} casas.")

    root = ET.Element("houses")

    for _, row in df.iterrows():
        house_el = build_house_element(row)
        root.append(house_el)

    # garantir que a pasta xml/ existe
    XML_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    tree = ET.ElementTree(root)
    tree.write(
        XML_OUTPUT,
        encoding="utf-8",
        xml_declaration=True,
        pretty_print=True,
    )

    print(f"XML gerado em: {XML_OUTPUT}")


def main():
    generate_xml()


if __name__ == "__main__":
    main()