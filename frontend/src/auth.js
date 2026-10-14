import Keycloak from "keycloak-js";

export const keycloak = new Keycloak({
  url: import.meta.env.VITE_KEYCLOAK_URL ?? "http://localhost:8080",
  realm: import.meta.env.VITE_KEYCLOAK_REALM ?? "agente-espacio",
  clientId: import.meta.env.VITE_KEYCLOAK_CLIENT_ID ?? "agente-frontend",
});

// React en desarrollo ejecuta los efectos dos veces, y Keycloak falla si se
// inicializa dos veces. Guardamos la promesa para iniciar una sola vez.
let promesa = null;
export function iniciarAuth() {
  if (!promesa) {
    promesa = keycloak.init({ onLoad: "login-required", pkceMethod: "S256" });
  }
  return promesa;
}

// El token dura 5 minutos: lo renovamos si le quedan menos de 30 segundos.
export async function obtenerToken() {
  await keycloak.updateToken(30);
  return keycloak.token;
}