/**
 * Task: UPDATE (T065) | Spec: plan.md Step 5 §frontend/src/app/layout.tsx
 * Description: Root layout with AuthProvider wrapper
 * Purpose: Make authentication context available to entire application
 * Reference: Constitution II (JWT Bridge), Constitution VI (App Structure)
 */

import type { Metadata } from "next";
import "./globals.css";
import { RootProvider } from "@/components/RootProvider";

export const metadata: Metadata = {
  title: "Phase 2 Todo App",
  description: "Full-stack todo application with JWT authentication",
  keywords: ["todo", "task management", "productivity"],
  authors: [{ name: "Phase 2 Development Team" }],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className="bg-white text-gray-900 dark:bg-gray-900 dark:text-white">
        <RootProvider>{children}</RootProvider>
      </body>
    </html>
  );
}
