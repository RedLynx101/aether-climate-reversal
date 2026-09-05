import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { request as httpRequest } from "node:http";
import { fileURLToPath } from "node:url";
import test from "node:test";

const projectDirectory = fileURLToPath(new URL("..", import.meta.url));
const nextBinary = fileURLToPath(
  new URL("../node_modules/next/dist/bin/next", import.meta.url),
);
const port = 32_000 + (process.pid % 1_000);

let server;
let serverOutput = "";

function requestSite(pathname, hostname = "aetherclimate.com") {
  return new Promise((resolve, reject) => {
    const request = httpRequest(
      {
        hostname: "127.0.0.1",
        port,
        path: pathname,
        method: "GET",
        headers: { host: hostname },
      },
      (response) => {
        const chunks = [];
        response.on("data", (chunk) => chunks.push(chunk));
        response.on("end", () => {
          resolve({
            body: Buffer.concat(chunks),
            headers: response.headers,
            status: response.statusCode,
          });
        });
      },
    );

    request.on("error", reject);
    request.end();
  });
}

async function waitForServer() {
  const deadline = Date.now() + 30_000;

  while (Date.now() < deadline) {
    if (server.exitCode !== null) {
      throw new Error(`Next.js exited before it was ready.\n${serverOutput}`);
    }

    try {
      const response = await requestSite("/");
      if (response.status === 200) return;
    } catch {
      // The listener is not ready yet.
    }

    await new Promise((resolve) => setTimeout(resolve, 200));
  }

  throw new Error(`Timed out waiting for Next.js.\n${serverOutput}`);
}

test.before(async () => {
  server = spawn(
    process.execPath,
    [nextBinary, "start", "--hostname", "127.0.0.1", "--port", String(port)],
    {
      cwd: projectDirectory,
      env: { ...process.env, NODE_ENV: "production" },
      stdio: ["ignore", "pipe", "pipe"],
    },
  );

  for (const stream of [server.stdout, server.stderr]) {
    stream.setEncoding("utf8");
    stream.on("data", (chunk) => {
      serverOutput += chunk;
    });
  }

  await waitForServer();
});

test.after(() => {
  if (server && server.exitCode === null) server.kill();
});

test("serves the Vercel production story and canonical redirect", async () => {
  const routes = [
    ["/", "The atmosphere is shared"],
    ["/evidence", "Show the system"],
  ];

  for (const [pathname, expectedCopy] of routes) {
    const response = await requestSite(pathname);
    const html = response.body.toString("utf8");
    assert.equal(response.status, 200, pathname);
    assert.match(response.headers["content-type"] ?? "", /^text\/html\b/i);
    assert.match(html, new RegExp(expectedCopy, "i"));
    assert.match(html, /AETHER/);
  }

  // Corrections and unresolved scientific boundaries must remain visible.
  const evidence = await requestSite("/evidence");
  const evidenceHtml = evidence.body.toString("utf8");
  for (const expected of ["Absolute climate projections", "quarantined", "NOT A PROBABILITY", "NOT FULLY COUPLED", "758.7", "803.3"]) {
    assert.match(evidenceHtml, new RegExp(expected, "i"), expected);
  }

  // Paths that were public before the restructure keep resolving.
  for (const [pathname, destination] of [
    ["/model", "/evidence"],
    ["/living-atmosphere", "/"],
    ["/papers/AETHER_v0.45_working_paper.pdf", "/papers/AETHER_v0.46_working_paper.pdf"],
    ["/papers/AETHER_Conditional_Feasibility_Proposal.pdf", "/papers/AETHER_v0.46_working_paper.pdf"],
  ]) {
    const response = await requestSite(pathname);
    assert.equal(response.status, 308, pathname);
    assert.equal(response.headers.location, destination, pathname);
  }

  for (const pathname of ["/planetary-os", "/carbon-foundry", "/civic-moonshot"]) {
    const response = await requestSite(pathname);
    assert.equal(response.status, 404, pathname);
  }

  const paper = await requestSite("/papers/AETHER_v0.46_working_paper.pdf");
  assert.equal(paper.status, 200);
  assert.match(paper.headers["content-type"] ?? "", /^application\/pdf\b/i);
  assert.equal(paper.body.subarray(0, 5).toString(), "%PDF-");
  assert.ok(paper.body.length > 100_000, "current paper includes embedded fonts and figures");
  const supplement = await requestSite("/papers/AETHER_v0.46_technical_supplement.pdf");
  assert.equal(supplement.status, 200);
  assert.equal(supplement.body.subarray(0, 5).toString(), "%PDF-");

  for (const pathname of [
    "/charts/regional-carbon-ledger.png",
    "/charts/regional-resource-limits.png",
    "/charts/regional-funding-ledger.png",
  ]) {
    const chart = await requestSite(pathname);
    assert.equal(chart.status, 200, pathname);
    assert.match(chart.headers["content-type"] ?? "", /^image\/png\b/i);
    assert.ok(chart.body.length > 50_000, `${pathname} should not be empty`);
  }

  const redirect = await requestSite("/evidence?source=org", "aetherclimate.org");
  assert.equal(redirect.status, 308);
  assert.equal(
    redirect.headers.location,
    "https://aetherclimate.com/evidence?source=org",
  );

  const wwwRedirect = await requestSite("/evidence?source=www", "www.aetherclimate.com");
  assert.equal(wwwRedirect.status, 308);
  assert.equal(
    wwwRedirect.headers.location,
    "https://aetherclimate.com/evidence?source=www",
  );
});
