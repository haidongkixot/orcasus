import { test } from "node:test";
import assert from "node:assert/strict";
import { invoiceTotal, changeStatus, listInvoices } from "../src/invoices.js";

const invoice = { id: "inv-1", orgId: "org-a", status: "draft", lines: [{ quantity: 2, unitPriceCents: 1500 }] };

test("total sums line amounts", () => {
  assert.equal(invoiceTotal(invoice), 3000);
});

test("only admins can void", () => {
  assert.throws(() => changeStatus(invoice, "void", { role: "member" }));
  assert.equal(changeStatus(invoice, "void", { role: "admin" }).status, "void");
});

test("list is scoped to the caller's org", () => {
  const rows = listInvoices([invoice, { ...invoice, id: "inv-2", orgId: "org-b" }], { orgId: "org-a" });
  assert.deepEqual(rows.map((r) => r.id), ["inv-1"]);
});
