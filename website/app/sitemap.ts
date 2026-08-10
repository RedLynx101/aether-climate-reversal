import type { MetadataRoute } from "next";

export default function sitemap(): MetadataRoute.Sitemap {
  const base = "https://aetherclimate.com";
  return [
    { url: base, changeFrequency: "monthly", priority: 1 },
    { url: `${base}/model`, changeFrequency: "monthly", priority: 0.8 },
  ];
}
