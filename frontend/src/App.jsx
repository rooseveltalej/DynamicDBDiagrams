import React, { useState, useEffect } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import ImageDisplay from './components/ImageDisplay';
import DiagramList from './components/DiagramList';

const App = () => {
  // Estado para el diagrama actual y la lista de diagramas
  const [currentDiagram, setCurrentDiagram] = useState(null);
  const [diagrams, setDiagrams] = useState([]);

  useEffect(() => {
    // Aquí podrías cargar los diagramas guardados desde el almacenamiento local o una API
    const savedDiagrams = JSON.parse(localStorage.getItem('savedDiagrams')) || [];
    setDiagrams(savedDiagrams);
  }, []);

  // Maneja los datos recibidos del componente Sidebar
  const handleDataReceived = (data) => {
    if (data.url) {
      // Si los datos contienen una URL, crea un nuevo diagrama
      const newDiagram = {
        ...data,
        timestamp: new Date().toISOString(),
        name: `Diagrama ${diagrams.length + 1}`,
        bdtype: data.dbType,
        host: data.host,
        port: data.port,
        username: data.username,

      };
      setCurrentDiagram(newDiagram);
      setDiagrams(prevDiagrams => {
        // Actualiza la lista de diagramas y guarda en el almacenamiento local
        const updatedDiagrams = [newDiagram, ...prevDiagrams];
        localStorage.setItem('savedDiagrams', JSON.stringify(updatedDiagrams));
        return updatedDiagrams;
      });
    } else {
      // Si no hay URL, simplemente establece el diagrama actual
      setCurrentDiagram(data);
    }
  };

  // Maneja la selección de un diagrama de la lista
  const handleDiagramSelect = (diagram) => {
    setCurrentDiagram(diagram);
  };

  return (
    <div className="app flex">
      {/* Componente Sidebar que recibe la función handleDataReceived */}
      <Sidebar onDataReceived={handleDataReceived} />
      <div className="content flex-grow p-4">
        <h1 className="text-2xl font-bold mb-4">Generador de Diagramas de Bases de Datos</h1>
        <p className="mb-4">Construye diagramas de bases de datos automáticamente a partir de la configuración proporcionada.</p>
        <div className="flex">
          <div className="w-2/3 pr-4">
          {/* Componente ImageDisplay que muestra el diagrama actual */}
            <ImageDisplay data={currentDiagram} />
          </div>
          <div className="w-1/3">
          {/* Componente DiagramList que muestra la lista de diagramas y maneja la selección */}
            <DiagramList diagrams={diagrams} onDiagramSelect={handleDiagramSelect} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;