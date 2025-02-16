from flask_restful import Resource, reqparse, marshal
import redis
import json 
import time
from models.cbo_ocupacao import cbo_ocupacao_fields, Cbo_ocupacao_Model
import pysolr

class Cbo_ocupacao(Resource):
    parser = reqparse.RequestParser()

    def get(self):
        redis_client = redis.StrictRedis(host='redis', port=6379, db=0)  # Usar o nome do serviço Redis no Docker

        # Medindo o tempo de consulta no Redis
        comeco_requisicaoredis = time.time() 
        cached_data = redis_client.get("cbo_ocupacao_cache")
        termico_requisicao_redis = time.time()

        if cached_data:
            cached_data = json.loads(cached_data)
            print(f"Tempo de consulta no Redis: {((termico_requisicao_redis - comeco_requisicaoredis) * 1000):.2f} ms")
            return cached_data, 200

        # Medindo o tempo de consulta ao banco de dados
        comeco_requisicao_db = time.time()
        cbos = Cbo_ocupacao_Model.query.all()
        termico_requisicao_db = time.time()

        serialized_data = json.dumps(marshal(cbos, cbo_ocupacao_fields))
        redis_client.set("cbo_ocupacao_cache", serialized_data, ex=3600)  # Cache com expiração de 1 hora

        print(f"Tempo de consulta ao banco de dados: {((termico_requisicao_db - comeco_requisicao_db) * 1000):.2f} ms")
        return marshal(cbos, cbo_ocupacao_fields), 200
    

class Cbo_ocupacao_solr(Resource):
    parser = reqparse.RequestParser()

    def get(self, busca):
        consulta = f"titulo:{busca}~10"
        solr_url = "http://solr:8983/solr/cbo_ocupacao/select"  # Usar o nome do serviço Solr no Docker

        # Montar a URL de consulta
        solr = pysolr.Solr(f"{solr_url}?q={consulta}&wt=json", timeout=10)

        inicio_solr = time.time()
        try:
            resultados = solr.search(consulta)
        except Exception as e:
            return {"message": f"Erro ao consultar Solr: {str(e)}"}, 500

        fim_solr = time.time()

        if resultados:
            dados_resultado = [doc for doc in resultados]
            print(f"Tempo de consulta no Solr: {((fim_solr - inicio_solr) * 1000):.2f} ms")
            return dados_resultado, 200

        return {"message": "Nenhum dado encontrado."}, 404
