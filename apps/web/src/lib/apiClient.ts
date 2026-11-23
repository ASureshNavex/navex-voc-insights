import { InteractionRequiredAuthError } from "@azure/msal-browser";

import { apiTokenRequest, loginRequest } from "./authConfig";
import { msalInstance } from "./msal";

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api/v1";
const ACCESS_DENIED_EVENT = "voc:access-denied";

export class ApiError extends Error {
  constructor(
    readonly status: number,
    readonly title: string,
    detail: string,
  ) {
    super(detail);
  }
}

type QueryValue = string | number | boolean | null | undefined | readonly string[];

interface RequestOptions {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  query?: Record<string, QueryValue>;
  body?: unknown;
  signal?: AbortSignal;
}

async function accessToken(forceRefresh = false): Promise<string> {
  const account = msalInstance.getActiveAccount() ?? msalInstance.getAllAccounts()[0];
  try {
    const result = await msalInstance.acquireTokenSilent({
      ...apiTokenRequest,
      account,
      forceRefresh,
    });
    return result.accessToken;
  } catch (error) {
    if (error instanceof InteractionRequiredAuthError || !account) {
      await msalInstance.acquireTokenRedirect(loginRequest());
    }
    throw error;
  }
}

function buildUrl(path: string, query: RequestOptions["query"]): string {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(query ?? {})) {
    if (value === null || value === undefined || value === "") continue;
    if (Array.isArray(value)) value.forEach((item) => params.append(key, item));
    else params.set(key, String(value));
  }
  const search = params.toString();
  return `${BASE_URL}${path}${search ? `?${search}` : ""}`;
}

async function send(path: string, options: RequestOptions, token: string): Promise<Response> {
  return fetch(buildUrl(path, options.query), {
    method: options.method ?? "GET",
    headers: {
      Authorization: `Bearer ${token}`,
      ...(options.body === undefined ? {} : { "Content-Type": "application/json" }),
    },
    body: options.body === undefined ? undefined : JSON.stringify(options.body),
    signal: options.signal,
  });
}

async function toError(response: Response): Promise<ApiError> {
  const problem = (await response.json().catch(() => ({}))) as { title?: string; detail?: string };
  return new ApiError(
    response.status,
    problem.title ?? response.statusText,
    problem.detail ?? "The request could not be completed.",
  );
}

/** The single HTTP client. Components and hooks never call fetch themselves. */
export async function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  let response = await send(path, options, await accessToken());
  if (response.status === 401) {
    response = await send(path, options, await accessToken(true));
  }
  if (response.status === 401) {
    await msalInstance.acquireTokenRedirect(loginRequest());
  }
  if (response.status === 403) {
    // Keep the session; the shell shows an access-denied notice.
    window.dispatchEvent(new CustomEvent(ACCESS_DENIED_EVENT));
  }
  if (!response.ok) throw await toError(response);
  return response.status === 204 ? (undefined as T) : ((await response.json()) as T);
}

export function onAccessDenied(listener: () => void): () => void {
  window.addEventListener(ACCESS_DENIED_EVENT, listener);
  return () => window.removeEventListener(ACCESS_DENIED_EVENT, listener);
}
