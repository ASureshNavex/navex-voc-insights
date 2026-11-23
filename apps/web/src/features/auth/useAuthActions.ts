import { useMsal } from "@azure/msal-react";
import { useCallback } from "react";

export function useAuthActions(): { signOut: () => void } {
  const { instance } = useMsal();
  const signOut = useCallback(() => void instance.logoutRedirect(), [instance]);
  return { signOut };
}
