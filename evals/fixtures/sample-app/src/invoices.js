// Invoice rules. Amounts are integer cents.
export const STATUSES = ["draft", "sent", "paid", "void"];

export function invoiceTotal(invoice) {
  return invoice.lines.reduce((sum, line) => sum + line.quantity * line.unitPriceCents, 0);
}

export function changeStatus(invoice, next, actor) {
  if (!STATUSES.includes(next)) throw new Error(`unknown status ${next}`);
  if (invoice.status === "void") throw new Error("void invoices cannot change");
  if (next === "void" && actor.role !== "admin") throw new Error("only admins can void invoices");
  return { ...invoice, status: next };
}

export function listInvoices(invoices, { orgId }) {
  return invoices.filter((invoice) => invoice.orgId === orgId);
}
