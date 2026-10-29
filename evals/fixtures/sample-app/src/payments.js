// Payment provider client. The key is read from the environment; no sandbox
// account is configured for this repository yet.
const apiKey = process.env.PAYMENT_API_KEY;

export async function chargeInvoice(invoice) {
  if (!apiKey) throw new Error("PAYMENT_API_KEY is not configured");
  throw new Error("payment provider integration not implemented");
}
