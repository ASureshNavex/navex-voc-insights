import { Badge } from "@/components/ui/badge";

interface Theme {
  theme_id: string;
  name: string;
  path: string;
}

/** ACC-03: every theme the run ranked for the account, straight from the Enterpret taxonomy. */
export function ThemeChips({ themes }: { themes: Theme[] }) {
  if (themes.length === 0) {
    return <p className="mt-1.5 text-xs text-muted-foreground">No themes this period</p>;
  }
  return (
    <ul className="mt-1.5 flex flex-wrap gap-1.5">
      {themes.map((theme) => (
        <li key={theme.theme_id}>
          <Badge title={theme.path}>{theme.name}</Badge>
        </li>
      ))}
    </ul>
  );
}
