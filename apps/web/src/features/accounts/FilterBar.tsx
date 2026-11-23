import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import type { Rating } from "@/types/api";

import { DEFAULT_FILTERS, type AccountFilters, type AccountSort } from "./types";

const RATINGS: { value: Rating; label: string }[] = [
  { value: "R", label: "Red" },
  { value: "Y", label: "Yellow" },
  { value: "G", label: "Green" },
];

interface FilterBarProps {
  filters: AccountFilters;
  onChange: (filters: AccountFilters) => void;
}

/**
 * ACC-06, first slice: search, sort and rating. The remaining filters follow the same pattern:
 * a Label with a native Select, written back through onChange.
 */
export function FilterBar({ filters, onChange }: FilterBarProps) {
  const toggleRating = (rating: Rating) =>
    onChange({
      ...filters,
      status: filters.status.includes(rating)
        ? filters.status.filter((value) => value !== rating)
        : [...filters.status, rating],
    });

  return (
    <section className="panel p-5" aria-label="Filters and search">
      <h2 className="text-base font-semibold">Filters and search</h2>
      <div className="mt-3 grid grid-cols-2 items-end gap-x-3.5 gap-y-3 md:grid-cols-4 xl:grid-cols-6">
        <div className="col-span-2 grid gap-1.5">
          <Label htmlFor="account-search">Search</Label>
          <Input
            id="account-search"
            type="search"
            value={filters.q}
            placeholder="Account, CXM, AE or summary"
            onChange={(event) => onChange({ ...filters, q: event.target.value })}
          />
        </div>
        <div className="grid gap-1.5">
          <Label htmlFor="account-sort">Sort by</Label>
          <Select
            id="account-sort"
            value={filters.sort}
            onChange={(event) => onChange({ ...filters, sort: event.target.value as AccountSort })}
          >
            <option value="priority">Red and churn language first, then ARR</option>
            <option value="arr">ARR (highest first)</option>
            <option value="renewal">Renewal date (soonest first)</option>
          </Select>
        </div>
        <fieldset className="grid gap-1.5">
          <legend className="text-[0.8125rem] font-medium text-secondary-foreground">Rating</legend>
          <div className="flex min-h-9 flex-wrap items-center gap-x-3.5 gap-y-1 text-sm">
            {RATINGS.map(({ value, label }) => (
              <label key={value} className="inline-flex items-center gap-1.5 font-medium">
                <input
                  type="checkbox"
                  className="size-4 accent-primary"
                  checked={filters.status.includes(value)}
                  onChange={() => toggleRating(value)}
                />
                {label}
              </label>
            ))}
          </div>
        </fieldset>
        <Button onClick={() => onChange(DEFAULT_FILTERS)}>Clear filters</Button>
      </div>
    </section>
  );
}
