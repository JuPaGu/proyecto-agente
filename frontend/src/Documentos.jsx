import { useCallback, useEffect, useRef, useState } from "react";
import { borrarDocumento, listarDocumentos, subirDocumento } from "./api";

export default function Documentos() {
  const [docs, setDocs] = useState([]);
  const [estado, setEstado] = useState(null);
  const [subiendo, setSubiendo] = useState(false);
  const input = useRef(null);

  const cargar = useCallback(() => {
    listarDocumentos()
      .then(setDocs)
      .catch((e) => setEstado({ tipo: "error", texto: e.message }));
  }, []);

  useEffect(() => {
    cargar();
  }, [cargar]);

  async function onArchivo(e) {
    const archivo = e.target.files?.[0];
    if (!archivo) return;
    setSubiendo(true);
    setEstado({
      tipo: "info",
      texto: `Procesando "${archivo.name}"… puede tardar hasta un minuto.`,
    });
    try {
      const r = await subirDocumento(archivo);
      setEstado({
        tipo: "ok",
        texto: `"${r.nombre}" procesado: ${r.fragmentos} fragmentos guardados.`,
      });
      cargar();
    } catch (err) {
      setEstado({ tipo: "error", texto: err.message });
    } finally {
      setSubiendo(false);
      if (input.current) input.current.value = "";
    }
  }

  async function borrar(d) {
    if (!window.confirm(`¿Borrar "${d.nombre}"? El agente dejará de usarlo.`)) return;
    try {
      await borrarDocumento(d.id);
      setEstado({ tipo: "ok", texto: `"${d.nombre}" eliminado.` });
      cargar();
    } catch (err) {
      setEstado({ tipo: "error", texto: err.message });
    }
  }

  return (
    <section className="docs">
      <input
        ref={input}
        type="file"
        accept=".pdf,.txt,.md"
        onChange={onArchivo}
        disabled={subiendo}
      />
      <p className="ayuda">
        PDF, TXT o MD · máximo 5 MB. Lo que subas amplía la base de conocimiento del agente.
      </p>
      {estado && <p className={`estado ${estado.tipo}`}>{estado.texto}</p>}
      {docs.length === 0 ? (
        <p className="vacio">Todavía no hay documentos subidos.</p>
      ) : (
        <ul className="lista">
          {docs.map((d) => (
            <li key={d.id}>
              <span>
                {d.nombre} <small>({d.n_fragmentos} fragmentos)</small>
              </span>
              {d.propio && (
                <button className="peligro" onClick={() => borrar(d)}>
                  Borrar
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}