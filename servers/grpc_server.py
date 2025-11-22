from concurrent import futures
from typing import List

import grpc

from core.config import GRPC_HOST, GRPC_PORT
from core import houses_service
from servers.proto import houses_pb2, houses_pb2_grpc

# Converte uma linha do dataset para mensagem House
def dict_to_house_msg(d: dict) -> houses_pb2.House:
    
    return houses_pb2.House(
        id=int(d.get("id", 0)),
        country=str(d.get("country", "")),
        city=str(d.get("city", "")),
        type=str(d.get("type", "")),
        price=int(d.get("price", 0)),
        rooms=int(d.get("rooms", 0)),
        bathrooms=int(d.get("bathrooms", 0)),
        year_built=int(d.get("year_built", 0)),
        decision=int(d.get("decision", 0)),
    )


class HouseServiceServicer(houses_pb2_grpc.HouseServiceServicer):
    def GetHousesByCountry(self, request, context):
        houses = houses_service.get_houses_by_country(
            country=request.country,
            limit=request.limit or 50,
        )
        house_msgs: List[houses_pb2.House] = [dict_to_house_msg(h) for h in houses]
        return houses_pb2.HousesResponse(houses=house_msgs)

    def GetHousesByPriceRange(self, request, context):
        country = request.country if request.country else None
        houses = houses_service.get_houses_by_price_range(
            min_price=request.min_price,
            max_price=request.max_price,
            country=country,
            limit=request.limit or 50,
        )
        house_msgs: List[houses_pb2.House] = [dict_to_house_msg(h) for h in houses]
        return houses_pb2.HousesResponse(houses=house_msgs)

    def GetAveragePriceByCountry(self, request, context):
        avg = houses_service.get_average_price_by_country(request.country)
        return houses_pb2.AveragePriceResponse(
            country=request.country,
            average_price=avg,
        )

    def GetDecisionStats(self, request, context):
        stats = houses_service.get_decision_stats()
        return houses_pb2.DecisionStatsResponse(
            total=stats["total"],
            bought=stats["bought"],
            not_bought=stats["not_bought"],
            percent_bought=stats["percent_bought"],
        )


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    houses_pb2_grpc.add_HouseServiceServicer_to_server(HouseServiceServicer(), server)
    server.add_insecure_port(f"{GRPC_HOST}:{GRPC_PORT}")
    print(f"[gRPC] Servidor á escuta em {GRPC_HOST}:{GRPC_PORT} ...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()