import { createColumnHelper, flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";

import { RatingBadge } from "@/components/shared/RatingBadge";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { ThemeChips } from "@/features/themes";
import { cn, formatArr, formatDate } from "@/lib/utils";

import type { AccountRow } from "./types";

const STATUS_TAGS = { new_red: "New red", repeat_red: "Repeat red", new_yellow: "New yellow" } as const;
const SKELETON_ROWS = 5;

const column = createColumnHelper<AccountRow>();

const columns = [
  column.accessor("name", {
    header: "Account",
    cell: ({ row: { original: account } }) => (
      <div className="min-w-64">
        <div className="flex flex-wrap items-center gap-2">
          <span className="font-semibold text-link">{account.name}</span>
          <RatingBadge rating={account.rating} />
          {account.status_tag && <Badge variant="accent">{STATUS_TAGS[account.status_tag]}</Badge>}
        </div>
        <ThemeChips themes={account.themes} />
        {account.top_verbatim && (
          <p className="mt-2 border-l-2 pl-2.5 text-[0.8125rem] text-secondary-foreground">
            &ldquo;{account.top_verbatim.text}&rdquo;
          </p>
        )}
      </div>
    ),
  }),
  column.accessor("arr", {
    header: "ARR",
    meta: { numeric: true },
    cell: (info) => formatArr(info.getValue()),
  }),
  column.accessor("region", {
    header: "Region and segment",
    cell: ({ row: { original: account } }) => (
      <>
        {account.region}
        <div className="text-xs text-muted-foreground">{account.segment}</div>
      </>
    ),
  }),
  column.accessor("cxm", {
    header: "CXM and exec sponsor",
    cell: ({ row: { original: account } }) => (
      <>
        {account.cxm ?? "Not assigned"}
        <div className="text-xs text-muted-foreground">Exec: {account.exec_sponsor ?? "Not assigned"}</div>
      </>
    ),
  }),
  column.accessor("account_executive", {
    header: "Account executive",
    cell: (info) => info.getValue() ?? "Not assigned",
  }),
  column.accessor("next_renewal_date", {
    header: "Next renewal",
    cell: (info) => <span className="tabular-nums">{formatDate(info.getValue())}</span>,
  }),
  column.accessor("rule", {
    header: "Rule or trigger",
    cell: (info) => (
      <Badge>
        <span className="font-bold">{info.getValue().code}</span>
        {info.getValue().text}
      </Badge>
    ),
  }),
  column.accessor("issue_status", { header: "Issue status", cell: (info) => info.getValue() ?? "No flag" }),
  column.accessor("nps", { header: "NPS", cell: (info) => info.getValue()?.category ?? "No data" }),
  column.accessor("explanation", {
    header: "Taxonomy and summary",
    cell: ({ row: { original: account } }) => (
      <div className="min-w-72 text-[0.8125rem]">
        <p className="text-muted-foreground">{account.products.join(", ")}</p>
        <p className="mt-1">{account.explanation ?? "The explanation is not available for this run."}</p>
      </div>
    ),
  }),
];

interface AccountsTableProps {
  accounts: AccountRow[] | undefined;
  total: number;
}

/** ACC-01 to ACC-05: the scorecard table. Server-side filter, sort and paging; no client sorting. */
export function AccountsTable({ accounts, total }: AccountsTableProps) {
  const table = useReactTable({
    data: accounts ?? [],
    columns,
    getCoreRowModel: getCoreRowModel(),
    manualSorting: true,
    manualFiltering: true,
    manualPagination: true,
    getRowId: (account) => account.sfdc_account_id,
  });
  const isNumeric = (meta: unknown) => (meta as { numeric?: boolean } | undefined)?.numeric === true;

  return (
    <>
      <Table>
        <TableHeader>
          {table.getHeaderGroups().map((group) => (
            <TableRow key={group.id}>
              {group.headers.map((header) => (
                <TableHead key={header.id} className={cn(isNumeric(header.column.columnDef.meta) && "text-right")}>
                  {flexRender(header.column.columnDef.header, header.getContext())}
                </TableHead>
              ))}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody>
          {!accounts &&
            Array.from({ length: SKELETON_ROWS }, (_, index) => (
              <TableRow key={index}>
                <TableCell colSpan={columns.length}>
                  <Skeleton className="h-16" />
                </TableCell>
              </TableRow>
            ))}
          {accounts?.length === 0 && (
            <TableRow>
              <TableCell colSpan={columns.length}>No accounts match these filters.</TableCell>
            </TableRow>
          )}
          {table.getRowModel().rows.map((row) => (
            <TableRow key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <TableCell
                  key={cell.id}
                  className={cn(isNumeric(cell.column.columnDef.meta) && "text-right tabular-nums")}
                >
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
      {accounts && (
        <p className="text-[0.8125rem] text-muted-foreground">
          {accounts.length} of {total} {total === 1 ? "account" : "accounts"}
        </p>
      )}
    </>
  );
}
