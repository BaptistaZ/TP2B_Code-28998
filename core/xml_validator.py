from lxml import etree as ET
from .config import XML_OUTPUT, XSD_SCHEMA

# Valida o ficheiro XML (houses.xml) através do schema XSD (houses.xsd) 
def validate_xml() -> bool:
    print(f"A carregar schema XSD de: {XSD_SCHEMA}")
    schema_doc = ET.parse(str(XSD_SCHEMA))
    schema = ET.XMLSchema(schema_doc)

    print(f"A carregar XML de: {XML_OUTPUT}")
    xml_doc = ET.parse(str(XML_OUTPUT))

    print("\n=== Resultado da validação ===")
    is_valid = schema.validate(xml_doc)
    print(f"XML válido? {is_valid}")

    if not is_valid:
        print("\nErros encontrados:")
        for error in schema.error_log:
            print(f"- Linha {error.line}: {error.message}")

    return is_valid


def main():
    validate_xml()


if __name__ == "__main__":
    main()