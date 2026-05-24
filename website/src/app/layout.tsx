import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "RouteDesk | Terminal Operasyon Yönetim Sistemi",
  description: "Modern terminal operasyon yazılımı. RouteDesk, seyahat ofislerinin seferlerini, bilet satışlarını, rezervasyonlarını ve özel koltuk planlarını yönetmesine yardımcı olur.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="tr" className="scroll-smooth">
      <body className={`${inter.variable} font-inter bg-background text-primary antialiased`}>
        {children}
      </body>
    </html>
  );
}
