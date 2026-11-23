import { Skeleton } from "@/components/ui/skeleton";
import { cn, formatArr } from "@/lib/utils";

import type { AccountRef, PortfolioSummary, RatingCard } from "./types";

function AccountList({ title, accounts, empty }: { title: string; accounts: AccountRef[]; empty: string }) {
  return (
    <div className="mt-3 border-t pt-2.5">
      <h3 className="text-[0.8125rem] font-semibold text-secondary-foreground">
        {title}: {accounts.length}
      </h3>
      {accounts.length === 0 ? (
        <p className="mt-1 text-[0.8125rem] text-muted-foreground">{empty}</p>
      ) : (
        <ul className="mt-1 max-h-40 overflow-auto text-sm">
          {accounts.map((account) => (
            <li key={account.sfdc_account_id} className="flex justify-between gap-3 py-1">
              <span className="font-semibold text-link">{account.name}</span>
              <span className="text-muted-foreground tabular-nums">{formatArr(account.arr)}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function Card({ tone, card, noRepeat }: { tone: "red" | "yellow"; card: RatingCard; noRepeat?: boolean }) {
  const label = tone === "red" ? "Red" : "Yellow";
  return (
    <section className={cn("panel p-5", tone === "red" ? "panel--red" : "panel--yellow")} aria-label={`${label} accounts`}>
      <div className="flex items-baseline justify-between gap-2">
        <h2 className="text-[0.9375rem] font-semibold">{label} accounts</h2>
        <span className="text-xs text-muted-foreground">
          {card.count} {card.count === 1 ? "account" : "accounts"}
        </span>
      </div>
      <p className="mt-2 text-[2.125rem] leading-none font-semibold tracking-tight tabular-nums">{formatArr(card.arr)}</p>
      <p className="mt-1 text-xs text-muted-foreground">ARR in {label.toLowerCase()} accounts</p>
      <AccountList
        title={`New ${label.toLowerCase()} this week`}
        accounts={card.new_this_week}
        empty={`No new ${label.toLowerCase()} accounts this week.`}
      />
      {!noRepeat && <AccountList title="Repeat red" accounts={card.repeat} empty="No repeat red accounts." />}
    </section>
  );
}

/** SCR-04 and SCR-05: red and yellow cards with this week's new and repeat accounts. */
export function RatingCards({ summary }: { summary: PortfolioSummary | undefined }) {
  if (!summary) {
    return (
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Skeleton className="h-56" />
        <Skeleton className="h-56" />
      </div>
    );
  }
  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
      <Card tone="red" card={summary.red} />
      <Card tone="yellow" card={summary.yellow} noRepeat />
    </div>
  );
}
