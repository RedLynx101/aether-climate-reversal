import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: "*", allow: "/" },
    sitemap: "https://aetherclimate.com/sitemap.xml",
    host: "https://aetherclimate.com",
  };
}
