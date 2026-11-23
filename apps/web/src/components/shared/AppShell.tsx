import { Bell, LogOut } from "lucide-react";
import { useEffect, useState } from "react";
import { NavLink, Outlet } from "react-router";

import logoUrl from "@/assets/navex-logo.svg";
import { Button } from "@/components/ui/button";
import { useAuthActions, useEntitlements, type Permission } from "@/features/auth";
import { useUnreadCount } from "@/features/notifications";
import { onAccessDenied } from "@/lib/apiClient";

import { Notice } from "./Notice";

export interface NavItem {
  to: string;
  label: string;
  permission: Permission;
}

/** Top bar, role-aware navigation and the page outlet. The only place that knows the layout. */
export function AppShell({ navigation }: { navigation: NavItem[] }) {
  const { name, permissions } = useEntitlements();
  const { signOut } = useAuthActions();
  const unread = useUnreadCount();
  const [denied, setDenied] = useState(false);
  const items = navigation.filter((item) => permissions.has(item.permission));

  useEffect(() => onAccessDenied(() => setDenied(true)), []);

  return (
    <div className="flex min-h-screen flex-col">
      <header className="app-shell__topbar">
        <div className="flex min-h-(--topbar-height) flex-wrap items-center gap-x-6 gap-y-2 px-4 py-2 md:px-6">
          <NavLink to="/" className="flex items-center gap-3" aria-label="VoC Insights home">
            <img src={logoUrl} alt="NAVEX" className="h-6 w-auto" />
            <span className="border-l pl-3 text-base font-semibold">VoC Insights</span>
          </NavLink>
          <div className="ml-auto flex items-center gap-2">
            <span className="hidden text-sm text-secondary-foreground sm:inline">{name}</span>
            {permissions.has("notifications:read") && (
              <NavLink
                to="/notifications"
                className="relative inline-flex size-9 items-center justify-center rounded-md hover:bg-secondary"
                aria-label={unread ? `Notifications, ${unread} unread` : "Notifications"}
              >
                <Bell className="size-5" aria-hidden="true" />
                {unread > 0 && (
                  <span className="absolute -top-1 -right-1 rounded-full bg-brand px-1.5 text-[0.6875rem] leading-[1.125rem] font-bold text-white">
                    {unread}
                  </span>
                )}
              </NavLink>
            )}
            <Button variant="outline" onClick={signOut}>
              <LogOut aria-hidden="true" />
              Sign out
            </Button>
          </div>
        </div>
        {items.length > 0 && (
          <nav aria-label="Main" className="flex gap-1 overflow-x-auto border-t px-2 md:px-4">
            {items.map((item) => (
              <NavLink key={item.to} to={item.to} className="app-shell__nav-link">
                {item.label}
              </NavLink>
            ))}
          </nav>
        )}
      </header>
      <main className="app-shell__content flex flex-1 flex-col gap-4 p-4 pb-16 md:p-6">
        {denied && <Notice tone="error">Your role does not include that action.</Notice>}
        <Outlet />
      </main>
    </div>
  );
}
