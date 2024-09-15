import React, { useState, useEffect } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import ImageDisplay from './components/ImageDisplay';
import DiagramList from './components/DiagramList';

const App = () => {
  const [currentDiagram, setCurrentDiagram] = useState(null);
  const [diagrams, setDiagrams] = useState([]);

  useEffect(() => {
    // Aquí podrías cargar los diagramas guardados desde el almacenamiento local o una API
    const savedDiagrams = JSON.parse(localStorage.getItem('savedDiagrams')) || [];
    setDiagrams(savedDiagrams);
  }, []);

  const handleDataReceived = (data) => {
    if (data.url) {
      const newDiagram = {
        ...data,
        timestamp: new Date().toISOString(),
        name: `Diagrama ${diagrams.length + 1}`
      };
      setCurrentDiagram(newDiagram);
      setDiagrams(prevDiagrams => {
        const updatedDiagrams = [newDiagram, ...prevDiagrams];
        localStorage.setItem('savedDiagrams', JSON.stringify(updatedDiagrams));
        return updatedDiagrams;
      });
    } else {
      setCurrentDiagram(data);
    }
  };

  const handleDiagramSelect = (diagram) => {
    setCurrentDiagram(diagram);
  };

  return (
    <div className="app flex">
      <Sidebar onDataReceived={handleDataReceived} />
      <div className="content flex-grow p-4">
        <h1 className="text-2xl font-bold mb-4">Generador de Diagramas de Bases de Datos</h1>
        <p className="mb-4">Construye diagramas de bases de datos automáticamente a partir de la configuración proporcionada.</p>
        <div className="flex">
          <div className="w-2/3 pr-4">
            <ImageDisplay data={currentDiagram} />
          </div>
          <div className="w-1/3">
            <DiagramList diagrams={diagrams} onDiagramSelect={handleDiagramSelect} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;