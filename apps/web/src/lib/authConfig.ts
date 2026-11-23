import { BrowserCacheLocation, type Configuration, type RedirectRequest } from "@azure/msal-browser";

/** Corp AD (Microsoft Entra ID): authorization code with PKCE. Tokens stay in memory. */
export const msalConfig: Configuration = {
  auth: {
    clientId: import.meta.env.VITE_ENTRA_CLIENT_ID,
    authority: `https://login.microsoftonline.com/${import.meta.env.VITE_ENTRA_TENANT_ID}`,
    redirectUri: window.location.origin,
  },
  cache: { cacheLocation: BrowserCacheLocation.MemoryStorage },
};

const apiScopes = [import.meta.env.VITE_API_SCOPE];

export const apiTokenRequest = { scopes: apiScopes };

/** Sign-in returns the user to the page they asked for, so alert and CTA links survive. */
export function loginRequest(): RedirectRequest {
  return { scopes: apiScopes, redirectStartPage: window.location.href };
}
