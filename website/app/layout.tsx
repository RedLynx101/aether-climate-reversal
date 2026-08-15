import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://aetherclimate.com"),
  title: {
    default: "AETHER — Climate recovery as public infrastructure",
    template: "%s — AETHER",
  },
  description:
    "A public research program testing whether autonomous systems, clean power, and durable carbon removal could make atmospheric recovery an inspectable public capability.",
  alternates: { canonical: "/" },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
  openGraph: {
    title: "AETHER",
    description:
      "What if climate recovery became an inspectable public capability?",
    url: "https://aetherclimate.com",
    siteName: "AETHER",
    images: [{ url: "/art/aether-social.jpg", width: 1536, height: 804 }],
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "AETHER",
    description: "Climate recovery as public infrastructure.",
    images: ["/art/aether-social.jpg"],
  },
};

export const viewport: Viewport = {
  colorScheme: "light dark",
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#f4f3e9" },
    { media: "(prefers-color-scheme: dark)", color: "#0d1a17" },
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <a className="skip-link" href="#main">Skip to content</a>
        {children}
      </body>
    </html>
  );
}
