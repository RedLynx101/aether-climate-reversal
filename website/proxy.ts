import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

const CANONICAL_HOST = "aetherclimate.com";
const REDIRECT_HOSTS = new Set([
  "aetherclimate.org",
  "www.aetherclimate.org",
  "www.aetherclimate.com",
]);

function requestHostname(request: NextRequest) {
  const forwardedHost = request.headers.get("x-forwarded-host");
  const host = forwardedHost?.split(",")[0] ?? request.headers.get("host") ?? "";

  return host.trim().toLowerCase().split(":")[0];
}

export function proxy(request: NextRequest) {
  if (!REDIRECT_HOSTS.has(requestHostname(request))) {
    return NextResponse.next();
  }

  const destination = request.nextUrl.clone();
  destination.protocol = "https:";
  destination.hostname = CANONICAL_HOST;
  destination.port = "";

  return NextResponse.redirect(destination, 308);
}

export const config = {
  matcher: "/:path*",
};
