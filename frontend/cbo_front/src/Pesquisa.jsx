import { useState, useEffect } from "react";
import api from "./api/requisicoes";

const Pesquisa = () => {
  const [pesquisa, setPesquisa] = useState("");
  const [sugestoes, setSugestoes] = useState([]);
  const [carregando, setCarregando] = useState(false);

  useEffect(() => {
    const buscarSugestoes = async () => {
      if (pesquisa.trim() === "") {
        setSugestoes([]);
        return;
      }

      setCarregando(true);
      try {
        const resposta = await api.get(`/cbo_ocupacao_solr/${pesquisa}`);
        setSugestoes(resposta.data.map(item => item.titulo[0]));
      } catch (erro) {
        console.error("Erro ao buscar sugestões:", erro);
      } finally {
        setCarregando(false);
      }
    };

    const debounce = setTimeout(() => {
      buscarSugestoes();
    }, 500); 

    return () => clearTimeout(debounce);
  }, [pesquisa]);

  return (
    <>
    
    <div>SOLR<br/>
      
      <input
        type="text"
        value={pesquisa}
        onChange={(e) => setPesquisa(e.target.value)}
        placeholder="Pesquisar..."
      />
      {carregando && <p>Carregando...</p>}
      {sugestoes.length > 0 && (
        <ul>
          {sugestoes.map((titulo, index) => (
            <li key={index}>{titulo}</li>
          ))}
        </ul>
      )}
    </div>
    </>
    
  );
};

export default Pesquisa;
