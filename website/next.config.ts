import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async redirects() {
    // Both paths were public before the evidence-led restructure, so they keep
    // working rather than 404ing anything already linked or indexed.
    return [
      { source: "/model", destination: "/evidence", permanent: true },
      { source: "/living-atmosphere", destination: "/", permanent: true },
    ];
  },
};

export default nextConfig;
