import React from 'react';

const DiagramList = ({ diagrams, onDiagramSelect }) => {
  return (
    <div className="diagram-list mt-4">
      <h3 className="text-lg font-semibold mb-2">Diagramas Anteriores</h3>
      {diagrams.length === 0 ? (
        // Si no hay diagramas, muestra un mensaje indicando que no hay diagramas previos
        <p>No hay diagramas previos.</p>
      ) : (
        // Si hay diagramas, muestra una lista de ellos
        <ul className="space-y-2">
          {diagrams.map((diagram, index) => (
            // Cada diagrama se muestra como un elemento de lista
            <li key={index} className="flex items-center">
              <button
                // Al hacer clic en el botón, se selecciona el diagrama correspondiente
                onClick={() => onDiagramSelect(diagram)}
                className="text-blue-600 hover:text-blue-800 underline focus:outline-none"
              >
                {diagram.name || `Diagrama ${index + 1}`}
              </button>
              <span className="text-gray-500 text-sm ml-2">
                {new Date(diagram.timestamp).toLocaleString()}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default DiagramList;