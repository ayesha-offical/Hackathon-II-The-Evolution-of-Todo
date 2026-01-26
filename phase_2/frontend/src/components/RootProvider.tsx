/**
 * Task: T065 | Spec: plan.md Step 5 §frontend/RootProvider.tsx
 * Description: Client-side root provider wrapper for layout
 * Purpose: Isolate client-side providers from server layout to prevent chunk load errors
 * Reference: Constitution II (JWT Bridge), Constitution VI (App Structure)
 */

"use client";

import React from "react";
import { AuthProvider } from "@/contexts/AuthContext";
import { Header } from "@/components/common/Header";

export function RootProvider({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <Header />
      {children}
    </AuthProvider>
  );
}
