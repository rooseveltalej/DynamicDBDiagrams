import React from 'react';


const ImageDisplay = ({ data }) => {
  if (!data) {
    return <p>Use el formulario para generar un diagrama.</p>;
  }

    if (data.error) {
    return <p>{data.error}</p>;
    }


  
    if (data.url) {
        return (
          <div className="image-display mt-4"> 
            <h2 className="text-xl font-bold mb-2">{data.name}</h2>
            <img src={data.url} alt="Diagrama de base de datos" className="max-w-full h-auto" />
            <p className="text-sm text-gray-500 mt-2">
              Generado el: {new Date(data.timestamp).toLocaleString()}
            </p>
          </div>
        );
      }
    
      return (
        <div className="image-display mt-4">
          <p>No se pudo generar el diagrama. Por favor, intente de nuevo.</p>
        </div>
      );
    };
    
    export default ImageDisplay;