import json
import socket
from pathlib import Path

from core.config import SOCKET_HOST as HOST, SOCKET_PORT as PORT

EVIDENCE_DIR = Path("docs") / "TPC_evidences"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

# Envia um comando para o servidor TCP e imprime a resposta JSON formatada.
def send_command(command: str, filename: str | None = None) -> None:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall((command + "\n").encode("utf-8"))
        data = s.recv(65535)

    response_text = data.decode("utf-8").strip()

    try:
        response_json = json.loads(response_text)

        if filename:
            output_path = EVIDENCE_DIR / filename
            with output_path.open("w", encoding="utf-8") as f:
                json.dump(response_json, f, indent=2, ensure_ascii=False)
            print(f"\n[CLIENTE] Resposta salva em: {output_path}")

    except json.JSONDecodeError:
        print("\n[CLIENTE] ERRO: Não foi possível gerar JSON.")


# Testar várias operações.
def demo() -> None:
    # 1) Listar casas por país
    send_command("LIST_BY_COUNTRY|France|3", filename="socket_list_by_country_france_3.json")

    # 2) Intervalo de preços num país
    send_command("PRICE_RANGE|100000|300000|France|5", filename="socket_price_range_france_100k_300k.json")

    # 3) Preço médio num país
    send_command("AVERAGE_PRICE|Germany", filename="socket_average_price_germany.json")

    # 4) Estatísticas globais de decisão
    send_command("DECISION_STATS", filename="socket_decision_stats.json")


if __name__ == "__main__":
    demo()

    