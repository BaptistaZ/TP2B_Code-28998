from pathlib import Path

# Diretório base do projeto (pasta onde está o README.md)
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminhos para ficheiros de dados
DATA_RAW_CSV = BASE_DIR / "data" / "raw" / "global_house_purchase_dataset.csv"
DATA_CLEAN_CSV = BASE_DIR / "data" / "clean" / "houses_clean.csv"

# Caminhos para XML / XSD 
XML_OUTPUT = BASE_DIR / "xml" / "houses.xml"
XSD_SCHEMA = BASE_DIR / "xml" / "schemas" / "houses.xsd"

