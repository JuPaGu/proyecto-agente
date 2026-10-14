import { useEffect, useState } from "react";
import { iniciarAuth, keycloak } from "./auth";
import Chat from "./Chat";
import Documentos from "./Documentos";

export default function App() {
  const [listo, setListo] = useState(false);
  const [error, setError] = useState(null);
  const [vista, setVista] = useState("chat");

  useEffect(() => {
    iniciarAuth()
      .then(() => setListo(true))
      .catch(() => setError("No se pudo conectar con el servicio de autenticación."));
  }, []);

  if (error) return <main><p className="estado error">{error}</p></main>;
  if (!listo) return <main><p className="cargando">Cargando…</p></main>;

  const usuario = keycloak.tokenParsed?.preferred_username ?? "";

  return (
    <main>
      <header className="barra">
        <div className="marca">
          <span className="logo" aria-hidden="true" />
          <div>
            <h1>Agente del Espacio</h1>
            <p className="subtitulo">Asistente sobre astronomía y exploración espacial</p>
          </div>
        </div>
        <div className="sesion">
          <span className="avatar usuario-av" aria-hidden="true">
            {usuario.charAt(0).toUpperCase()}
          </span>
          <span className="nombre">{usuario}</span>
          <button
            className="ghost"
            onClick={() => keycloak.logout({ redirectUri: window.location.origin })}
          >
            Cerrar sesión
          </button>
        </div>
      </header>

      <nav className="tabs">
        <button className={vista === "chat" ? "activa" : ""} onClick={() => setVista("chat")}>
          Chat
        </button>
        <button className={vista === "docs" ? "activa" : ""} onClick={() => setVista("docs")}>
          Documentos
        </button>
      </nav>

      <div hidden={vista !== "chat"}><Chat /></div>
      <div hidden={vista !== "docs"}><Documentos /></div>
    </main>
  );
}