/**
 * Task: T057 | Spec: plan.md Step 4 §contexts/AuthContext.tsx
 * Description: AuthContext provider for session state management
 * Purpose: Manage authenticated user state across entire application
 * Reference: Constitution II (JWT Bridge), Constitution VI (Context State)
 */

"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { authClient } from "@/lib/auth";
import type { User, AuthContextType, BetterAuthSessionResponse } from "@/types/auth";

/**
 * AuthContext for storing authentication state
 * Available to all components wrapped in AuthProvider
 */
const AuthContext = createContext<AuthContextType | undefined>(undefined);

/**
 * AuthProvider component
 *
 * Responsibilities:
 * 1. Check session on mount using Better Auth
 * 2. Set user state if logged in
 * 3. Handle loading and error states
 * 4. Provide user state to all children
 *
 * Usage:
 * ```tsx
 * <AuthProvider>
 *   <App />
 * </AuthProvider>
 * ```
 *
 * Then use `const { user, isLoading } = useAuth()` in child components
 *
 * Reference: Constitution II - User identity comes from JWT session
 */
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Check session on component mount
   * This verifies if user is already logged in (from HTTP-only cookie)
   */
  useEffect(() => {
    checkSession();
  }, []);

  /**
   * Verify current session status
   * Called on mount and can be called manually to refresh
   */
  async function checkSession() {
    try {
      const sessionData = (await authClient.getSession()) as unknown as BetterAuthSessionResponse;
      const session = sessionData?.data || sessionData;

      if (session?.user) {
        // User is authenticated
        setUser(session.user as User);
        setIsError(false);
        setError(null);
      } else {
        // User is not authenticated
        setUser(null);
      }
    } catch (err) {
      // Session check failed (network error, etc.)
      setIsError(true);
      setError(err instanceof Error ? err.message : "Session check failed");
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }

  /**
   * Context value provided to children
   * Reference: @specs/001-sdd-initialization/types/auth.ts §AuthContextType
   */
  const value: AuthContextType = {
    user,
    isLoading,
    isError,
    error,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

/**
 * Hook to consume AuthContext
 *
 * Usage in components:
 * ```tsx
 * "use client";
 * import { useAuth } from "@/contexts/AuthContext";
 *
 * export function MyComponent() {
 *   const { user, isLoading } = useAuth();
 *
 *   if (isLoading) return <div>Loading...</div>;
 *   if (!user) return <div>Not authenticated</div>;
 *
 *   return <div>Welcome {user.email}</div>;
 * }
 * ```
 *
 * @throws Error if used outside of AuthProvider
 * @returns AuthContextType with user, loading, error state
 */
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  return context;
}
