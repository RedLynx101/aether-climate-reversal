import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async redirects() {
    // Both paths were public before the evidence-led restructure, so they keep
    // working rather than 404ing anything already linked or indexed.
    return [
      { source: "/model", destination: "/evidence", permanent: true },
      { source: "/living-atmosphere", destination: "/", permanent: true },
      { source: "/papers/AETHER_v0.45_working_paper.pdf", destination: "/papers/AETHER_v0.46_working_paper.pdf", permanent: true },
      { source: "/papers/AETHER_Conditional_Feasibility_Proposal.pdf", destination: "/papers/AETHER_v0.46_working_paper.pdf", permanent: true },
    ];
  },
};

export default nextConfig;
