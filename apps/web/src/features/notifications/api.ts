import { useQuery } from "@tanstack/react-query";

import { useEntitlements } from "@/features/auth";
import { apiRequest } from "@/lib/apiClient";

export interface NotificationItem {
  notification_id: string;
  title: string;
  created_at: string;
  read: boolean;
  sfdc_account_id: string | null;
}

interface NotificationList {
  items: NotificationItem[];
  unread: number;
}

export function useNotifications() {
  const { upn, permissions } = useEntitlements();
  return useQuery({
    queryKey: ["notifications", upn],
    queryFn: () => apiRequest<NotificationList>("/notifications"),
    enabled: permissions.has("notifications:read"),
  });
}

/** Count for the bell icon in the top bar. */
export function useUnreadCount(): number {
  return useNotifications().data?.unread ?? 0;
}
