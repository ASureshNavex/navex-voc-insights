import { render, screen } from "@testing-library/react";
import type { ReactNode } from "react";

import { EntitlementContext, type Entitlements, type Permission } from "@/features/auth";

import { Can } from "./Can";

function entitlements(permissions: Permission[]): Entitlements {
  return {
    upn: "lindsay@navex.com",
    name: "Lindsay",
    role: "CXM",
    dataScope: "OWN_BOOK",
    permissions: new Set(permissions),
    scopeSize: 3,
  };
}

function renderWith(permissions: Permission[], ui: ReactNode) {
  return render(
    <EntitlementContext.Provider value={entitlements(permissions)}>{ui}</EntitlementContext.Provider>,
  );
}

describe("Can", () => {
  it("shows its children when the user holds the permission", () => {
    renderWith(["scorecard:export"], <Can perform="scorecard:export">Download Excel</Can>);
    expect(screen.getByText("Download Excel")).toBeInTheDocument();
  });

  it("hides its children and shows the fallback without the permission", () => {
    renderWith(
      ["scorecard:read"],
      <Can perform="knowledge_hub:upload" fallback="Not available">
        New upload
      </Can>,
    );
    expect(screen.queryByText("New upload")).not.toBeInTheDocument();
    expect(screen.getByText("Not available")).toBeInTheDocument();
  });
});
