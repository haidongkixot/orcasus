import http from "node:http";
import { listInvoices, invoiceTotal } from "./invoices.js";

const invoices = [];

const server = http.createServer((req, res) => {
  const url = new URL(req.url, "http://localhost");
  if (req.method === "GET" && url.pathname === "/invoices") {
    const orgId = req.headers["x-org-id"];
    if (!orgId) {
      res.writeHead(401).end();
      return;
    }
    const rows = listInvoices(invoices, { orgId }).map((i) => ({ ...i, totalCents: invoiceTotal(i) }));
    res.writeHead(200, { "content-type": "application/json" }).end(JSON.stringify(rows));
    return;
  }
  res.writeHead(404).end();
});

if (process.argv[1] && process.argv[1].endsWith("server.js")) {
  server.listen(process.env.PORT || 3000);
}

export default server;
