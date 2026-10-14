import { useEffect, useRef, useState } from "react";
import { historial, preguntar } from "./api";

function Fuente({ f }) {
  // Solo enlazamos URLs https: un "javascript:..." no debe volverse un enlace.
  if (f.url.startsWith("https://")) {
    return (
      <a href={f.url} target="_blank" rel="noopener noreferrer">
        {f.titulo}
      </a>
    );
  }
  return <span>{f.titulo} (documento subido)</span>;
}

export default function Chat() {
  const [mensajes, setMensajes] = useState([]);
  const [texto, setTexto] = useState("");
  const [cargando, setCargando] = useState(false);
  const fin = useRef(null);

  useEffect(() => {
    historial()
      .then((filas) => {
        const previos = [...filas].reverse().flatMap((m) => [
          { rol: "usuario", texto: m.pregunta },
          { rol: "agente", texto: m.respuesta, fuentes: m.fuentes, decision: m.decision },
        ]);
        setMensajes(previos);
      })
      .catch(() => {});
  }, []);

  useEffect(() => {
    fin.current?.scrollIntoView({ behavior: "smooth" });
  }, [mensajes, cargando]);

  async function enviar(e) {
    e.preventDefault();
    const pregunta = texto.trim();
    if (pregunta.length < 3 || cargando) return;
    setTexto("");
    setMensajes((m) => [...m, { rol: "usuario", texto: pregunta }]);
    setCargando(true);
    try {
      const r = await preguntar(pregunta);
      setMensajes((m) => [
        ...m,
        { rol: "agente", texto: r.respuesta, fuentes: r.fuentes, decision: r.decision },
      ]);
    } catch (err) {
      setMensajes((m) => [
        ...m,
        { rol: "agente", texto: `No pude responder: ${err.message}`, error: true },
      ]);
    } finally {
      setCargando(false);
    }
  }

  return (
    <section className="chat">
      <div className="mensajes">
        {mensajes.length === 0 && (
          <p className="vacio">Pregunta algo sobre el espacio exterior.</p>
        )}
        {mensajes.map((m, i) => (
          <div
            key={i}
            className={`burbuja ${m.rol} ${m.error ? "error" : ""} ${
              m.decision === "rechazar" ? "rechazo" : ""
            }`}
          >
            <p>{m.texto}</p>
            {m.fuentes?.length > 0 && (
              <p className="fuentes">
                Fuentes:{" "}
                {m.fuentes.map((f, j) => (
                  <span key={j}>
                    {j > 0 && " · "}
                    <Fuente f={f} />
                  </span>
                ))}
              </p>
            )}
          </div>
        ))}
        {cargando && <div className="burbuja agente">Pensando…</div>}
        <div ref={fin} />
      </div>
      <form onSubmit={enviar} className="entrada">
        <input
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
          placeholder="Escribe tu pregunta…"
          maxLength={500}
          disabled={cargando}
        />
        <button disabled={cargando || texto.trim().length < 3}>Enviar</button>
      </form>
    </section>
  );
}