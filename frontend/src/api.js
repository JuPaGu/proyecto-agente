import { obtenerToken } from "./auth";

const API = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function llamar(ruta, opciones = {}) {
  const token = await obtenerToken();
  const r = await fetch(`${API}${ruta}`, {
    ...opciones,
    headers: { ...(opciones.headers ?? {}), Authorization: `Bearer ${token}` },
  });
  if (!r.ok) {
    let detalle = `Error ${r.status}`;
    try {
      const d = await r.json();
      if (typeof d.detail === "string") detalle = d.detail;
      else if (Array.isArray(d.detail)) detalle = "Los datos enviados no son válidos.";
    } catch {
      /* la respuesta no era JSON */
    }
    throw new Error(detalle);
  }
  return r.status === 204 ? null : r.json();
}

export const preguntar = (pregunta) =>
  llamar("/preguntar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pregunta }),
  });

export const historial = () => llamar("/historial");
export const listarDocumentos = () => llamar("/documentos");
export const borrarDocumento = (id) => llamar(`/documentos/${id}`, { method: "DELETE" });

export function subirDocumento(archivo) {
  const datos = new FormData();
  datos.append("archivo", archivo);
  return llamar("/documentos", { method: "POST", body: datos });
}