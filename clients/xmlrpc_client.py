import json
from pathlib import Path
from xmlrpc.client import ServerProxy

from core.config import XMLRPC_HOST, XMLRPC_PORT


EVIDENCE_DIR = Path("docs") / "evidence" / "xmlrpc"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

def save_json(data, filename: str) -> None:
    output_path = EVIDENCE_DIR / filename
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[XML-RPC CLIENTE] Resposta salva em: {output_path}")

def demo() -> None:
    url = f"http://{XMLRPC_HOST}:{XMLRPC_PORT}"
    client = ServerProxy(url, allow_none=True)
    print(f"[XML-RPC CLIENTE] Conectado a {url}")

    # 1) casas por país
    france_houses = client.get_houses_by_country("France", 3)
    save_json(france_houses, "xmlrpc_houses_france_3.json")

    # 2) intervalo de preços
    price_range = client.get_houses_by_price_range(100000, 300000, "France", 5)
    save_json(price_range, "xmlrpc_price_range_france_100k_300k.json")

    # 3) preço médio
    avg_germany = client.get_average_price_by_country("Germany")
    save_json(
        {"country": "Germany", "average_price": avg_germany},
        "xmlrpc_average_price_germany.json",
    )

    # 4) estatísticas de decisão
    stats = client.get_decision_stats()
    save_json(stats, "xmlrpc_decision_stats.json")


if __name__ == "__main__":
    demo()