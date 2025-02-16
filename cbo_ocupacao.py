import csv
import psycopg2
import pysolr

# Configuração do PostgreSQL
DB_CONFIG = {
    "dbname": "cbo_ocupacao",
    "user": "postgres",
    "password": "123456",
    "host": "app_postgres",  # Nome do serviço do Postgres no Docker Swarm
    "port": "5432",  # A porta padrão do Postgres
}

# URL do Solr
SOLR_URL = "http://app_solr:8983/solr/cbo_ocupacao"  # Nome do serviço do Solr no Docker Swarm

try:
    # Conectar ao banco de dados PostgreSQL
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("Conexão com o banco de dados estabelecida.")

    # Criar tabela no PostgreSQL se não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cbo_ocupacao (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL
        )
    """)
    conn.commit()
    print("Tabela verificada/criada com sucesso.")

    # Ler e inserir dados do CSV no PostgreSQL
    with open("CBO2002 - Ocupacao.csv", newline="", encoding="ISO-8859-1") as csvfile:
        arquivo_lido = csv.reader(csvfile)
        next(arquivo_lido)  # Pular cabeçalho
        for linha in arquivo_lido:
            itens = linha[0].split(';')
            id, titulo = itens[0], itens[1]
            cursor.execute("INSERT INTO cbo_ocupacao (id, titulo) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;", (id, titulo))

    conn.commit()
    print("Dados inseridos no PostgreSQL com sucesso.")

    # Consultar todos os dados do PostgreSQL
    cursor.execute("SELECT id, titulo FROM cbo_ocupacao;")
    registros = cursor.fetchall()
    print(f"Consultados {len(registros)} registros do PostgreSQL.")

    # Enviar dados ao Solr
    solr = pysolr.Solr(SOLR_URL, always_commit=True)
    documentos = [{"id": str(reg[0]), "titulo": reg[1]} for reg in registros]
    solr.add(documentos)

    print(f"{len(documentos)} registros indexados no Solr com sucesso.")

except Exception as e:
    print(f"Erro: {e}")

finally:
    if conn:
        cursor.close()
        conn.close()
        print("Conexão com o banco de dados fechada.")
