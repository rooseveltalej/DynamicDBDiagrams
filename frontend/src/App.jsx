import './App.css';
import Sidebar from './components/Sidebar';

const App = () => {
  return (
    <div className="content">
      <h1>Generador de Diagramas de Bases de Datos</h1>
      <p>Construye diagramas de bases de datos automáticamente a partir de la configuración proporcionada.</p>
      <Sidebar />
    </div>
  );
};

export default App;
