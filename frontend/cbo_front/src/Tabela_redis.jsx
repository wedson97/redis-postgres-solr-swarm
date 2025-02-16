import { useState, useEffect } from "react";
import api from "./api/requisicoes";

export default function Tabela_redis() {
  const [dados, setDados] = useState([]);
  const [pesquisa, setPesquisa] = useState("");
  const [paginaAtual, setPaginaAtual] = useState(1);
  const [tempoDeCarregamento, setTempoDeCarregamento] = useState(null); 
  const itensPorPagina = 10;

  useEffect(() => {
    const buscarDados = async () => {
      const inicio = performance.now();
      try {
        const resposta = await api.get("/cbo_ocupacao");
        setDados(resposta.data);
      } catch (erro) {
        console.error("Erro ao buscar dados:", erro);
      }
      const fim = performance.now();
      const tempo = fim - inicio;
      setTempoDeCarregamento(tempo.toFixed(2));
    };

    buscarDados();
  }, []);

  const dadosFiltrados = dados.filter((item) =>
    item.titulo.toLowerCase().includes(pesquisa.toLowerCase())
  );

  const totalDePaginas = Math.ceil(dadosFiltrados.length / itensPorPagina);
  const dadosPaginados = dadosFiltrados.slice(
    (paginaAtual - 1) * itensPorPagina,
    paginaAtual * itensPorPagina
  );

  return (
    <div className="max-w-3xl mx-auto p-4">REDIS<br/>
      <input
        type="text"
        placeholder="Pesquisar título..."
        value={pesquisa}
        onChange={(e) => setPesquisa(e.target.value)}
        className="mb-4 w-full p-2 border rounded"
      />

      {tempoDeCarregamento && (
        <div className="mb-4 text-gray-600">
          Tempo de Carregamento: {tempoDeCarregamento} ms
        </div>
      )}

      <table className="w-full border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-200">
            <th className="border border-gray-300 p-2">ID</th>
            <th className="border border-gray-300 p-2">Título</th>
          </tr>
        </thead>
        <tbody>
          {dadosPaginados.map((item) => (
            <tr key={item.id} className="hover:bg-gray-100">
              <td className="border border-gray-300 p-2">{item.id}</td>
              <td className="border border-gray-300 p-2">{item.titulo}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="flex justify-between items-center mt-4">
        <button
          disabled={paginaAtual === 1}
          onClick={() => setPaginaAtual(paginaAtual - 1)}
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-300"
        >
          Anterior
        </button>
        <span>Página {paginaAtual} de {totalDePaginas}</span>
        <button
          disabled={paginaAtual === totalDePaginas}
          onClick={() => setPaginaAtual(paginaAtual + 1)}
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-300"
        >
          Próximo
        </button>
      </div>
    </div>
  );
}
