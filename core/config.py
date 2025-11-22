import os
from pathlib import Path

# Diretório base do projeto (pasta onde está o README.md)
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminhos para ficheiros de dados
DATA_RAW_CSV = BASE_DIR / "data" / "raw" / "global_house_purchase_dataset.csv"
DATA_CLEAN_CSV = BASE_DIR / "data" / "clean" / "houses_clean.csv"

# Caminhos para XML / XSD 
XML_OUTPUT = BASE_DIR / "xml" / "houses.xml"
XSD_SCHEMA = BASE_DIR / "xml" / "schemas" / "houses.xsd"

# ==========================
# NETWORK CONFIG (with env vars)
# ==========================

# TCP sockets
SOCKET_HOST = os.getenv("SOCKET_HOST", "127.0.0.1")
SOCKET_PORT = int(os.getenv("SOCKET_PORT", "5050"))

# XML-RPC
XMLRPC_HOST = os.getenv("XMLRPC_HOST", "127.0.0.1")
XMLRPC_PORT = int(os.getenv("XMLRPC_PORT", "5051"))

# gRPC
GRPC_HOST = os.getenv("GRPC_HOST", "127.0.0.1")
GRPC_PORT = int(os.getenv("GRPC_PORT", "5052"))

