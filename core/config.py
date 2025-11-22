from pathlib import Path

# Diretório base do projeto (pasta onde está o README.md)
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminhos para ficheiros de dados
DATA_RAW_CSV = BASE_DIR / "data" / "raw" / "global_house_purchase_dataset.csv"
DATA_CLEAN_CSV = BASE_DIR / "data" / "clean" / "houses_clean.csv"

# Caminhos para XML / XSD 
XML_OUTPUT = BASE_DIR / "xml" / "houses.xml"
XSD_SCHEMA = BASE_DIR / "xml" / "schemas" / "houses.xsd"

# =====================================================
# CONFIGURAÇÕES DE REDE (SOCKETS / RPC / gRPC)
# =====================================================

# Endereço e porto do servidor TCP
SOCKET_HOST = "127.0.0.1"
SOCKET_PORT = 5050

# Endereço e porto para o XML-RPC
XMLRPC_HOST = "127.0.0.1"
XMLRPC_PORT = 5001

# Endereço e porto para o gRPC
GRPC_HOST = "127.0.0.1"
GRPC_PORT = 5002

