import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

import { classNames } from "@/utils/classNames";

const inter = Inter({ subsets: ["latin"] });

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
      <body className={classNames(inter.className, "h-screen max-h-screen")}>
        {children}
      </body>
    </html>
  );
}
