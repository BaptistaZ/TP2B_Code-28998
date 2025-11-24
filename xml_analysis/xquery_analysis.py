from collections import defaultdict
from pathlib import Path
import json

from lxml import etree

from core.config import XML_OUTPUT
from .xpath_queries import house_element_to_dict  # reaproveitamos o helper


EVIDENCE_DIR = Path("docs") / "evidence" / "xquery"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


# Carrega o XML Completo
def load_xml_tree():
    print(f"[XQUERY] A carregar XML de: {XML_OUTPUT}")
    tree = etree.parse(str(XML_OUTPUT))
    return tree


def save_json(data, filename: str) -> None:
    output_path = EVIDENCE_DIR / filename
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[XQUERY] Resultado salvo em: {output_path}")


# 1) Média de preço por país
def avg_price_per_country(tree):
    houses = [house_element_to_dict(h) for h in tree.xpath("/houses/house")]

    totals = defaultdict(int)
    counts = defaultdict(int)

    for h in houses:
        country = h["country"]
        totals[country] += h["price"]
        counts[country] += 1

    result = []
    for country in sorted(totals.keys()):
        avg_price = round(totals[country] / counts[country], 2)
        result.append(
            {"country": country, "average_price": avg_price, "count": counts[country]}
        )

    return result


# 2) Número de casas por tipo em cada país
def count_by_type_per_country(tree):
    houses = [house_element_to_dict(h) for h in tree.xpath("/houses/house")]

    # country -> type -> count
    counts = defaultdict(lambda: defaultdict(int))

    for h in houses:
        country = h["country"]
        h_type = h["type"] or "Unknown"
        counts[country][h_type] += 1

    result = []
    for country in sorted(counts.keys()):
        types_list = []
        for h_type, cnt in sorted(counts[country].items(), key=lambda x: (-x[1], x[0])):
            types_list.append({"type": h_type, "count": cnt})
        result.append({"country": country, "types": types_list})

    return result


# 3) Percentagem de casas compradas por país
def decision_percentage_per_country(tree):
    houses = [house_element_to_dict(h) for h in tree.xpath("/houses/house")]

    totals = defaultdict(int)
    boughts = defaultdict(int)

    for h in houses:
        country = h["country"]
        totals[country] += 1
        if h["decision"] == 1:
            boughts[country] += 1

    result = []
    for country in sorted(totals.keys()):
        total = totals[country]
        bought = boughts[country]
        percent = round((bought / total) * 100, 2) if total > 0 else 0.0
        result.append(
            {
                "country": country,
                "total": total,
                "bought": bought,
                "percent_bought": percent,
            }
        )

    return result


def demo() -> None:
    tree = load_xml_tree()

    # 1) Média de preço por país
    avg_prices = avg_price_per_country(tree)
    save_json(avg_prices, "xquery_avg_price_per_country.json")

    # 2) Número de casas por tipo em cada país
    counts_types = count_by_type_per_country(tree)
    save_json(counts_types, "xquery_count_by_type_per_country.json")

    # 3) Percentagem de casas compradas por país
    perc_decision = decision_percentage_per_country(tree)
    save_json(perc_decision, "xquery_decision_percentage_per_country.json")


if __name__ == "__main__":
    demo()