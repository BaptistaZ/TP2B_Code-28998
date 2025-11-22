import json
from pathlib import Path

import grpc

from core.config import GRPC_HOST, GRPC_PORT
from servers.proto import houses_pb2, houses_pb2_grpc

EVIDENCE_DIR = Path("docs") / "evidence" / "grpc"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


def save_json(data, filename: str) -> None:
    output_path = EVIDENCE_DIR / filename
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[gRPC CLIENTE] Resposta salva em: {output_path}")


def demo() -> None:
    channel = grpc.insecure_channel(f"{GRPC_HOST}:{GRPC_PORT}")
    stub = houses_pb2_grpc.HouseServiceStub(channel)

    # 1) Houses by country
    resp_country = stub.GetHousesByCountry(
        houses_pb2.CountryRequest(country="France", limit=3)
    )
    data_country = [  # converter lista de House -> lista de dicts
        {
            "id": h.id,
            "country": h.country,
            "city": h.city,
            "type": h.type,
            "price": h.price,
            "rooms": h.rooms,
            "bathrooms": h.bathrooms,
            "year_built": h.year_built,
            "decision": h.decision,
        }
        for h in resp_country.houses
    ]
    save_json(data_country, "grpc_houses_france_3.json")

    # 2) Price range
    resp_range = stub.GetHousesByPriceRange(
        houses_pb2.PriceRangeRequest(
            min_price=100000,
            max_price=300000,
            country="France",
            limit=5,
        )
    )
    data_range = [
        {
            "id": h.id,
            "country": h.country,
            "city": h.city,
            "type": h.type,
            "price": h.price,
            "rooms": h.rooms,
            "bathrooms": h.bathrooms,
            "year_built": h.year_built,
            "decision": h.decision,
        }
        for h in resp_range.houses
    ]
    save_json(data_range, "grpc_price_range_france_100k_300k.json")

    # 3) Average price
    resp_avg = stub.GetAveragePriceByCountry(
        houses_pb2.CountryRequest(country="Germany", limit=0)
    )
    save_json(
        {
            "country": resp_avg.country,
            "average_price": resp_avg.average_price,
        },
        "grpc_average_price_germany.json",
    )

    # 4) Decision stats
    resp_stats = stub.GetDecisionStats(houses_pb2.Empty())
    save_json(
        {
            "total": resp_stats.total,
            "bought": resp_stats.bought,
            "not_bought": resp_stats.not_bought,
            "percent_bought": resp_stats.percent_bought,
        },
        "grpc_decision_stats.json",
    )


if __name__ == "__main__":
    demo()