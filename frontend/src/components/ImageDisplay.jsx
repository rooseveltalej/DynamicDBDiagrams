import React from 'react';


const ImageDisplay = ({ data }) => {
    // Si no hay datos, muestra un mensaje indicando que se use el formulario
  if (!data) {
    return <p>Use el formulario para generar un diagrama.</p>;
  }
    // Si hay un error en los datos, muestra el mensaje de error
    if (data.error) {
    return <p>{data.error}</p>;
    }


    // Si hay una URL en los datos, muestra la imagen y la información asociada
    if (data.url) {
        return (
          <div className="image-display mt-4"> 
            <h2 className="text-xl font-bold mb-2">{data.name}</h2>
            <img src={data.url} alt="Diagrama de base de datos" className="max-w-full h-auto" />
            <p className="text-sm text-gray-500 mt-2">
              Generado el: {new Date(data.timestamp).toLocaleString()}
            </p>
            <p className="text-sm text-gray-500">
              Base de datos: {data.dbType} - Host: {data.host} - Port: {data.port}
            </p>
          </div>
        );
      }
      // Si no se pudo generar el diagrama, muestra un mensaje indicando que se intente de nuevo
      return (
        <div className="image-display mt-4">
          {alert("No se pudo generar el diagrama. Por favor, verifique los datos ingresados e intente de nuevo.")}
          <p>No se pudo generar el diagrama. Por favor, intente de nuevo.</p>
        </div>
      );
    };
    // Exporta el componente para que pueda ser utilizado en otros archivos
    export default ImageDisplay;