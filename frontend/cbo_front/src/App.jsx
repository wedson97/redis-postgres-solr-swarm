import Tabela_redis from './Tabela_redis'
import Pesquisa from './Pesquisa'

function App() {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
      <Tabela_redis />
      <Pesquisa />
    </div>
  )
}

export default App
