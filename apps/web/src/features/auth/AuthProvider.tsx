import { InteractionType } from "@azure/msal-browser";
import { MsalAuthenticationTemplate, MsalProvider } from "@azure/msal-react";
import type { ReactNode } from "react";

import { PageLoader } from "@/components/shared/PageLoader";
import { loginRequest } from "@/lib/authConfig";
import { msalInstance } from "@/lib/msal";

/** Signs the user in with Corp AD before anything else renders. There is no sign-in screen. */
export function AuthProvider({ children }: { children: ReactNode }) {
  return (
    <MsalProvider instance={msalInstance}>
      <MsalAuthenticationTemplate
        interactionType={InteractionType.Redirect}
        authenticationRequest={loginRequest()}
        loadingComponent={PageLoader}
      >
        {children}
      </MsalAuthenticationTemplate>
    </MsalProvider>
  );
}
