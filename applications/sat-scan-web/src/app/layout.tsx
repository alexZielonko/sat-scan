import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Sat Scan",
  description: "Sat Scan Web Application",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-screen max-h-screen bg-gray-100">
      <body className="h-screen max-h-screen">{children}</body>
    </html>
  );
}
