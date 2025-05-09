import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

export const metadata: Metadata = {
  title: "App Analytics",
  description: "App Store Dashboard Analytics",
};

import "./globals.css"
import { AppHeader } from "../components/ui/app-header"

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AppHeader />
        <main className="container mx-auto py-6 px-4">{children}</main>
      </body>
    </html>
  )
}
