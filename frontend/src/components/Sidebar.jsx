import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const Sidebar = ({ onDataReceived }) => {
  // Estado para almacenar los datos del formulario
  const [formData, setFormData] = useState({
    dbType: '',
    host: '',
    port: '',
    username: '',
    password: '',
    databaseName: ''
  });
  // Estado para controlar la visibilidad de la contraseña
  const [showPassword, setShowPassword] = useState(false);
  // Estado para controlar si la solicitud está en proceso
  const [isLoading, setIsLoading] = useState(false);

  // Función para alternar la visibilidad de la contraseña
  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  // Función para manejar los cambios en los campos del formulario
  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value
    });
  };

  // Función para manejar el envío del formulario
  const handleSubmit = (e) => {
    e.preventDefault();
    setIsLoading(true);

    // Construir los parámetros de la consulta
    const queryParams = new URLSearchParams({
      bd: formData.dbType,
      host: formData.host,
      port: formData.port,
      user: formData.username,
      password: formData.password,
      database: formData.databaseName
    }).toString();

    // Realizar la solicitud al servidor
    fetch(`http://localhost:8000/diagram?${queryParams}`, {
      method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
      setIsLoading(false);

      const combinedData = {
        ...data, // Datos de la API
        dbType: formData.dbType,
        host: formData.host,
        port: formData.port,
        username: formData.username,
        password: formData.password,
        databaseName: formData.databaseName
      };
      
      // Llamar a la función onDataReceived con los datos combinados
      onDataReceived(combinedData); // Llamar a la función onDataReceived con los datos recibidos
    })
    .catch((error) => {
      setIsLoading(false);
      console.error('Error:', error);
      onDataReceived({ error: 'Error al obtener los datos' }); // Llamar a la función onDataReceived con un mensaje de error
    });
  };

  return (
    <div className="sidebar bg-light p-3 text-black" style={{ height: '100vh', width: '250px', position: 'fixed', top: 0, left: 0, borderRight: '1px solid #dee2e6' }}>
      <h4>Configuración de Base de Datos</h4>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="dbType" className="form-label text-black">Tipo de servidor de base de datos</label>
          <select className="form-select" id="dbType" value={formData.dbType} onChange={handleInputChange} required>
            <option value="" disabled>Selecciona uno</option>
            <option value="mysql">MySQL</option>
            <option value="postgres">PostgreSQL</option> {/* Cambiado de 'postgresql' a 'postgres' */}
            <option value="sqlserver">SQL Server</option>
          </select>
        </div>
        <div className="mb-3">
          <label htmlFor="host" className="form-label text-black">Host</label>
          <input type="text" className="form-control" id="host" value={formData.host} onChange={handleInputChange} required />
        </div>
        <div className="mb-3">
          <label htmlFor="port" className="form-label text-black">Puerto</label>
          <input type="number" className="form-control" id="port" value={formData.port} onChange={handleInputChange} required />
        </div>
        <div className="mb-3">
          <label htmlFor="username" className="form-label text-black">Nombre de usuario</label>
          <input type="text" className="form-control" id="username" value={formData.username} onChange={handleInputChange} required />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label text-black">Contraseña</label>
          <div className="input-group">
            <input 
              type={showPassword ? 'text' : 'password'} 
              className="form-control" 
              id="password" 
              value={formData.password}
              onChange={handleInputChange} 
              required 
            />
            <button 
              type="button" 
              className="btn btn-outline-secondary" 
              onClick={togglePasswordVisibility}
            >
              {showPassword ? 'Ocultar' : 'Mostrar'}
            </button>
          </div>
        </div>
        <div className="mb-3">
          <label htmlFor="databaseName" className="form-label text-black">Nombre de la base de datos</label>
          <input type="text" className="form-control" id="databaseName" value={formData.databaseName} onChange={handleInputChange} required />
        </div>
        <button type="submit" className="btn btn-primary">Generar</button>
      </form>
    </div>
  );
}

export default Sidebar;
