import { UnitPlaceholder } from "@/components/shared/UnitPlaceholder";

export function SourceHealthPage() {
  return (
    <UnitPlaceholder
      title="Data source health"
      description="Status of each data source feeding the platform."
      requirements="ADM-04, ADM-05"
      unit="WEB-12"
    />
  );
}
