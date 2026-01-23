/**
 * Task: T059 | Spec: @specs/001-sdd-initialization/ui/pages.md §Login Page
 * Description: User login page with form validation
 * Purpose: Allow registered users to authenticate and receive JWT tokens
 * Reference: Constitution II (JWT Bridge), rest-endpoints.md §POST /api/v1/auth/login
 */

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import Link from "next/link";
import { authClient } from "@/lib/auth";
import { useAuth } from "@/contexts/AuthContext";
import { ROUTES, ERROR_MESSAGES, EMAIL_REGEX } from "@/config/constants";
import { PasswordInput } from "@/components/common/PasswordInput";

/**
 * Login form validation schema
 * Reference: @specs/001-sdd-initialization/features/authentication.md §FR-005
 */
const loginSchema = z.object({
  email: z
    .string()
    .email("Invalid email address")
    .regex(EMAIL_REGEX, "Invalid email format"),
  password: z
    .string()
    .min(1, "Password is required"),
});

type LoginFormData = z.infer<typeof loginSchema>;

/**
 * Login page component
 *
 * Features:
 * - Email and password inputs with validation
 * - Real-time validation with react-hook-form
 * - Submit to `/api/v1/auth/login` endpoint
 * - Display error messages for invalid credentials
 * - Redirect to dashboard on successful login
 * - Show links to registration and password reset
 * - Responsive design (mobile to desktop)
 *
 * Reference:
 * - UI spec: @specs/001-sdd-initialization/ui/pages.md §Login Page
 * - API spec: rest-endpoints.md §POST /api/v1/auth/login
 * - Auth flow: plan.md Step 4 §Frontend Authentication
 */
export default function LoginPage() {
  const router = useRouter();
  const { user, isLoading: authLoading } = useAuth();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    mode: "onChange",
  });

  /**
   * Redirect if already authenticated
   */
  if (!authLoading && user) {
    router.push(ROUTES.DASHBOARD);
    return null;
  }

  /**
   * Handle form submission
   * Call Better Auth signIn method with email and password
   */
  async function onSubmit(data: LoginFormData) {
    try {
      setSubmitError(null);
      setIsSubmitting(true);

      // Use Better Auth to sign in
      // This sends request to /api/v1/auth/login and stores JWT in HTTP-only cookie
      const result = await authClient.signIn.email({
        email: data.email,
        password: data.password,
      });

      if (result && ((result as any)?.user || (result as any)?.data?.user)) {
        // Login successful, redirect to dashboard
        router.push(ROUTES.DASHBOARD);
      } else {
        setSubmitError(ERROR_MESSAGES.INVALID_CREDENTIALS);
      }
    } catch (error) {
      console.error("Login failed:", error);
      setSubmitError(
        error instanceof Error ? error.message : ERROR_MESSAGES.INVALID_CREDENTIALS
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Phase 2 Todo App
          </h1>
          <h2 className="mt-6 text-2xl font-bold text-gray-900 dark:text-white">
            Sign in to your account
          </h2>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Or{" "}
            <Link
              href={ROUTES.REGISTER}
              className="font-medium text-blue-600 hover:text-blue-500"
            >
              create a new account
            </Link>
          </p>
        </div>

        {/* Form */}
        <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
          {/* Error alert */}
          {submitError && (
            <div className="rounded-md bg-red-50 dark:bg-red-900/20 p-4 border border-red-200 dark:border-red-800">
              <p className="text-sm font-medium text-red-800 dark:text-red-200">
                {submitError}
              </p>
            </div>
          )}

          {/* Email field */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Email address
            </label>
            <input
              id="email"
              type="email"
              placeholder="you@example.com"
              {...register("email")}
              className="input mt-1"
              disabled={isSubmitting}
            />
            {errors.email && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.email.message}
              </p>
            )}
          </div>

          {/* Password field */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Password
            </label>
            <PasswordInput
              id="password"
              placeholder="••••••••"
              disabled={isSubmitting}
              {...register("password")}
              className="mt-1"
            />
            {errors.password && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.password.message}
              </p>
            )}
          </div>

          {/* Submit button */}
          <button
            type="submit"
            disabled={!isValid || isSubmitting}
            className="btn-primary w-full mt-4"
          >
            {isSubmitting ? "Signing in..." : "Sign in"}
          </button>
        </form>

        {/* Footer links */}
        <div className="text-center space-y-2">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Forgot your password?{" "}
            <Link
              href={ROUTES.FORGOT_PASSWORD}
              className="font-medium text-blue-600 hover:text-blue-500"
            >
              Reset it here
            </Link>
          </p>
          <p className="text-xs text-gray-500 dark:text-gray-500">
            By signing in, you agree to our Terms & Conditions
          </p>
        </div>
      </div>
    </div>
  );
}
