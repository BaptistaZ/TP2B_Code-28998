from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

from core.config import XMLRPC_HOST, XMLRPC_PORT
from core import houses_service


class RequestHandler(SimpleXMLRPCRequestHandler):
    # Caminho padrão para XML-RPC
    rpc_paths = ("/RPC2",)


def rpc_get_houses_by_country(country: str, limit: int = 50):
    return houses_service.get_houses_by_country(country, limit=limit)


def rpc_get_houses_by_price_range(
    min_price: int,
    max_price: int,
    country: str | None = None,
    limit: int = 50,
):
    return houses_service.get_houses_by_price_range(
        min_price=min_price,
        max_price=max_price,
        country=country,
        limit=limit,
    )


def rpc_get_average_price_by_country(country: str) -> float:
    return houses_service.get_average_price_by_country(country)


def rpc_get_decision_stats():
    return houses_service.get_decision_stats()


def run_xmlrpc_server() -> None:
    with SimpleXMLRPCServer(
        (XMLRPC_HOST, XMLRPC_PORT),
        requestHandler=RequestHandler,
        allow_none=True,
        logRequests=True,
    ) as server:
        print(f"[XML-RPC] Servidor à escuta em {XMLRPC_HOST}:{XMLRPC_PORT} ...")

        server.register_introspection_functions()

        server.register_function(rpc_get_houses_by_country, "get_houses_by_country")
        server.register_function(
            rpc_get_houses_by_price_range,
            "get_houses_by_price_range",
        )
        server.register_function(
            rpc_get_average_price_by_country,
            "get_average_price_by_country",
        )
        server.register_function(rpc_get_decision_stats, "get_decision_stats")

        server.serve_forever()


if __name__ == "__main__":
    run_xmlrpc_server()