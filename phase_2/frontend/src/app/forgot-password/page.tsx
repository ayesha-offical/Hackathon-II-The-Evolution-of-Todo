/**
 * Task: T061 | Spec: @specs/001-sdd-initialization/ui/pages.md §Forgot Password Page
 * Description: Forgot password page with email input for password reset
 * Purpose: Allow users to request password reset email
 * Reference: Constitution II (JWT Bridge), rest-endpoints.md §POST /api/v1/auth/forgot-password
 */

"use client";

import { useState } from "react";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { ROUTES, ERROR_MESSAGES, EMAIL_REGEX } from "@/config/constants";
import { apiPost } from "@/lib/api";

/**
 * Forgot password form validation schema
 */
const forgotPasswordSchema = z.object({
  email: z
    .string()
    .email("Invalid email address")
    .regex(EMAIL_REGEX, "Invalid email format"),
});

type ForgotPasswordFormData = z.infer<typeof forgotPasswordSchema>;

/**
 * Forgot Password page component
 *
 * Features:
 * - Email input for requesting password reset
 * - Real-time validation with react-hook-form
 * - Submit to `/api/v1/auth/forgot-password` endpoint
 * - Display success message after request
 * - Link back to login
 * - Responsive design
 *
 * Reference:
 * - UI spec: @specs/001-sdd-initialization/ui/pages.md §Forgot Password Page
 * - API spec: rest-endpoints.md §POST /api/v1/auth/forgot-password
 */
export default function ForgotPasswordPage() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<ForgotPasswordFormData>({
    resolver: zodResolver(forgotPasswordSchema),
    mode: "onChange",
  });

  /**
   * Handle form submission
   * Request password reset email
   */
  async function onSubmit(data: ForgotPasswordFormData) {
    try {
      setSubmitError(null);
      setIsSubmitting(true);

      const response = await apiPost("/api/v1/auth/forgot-password", {
        email: data.email,
      });

      if (response.ok) {
        // Always show success for security reasons
        setSuccessMessage(
          "If this email exists in our system, you will receive a password reset link shortly."
        );
      }
    } catch (error) {
      console.error("Forgot password failed:", error);
      // For security, always show the same message regardless of whether email exists
      setSuccessMessage(
        "If this email exists in our system, you will receive a password reset link shortly."
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
            Reset your password
          </h2>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Enter your email address and we&apos;ll send you a link to reset your password.
          </p>
        </div>

        {/* Success message */}
        {successMessage && (
          <div className="rounded-md bg-green-50 dark:bg-green-900/20 p-4 border border-green-200 dark:border-green-800">
            <p className="text-sm font-medium text-green-800 dark:text-green-200">
              {successMessage}
            </p>
            <p className="text-xs text-green-700 dark:text-green-300 mt-2">
              Back to{" "}
              <Link
                href={ROUTES.LOGIN}
                className="font-medium text-green-600 dark:text-green-400 hover:underline"
              >
                sign in
              </Link>
            </p>
          </div>
        )}

        {/* Form */}
        {!successMessage && (
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
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300"
              >
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

            {/* Submit button */}
            <button
              type="submit"
              disabled={!isValid || isSubmitting}
              className="btn-primary w-full mt-4"
            >
              {isSubmitting ? "Sending..." : "Send reset link"}
            </button>
          </form>
        )}

        {/* Footer links */}
        {!successMessage && (
          <div className="text-center space-y-2">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Remember your password?{" "}
              <Link
                href={ROUTES.LOGIN}
                className="font-medium text-blue-600 hover:text-blue-500"
              >
                Sign in
              </Link>
            </p>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Don&apos;t have an account?{" "}
              <Link
                href={ROUTES.REGISTER}
                className="font-medium text-blue-600 hover:text-blue-500"
              >
                Sign up
              </Link>
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
