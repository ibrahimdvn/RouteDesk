import type { NextConfig } from "next";

const securityHeaders = [
  // Clickjacking koruması
  { key: "X-Frame-Options", value: "DENY" },
  // MIME sniffing koruması
  { key: "X-Content-Type-Options", value: "nosniff" },
  // XSS filtresi (eski tarayıcılar)
  { key: "X-XSS-Protection", value: "1; mode=block" },
  // Referrer politikası — dışarıya URL sızdırma
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  // Permissions Policy — gereksiz tarayıcı API'larını kapat
  {
    key: "Permissions-Policy",
    value: "camera=(), microphone=(), geolocation=(), payment=()",
  },
  // Content Security Policy
  {
    key: "Content-Security-Policy",
    value: [
      "default-src 'self'",
      "script-src 'self' 'unsafe-inline' 'unsafe-eval'", // Next.js için gerekli
      "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
      "font-src 'self' https://fonts.gstatic.com",
      "img-src 'self' data: blob:",
      "connect-src 'self' https://formspree.io",
      "frame-ancestors 'none'",
    ].join("; "),
  },
  // HTTPS zorunluluğu (production)
  {
    key: "Strict-Transport-Security",
    value: "max-age=63072000; includeSubDomains; preload",
  },
];

const nextConfig: NextConfig = {
  experimental: {
    // @ts-expect-error: Next.js 15 turbopack property might not be in the TS definitions yet
    turbopack: {
      root: __dirname,
    },
  },
  async headers() {
    return [
      {
        source: "/(.*)", // Tüm sayfalara uygula
        headers: securityHeaders,
      },
    ];
  },
  // Sunucu hata mesajlarında stack trace gösterme
  productionBrowserSourceMaps: false,
};

export default nextConfig;
