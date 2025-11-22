from pathlib import Path
import json

from lxml import etree

from core.config import XML_OUTPUT

EVIDENCE_DIR = Path("docs") / "evidence" / "xpath"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


# Carrega o XML completo para memória
def load_xml_tree():
    print(f"[XPATH] A carregar XML de: {XML_OUTPUT}")
    tree = etree.parse(str(XML_OUTPUT))
    return tree


# Converte um elemento <house> numa linha de dataset com alguns campos
def house_element_to_dict(elem) -> dict:
    def get_text(tag):
        child = elem.find(tag)
        return child.text if child is not None else None

    return {
        "id": int(elem.get("id", "0")),
        "country": elem.get("country", ""),
        "city": elem.get("city", ""),
        "type": get_text("type"),
        "price": int(get_text("price") or 0),
        "rooms": int(get_text("rooms") or 0),
        "bathrooms": int(get_text("bathrooms") or 0),
        "year_built": int(get_text("year_built") or 0),
        "decision": int(get_text("decision") or 0),
    }


def save_json(data, filename: str) -> None:
    output_path = EVIDENCE_DIR / filename
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[XPATH] Resultado salvo em: {output_path}")


# ==========================
# Queries XPath
# ==========================

def query_houses_by_country(tree, country: str, limit: int = 5):
    """
    /houses/house[@country='France']
    """
    xpath_expr = f"/houses/house[@country='{country}']"
    elems = tree.xpath(xpath_expr)[:limit]
    return [house_element_to_dict(e) for e in elems]


def query_expensive_houses(tree, min_price: int, country: str | None = None, limit: int = 5):
    """
    /houses/house[price >= min_price] opcionalmente filtrado por país.
    """
    if country:
        xpath_expr = f"/houses/house[@country='{country}' and price >= {min_price}]"
    else:
        xpath_expr = f"/houses/house[price >= {min_price}]"

    elems = tree.xpath(xpath_expr)[:limit]
    return [house_element_to_dict(e) for e in elems]


def query_bought_houses(tree, limit: int = 5):
    """
    /houses/house[decision=1]
    """
    xpath_expr = "/houses/house[decision=1]"
    elems = tree.xpath(xpath_expr)[:limit]
    return [house_element_to_dict(e) for e in elems]


def query_decision_stats_xpath(tree):
    """
    Usa funções XPath para contar casas compradas / não compradas.
    count(/houses/house[decision=1]), etc.
    """
    total = int(tree.xpath("count(/houses/house)"))
    bought = int(tree.xpath("count(/houses/house[decision=1])"))
    not_bought = total - bought
    percent_bought = round((bought / total) * 100, 2) if total > 0 else 0.0

    return {
        "total": total,
        "bought": bought,
        "not_bought": not_bought,
        "percent_bought": percent_bought,
    }


def demo() -> None:
    tree = load_xml_tree()

    # 1) Casas em France
    france_houses = query_houses_by_country(tree, "France", limit=3)
    save_json(france_houses, "xpath_houses_france_3.json")

    # 2) Casas caras em France (preço >= 1_000_000)
    expensive_france = query_expensive_houses(tree, min_price=1_000_000, country="France", limit=5)
    save_json(expensive_france, "xpath_expensive_france_over_1M.json")

    # 3) Casas compradas (decision=1)
    bought_houses = query_bought_houses(tree, limit=5)
    save_json(bought_houses, "xpath_bought_houses_5.json")

    # 4) Estatísticas globais de decisão (apenas XPath)
    stats = query_decision_stats_xpath(tree)
    save_json(stats, "xpath_decision_stats.json")


if __name__ == "__main__":
    demo()