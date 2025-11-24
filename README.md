# 🧩 Integração de Sistemas - TP2  
**Implementação em Python de Sockets, XML-RPC e gRPC**

📘 Descrição

Este projeto tem como objetivo aplicar conceitos de Integração de Sistemas através da implementação de três abordagens de comunicação cliente - servidor: Sockets TCP, XML-RPC e gRPC - complementadas com a análise de dados XML via XPath e XQuery.
O sistema baseia-se num dataset de decisões de compra de habitação, processado e convertido em XML validado por XSD, permitindo consultas remotas e geração automática de evidências.

⚙️ Tecnologias

	•	Python 3.12
	•	Docker / Docker Compose
	•	gRPC + Protocol Buffers
	•	XML / XSD / XPath / XQuery
	•	Pandas

🧠 Estrutura Geral

	•	core/ → Lógica principal e camada de serviço de dados (houses_service.py)
	•	servers/ → Implementações Socket, XML-RPC e gRPC
	•	clients/ → Clientes para teste de cada serviço
	•	xml_analysis/ → Consultas XPath e XQuery
	•	docs/evidence/ → Resultados e evidências em JSON/XML

🚀 Execução

🔹 1. Levantar os servidores

Cada servidor é isolado num container Docker:

docker compose up socket-server
docker compose up xmlrpc-server
docker compose up grpc-server

🔹 2. Executar os clientes

No terminal, correr o cliente correspondente:

# Cliente Socket
python -m clients.socket_client

# Cliente XML-RPC
python -m clients.xmlrpc_client

# Cliente gRPC
python -m clients.grpc_client

🔹 3. Resultados

As respostas são guardadas automaticamente em:

docs/evidence/socket/
docs/evidence/xmlrpc/
docs/evidence/grpc/

🔹 4. Consultas XPath e XQuery

# Consultas XPath
python -m xml_analysis.xpath_queries

# Consultas XQuery
python -m xml_analysis.xquery_analysis

As evidências geradas são armazenadas em:

docs/evidence/xpath/
docs/evidence/xquery/


👨‍💻 Autor

Tiago Baptista
Instituto Politécnico de Viana do Castelo (IPVC)
📚 Unidade Curricular: Integração de Sistemas