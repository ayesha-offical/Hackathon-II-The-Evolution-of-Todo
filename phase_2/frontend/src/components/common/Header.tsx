/**
 * Task: T066 | Spec: @specs/001-sdd-initialization/ui/pages.md §Shared Components
 * Description: Navigation header with user menu and logout
 * Purpose: Display app branding, user info, and authentication actions
 * Reference: Constitution II (JWT Bridge), Constitution VI (UI Components)
 */

"use client";

import Link from "next/link";
import { useAuth } from "@/contexts/AuthContext";
import { ROUTES } from "@/config/constants";

/**
 * Header component
 *
 * Features:
 * - App logo/name (clickable link to dashboard or home)
 * - User email display when authenticated
 * - Logout button for authenticated users
 * - Login/Sign up links for unauthenticated users
 * - Responsive design with dark mode support
 *
 * Reference:
 * - UI spec: @specs/001-sdd-initialization/ui/pages.md §Shared Components
 * - Used on all pages to provide navigation
 */
export function Header() {
  const { user, isLoading, logout } = useAuth();

  return (
    <header className="sticky top-0 z-50 border-b bg-white shadow-sm dark:border-gray-700 dark:bg-gray-800">
      <div className="container mx-auto px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          {/* Logo/Brand */}
          <Link
            href={user ? ROUTES.DASHBOARD : ROUTES.HOME}
            className="flex items-center gap-2"
          >
            <span className="text-xl font-bold text-gray-900 dark:text-white">
              📝 Phase 2 Todo
            </span>
          </Link>

          {/* Navigation */}
          <nav className="flex items-center gap-4">
            {isLoading ? (
              <div className="h-8 w-20 animate-pulse bg-gray-200 dark:bg-gray-700 rounded" />
            ) : user ? (
              <>
                {/* User email */}
                <div className="hidden sm:block">
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {user.email}
                  </span>
                </div>

                {/* Logout button */}
                <button
                  onClick={logout}
                  className="btn-secondary inline-flex items-center gap-2 px-3 py-2 text-sm"
                >
                  <span>Logout</span>
                </button>
              </>
            ) : (
              <>
                {/* Login link */}
                <Link href={ROUTES.LOGIN} className="btn-secondary text-sm">
                  Sign In
                </Link>

                {/* Register link */}
                <Link href={ROUTES.REGISTER} className="btn-primary text-sm">
                  Sign Up
                </Link>
              </>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
}
