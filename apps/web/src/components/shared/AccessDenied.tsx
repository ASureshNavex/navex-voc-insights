import { PageHeader } from "./PageHeader";

export function AccessDenied({ detail }: { detail?: string }) {
  return (
    <PageHeader
      title="Access denied"
      description={
        detail ??
        "Your account does not include this page. Access comes from your Corp AD group. Ask your team lead or the VoC admin team to add you."
      }
    />
  );
}
