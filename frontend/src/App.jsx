import { useEffect, useState } from "react";
import { iniciarAuth, keycloak, obtenerToken } from "./auth";

const API = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export default function App() {
  const [listo, setListo] = useState(false);
  const [error, setError] = useState(null);
  const [resultado, setResultado] = useState("");

  useEffect(() => {
    iniciarAuth()
      .then(() => setListo(true))
      .catch(() => setError("No se pudo conectar con el servicio de autenticación."));
  }, []);

  async function probarApi() {
    setResultado("Consultando...");
    try {
      const token = await obtenerToken();
      const r = await fetch(`${API}/historial`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const datos = await r.json();
      setResultado(`La API respondió: ${datos.length} mensajes en tu historial.`);
    } catch (e) {
      setResultado(`Falló la llamada: ${e.message}`);
    }
  }

  if (error) return <p>{error}</p>;
  if (!listo) return <p>Cargando...</p>;

  return (
    <main>
      <h1>Agente del Espacio</h1>
      <p>
        Sesión iniciada como <strong>{keycloak.tokenParsed?.preferred_username}</strong>
      </p>
      <button onClick={probarApi}>Probar API</button>{" "}
      <button onClick={() => keycloak.logout({ redirectUri: window.location.origin })}>
        Cerrar sesión
      </button>
      <p>{resultado}</p>
    </main>
  );
}