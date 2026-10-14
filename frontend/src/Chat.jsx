import { useEffect, useRef, useState } from "react";
import { historial, preguntar } from "./api";
import Mascota from "./Mascota";

// Preguntas que ya respondieron bien en nuestras pruebas
const EJEMPLOS = [
  "¿Qué es un agujero negro?",
  "¿Qué es un púlsar?",
  "¿Qué es el telescopio Hubble?",
  "¿Qué es la energía oscura?",
];

const FRASES = {
  listo: "¡Listo para explorar, jefe!",
  pensando: "Calculando órbita…",
  rechazo: "Eso no está en mis mapas estelares. Sube un documento y lo exploramos.",
  error: "¡Houston, tenemos un problema!",
};

function Fuente({ f }) {
  // Solo enlazamos URLs https: un "javascript:..." no debe volverse un enlace.
  if (f.url.startsWith("https://")) {
    return (
      <a className="chip" href={f.url} target="_blank" rel="noopener noreferrer">
        {f.titulo}
      </a>
    );
  }
  return <span className="chip chip-doc">{f.titulo} · documento subido</span>;
}

export default function Chat() {
  const [mensajes, setMensajes] = useState([]);
  const [texto, setTexto] = useState("");
  const [cargando, setCargando] = useState(false);
  const [inicial, setInicial] = useState(true);
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
      .catch(() => {})
      .finally(() => setInicial(false));
  }, []);

  useEffect(() => {
    fin.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }, [mensajes, cargando]);

  async function enviarPregunta(pregunta) {
    pregunta = pregunta.trim();
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

  function onSubmit(e) {
    e.preventDefault();
    enviarPregunta(texto);
  }

  const ultimo = mensajes[mensajes.length - 1];
  const estadoMascota = cargando
    ? "pensando"
    : ultimo?.error
      ? "error"
      : ultimo?.decision === "rechazar"
        ? "rechazo"
        : "listo";

  return (
    <section className="chat">
      <aside className="lateral">
        <p className="globo">{FRASES[estadoMascota]}</p>
        <Mascota estado={estadoMascota} />
      </aside>

      <div className="columna">
        <div className="mensajes" aria-live="polite">
          {mensajes.length === 0 && !inicial && !cargando && (
            <div className="bienvenida">
              <h2>¡A explorar el cosmos!</h2>
              <p>
                Pregunta sobre planetas, estrellas, misiones y teorías del universo.
                Respondo solo con lo que hay en mi base de conocimiento.
              </p>
              <div className="sugerencias">
                {EJEMPLOS.map((e) => (
                  <button key={e} type="button" onClick={() => enviarPregunta(e)}>
                    {e}
                  </button>
                ))}
              </div>
            </div>
          )}

          {mensajes.map((m, i) => (
            <div key={i} className={`fila ${m.rol}`}>
              {m.rol === "agente" && (
                <div className="avatar agente-av" aria-hidden="true">✦</div>
              )}
              <div
                className={`burbuja ${m.rol} ${m.error ? "error" : ""} ${
                  m.decision === "rechazar" ? "rechazo" : ""
                }`}
              >
                {m.decision === "rechazar" && (
                  <span className="etiqueta">Sin información suficiente</span>
                )}
                <p>{m.texto}</p>
                {m.fuentes?.length > 0 && (
                  <div className="chips">
                    <span className="chips-titulo">Fuentes</span>
                    {m.fuentes.map((f, j) => (
                      <Fuente key={j} f={f} />
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {cargando && (
            <div className="fila agente">
              <div className="avatar agente-av" aria-hidden="true">✦</div>
              <div className="burbuja agente">
                <span className="puntos"><i /><i /><i /></span>
              </div>
            </div>
          )}
          <div ref={fin} />
        </div>

        <form onSubmit={onSubmit} className="entrada">
          <input
            value={texto}
            onChange={(e) => setTexto(e.target.value)}
            placeholder="Escribe tu pregunta sobre el espacio…"
            aria-label="Pregunta para el agente"
            maxLength={500}
            disabled={cargando}
          />
          <button disabled={cargando || texto.trim().length < 3}>Enviar</button>
        </form>
      </div>
    </section>
  );
}