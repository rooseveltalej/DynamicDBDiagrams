import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const Sidebar = () => {
  // Estado para controlar la visibilidad de la contraseña
  const [showPassword, setShowPassword] = useState(false);

  // Función para alternar la visibilidad de la contraseña
  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <div className="sidebar bg-light p-3" style={{ height: '100vh', width: '250px', position: 'fixed', top: 0, left: 0, borderRight: '1px solid #dee2e6' }}>
      <h4>Configuración de Base de Datos</h4>
      <form>
        <div className="mb-3">
          <label htmlFor="dbType" className="form-label text-black">Tipo de servidor de base de datos</label>
          <select className="form-select" id="dbType" required>
            <option value="" disabled selected>Selecciona uno</option>
            <option value="mysql">MySQL</option>
            <option value="postgresql">PostgreSQL</option>
            <option value="sqlserver">SQL Server</option>
          </select>
        </div>
        <div className="mb-3">
          <label htmlFor="host" className="form-label text-black">Host</label>
          <input type="text" className="form-control" id="host" required />
        </div>
        <div className="mb-3">
          <label htmlFor="port" className="form-label text-black">Puerto</label>
          <input type="number" className="form-control" id="port" required />
        </div>
        <div className="mb-3">
          <label htmlFor="username" className="form-label text-black">Nombre de usuario</label>
          <input type="text" className="form-control" id="username" required />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label text-black">Contraseña</label>
          <div className="input-group">
            <input 
              type={showPassword ? 'text' : 'password'} 
              className="form-control" 
              id="password" 
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
          <input type="text" className="form-control" id="databaseName" required />
        </div>
        <button type="submit" className="btn btn-primary">Guardar</button>
      </form>
    </div>
  );
}

export default Sidebar;
