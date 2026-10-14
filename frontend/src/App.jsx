import { useEffect, useState } from "react";
import { iniciarAuth, keycloak } from "./auth";
import Chat from "./Chat";

export default function App() {
  const [listo, setListo] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    iniciarAuth()
      .then(() => setListo(true))
      .catch(() => setError("No se pudo conectar con el servicio de autenticación."));
  }, []);

  if (error) return <main><p>{error}</p></main>;
  if (!listo) return <main><p>Cargando…</p></main>;

  return (
    <main>
      <header>
        <h1>Agente del Espacio</h1>
        <div>
          <span>{keycloak.tokenParsed?.preferred_username}</span>{" "}
          <button onClick={() => keycloak.logout({ redirectUri: window.location.origin })}>
            Cerrar sesión
          </button>
        </div>
      </header>
      <Chat />
    </main>
  );
}