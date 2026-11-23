import { PageHeader } from "./PageHeader";

interface UnitPlaceholderProps {
  title: string;
  description: string;
  requirements: string;
  unit: string;
}

/** Stands in for a screen whose unit of work is still open. Replaced when the unit is built. */
export function UnitPlaceholder({ title, description, requirements, unit }: UnitPlaceholderProps) {
  return (
    <>
      <PageHeader title={title} description={description} />
      <section className="panel p-5 text-sm">
        <p className="font-semibold">This screen is not built yet.</p>
        <dl className="mt-3 grid gap-x-6 gap-y-2 sm:grid-cols-[max-content_1fr]">
          <dt className="text-muted-foreground">Unit of work</dt>
          <dd>{unit}, in docs/04-delivery/units-of-work.md</dd>
          <dt className="text-muted-foreground">Requirements</dt>
          <dd>{requirements}, in docs/01-product/requirements.md</dd>
          <dt className="text-muted-foreground">Reference</dt>
          <dd>docs/reference/prototype/voc-insights-workspace-latest.html</dd>
        </dl>
      </section>
    </>
  );
}
