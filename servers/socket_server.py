import json
import socket
from typing import Any, Dict

from core import houses_service

from core.config import SOCKET_HOST as HOST, SOCKET_PORT as PORT

# Recebe uma string de comando e devolve um dicionário com o resultado.
def process_command(command: str) -> Dict[str, Any]:
    command = command.strip()
    parts = command.split("|")

    if not parts:
        return {"status": "error", "message": "Comando vazio"}

    cmd = parts[0].upper()

    try:
        if cmd == "LIST_BY_COUNTRY":
            if len(parts) < 2:
                return {"status": "error", "message": "Uso: LIST_BY_COUNTRY|<country>|[limit]"}

            country = parts[1]
            limit = int(parts[2]) if len(parts) >= 3 else 50

            houses = houses_service.get_houses_by_country(country, limit=limit)
            return {"status": "ok", "command": cmd, "country": country, "limit": limit, "data": houses}

        elif cmd == "PRICE_RANGE":
            if len(parts) < 3:
                return {"status": "error", "message": "Uso: PRICE_RANGE|<min>|<max>|[country]|[limit]"}

            min_price = int(parts[1])
            max_price = int(parts[2])
            country = parts[3] if len(parts) >= 4 and parts[3] else None
            limit = int(parts[4]) if len(parts) >= 5 else 50

            houses = houses_service.get_houses_by_price_range(
                min_price=min_price,
                max_price=max_price,
                country=country,
                limit=limit,
            )
            return {
                "status": "ok",
                "command": cmd,
                "min_price": min_price,
                "max_price": max_price,
                "country": country,
                "limit": limit,
                "data": houses,
            }

        elif cmd == "AVERAGE_PRICE":
            if len(parts) < 2:
                return {"status": "error", "message": "Uso: AVERAGE_PRICE|<country>"}

            country = parts[1]
            avg_price = houses_service.get_average_price_by_country(country)
            return {
                "status": "ok",
                "command": cmd,
                "country": country,
                "average_price": avg_price,
            }

        elif cmd == "DECISION_STATS":
            stats = houses_service.get_decision_stats()
            return {"status": "ok", "command": cmd, "data": stats}

        else:
            return {"status": "error", "message": f"Comando desconhecido: {cmd}"}

    except Exception as e:
        # Nunca rebentar o servidor por causa de um pedido
        return {"status": "error", "message": f"Erro ao processar comando: {str(e)}"}


# Trata UM pedido de UM cliente. O protocolo é 1 pedido por ligação TCP.
def handle_client(conn: socket.socket, addr) -> None:
    print(f"[SERVER] Ligação de {addr}")

    try:
        data = conn.recv(4096) # Buffer size de 4KB
        if not data:
            print("[SERVER] Nenhum dado recebido (ligação vazia).")
            return

        command = data.decode("utf-8").strip()
        print(f"[SERVER] Comando recebido: {command}")

        response_dict = process_command(command)
        response_json = json.dumps(response_dict)

        # Enviar resposta com newline para facilitar debugging
        conn.sendall((response_json + "\n").encode("utf-8"))
        print("[SERVER] Resposta enviada.")

    finally:
        conn.close()
        print(f"[SERVER] Ligação fechada com {addr}")


# Ciclo principal do servidor: fica a aguardar ligações e trata uma de cada vez.
def run_server() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print(f"[SERVER] Servidor TCP à escuta em {HOST}:{PORT} ...")

        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)


if __name__ == "__main__":
    run_server()