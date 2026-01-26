/**
 * Task: T062 | Spec: @specs/001-sdd-initialization/ui/pages.md §Reset Password Page
 * Description: Reset password page with new password form
 * Purpose: Allow users to reset their password using a reset token
 * Reference: Constitution II (JWT Bridge), rest-endpoints.md §POST /api/v1/auth/reset-password
 */

"use client";

import { useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import Link from "next/link";
import { ROUTES, ERROR_MESSAGES, PASSWORD_REQUIREMENTS } from "@/config/constants";
import { PasswordInput } from "@/components/common/PasswordInput";
import { apiPost } from "@/lib/api";

/**
 * Reset password form validation schema
 */
const resetPasswordSchema = z
  .object({
    password: z
      .string()
      .min(
        PASSWORD_REQUIREMENTS.MIN_LENGTH,
        `Password must be at least ${PASSWORD_REQUIREMENTS.MIN_LENGTH} characters`
      )
      .regex(
        PASSWORD_REQUIREMENTS.REGEX,
        "Password must include uppercase letter, lowercase letter, and number"
      ),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: ERROR_MESSAGES.PASSWORDS_DO_NOT_MATCH,
    path: ["confirmPassword"],
  });

type ResetPasswordFormData = z.infer<typeof resetPasswordSchema>;

/**
 * Calculate password strength (0-100)
 */
function calculatePasswordStrength(password: string): number {
  let strength = 0;
  strength += Math.min(password.length * 3, 30);
  if (/[A-Z]/.test(password)) strength += 10;
  if (/[a-z]/.test(password)) strength += 10;
  if (/\d/.test(password)) strength += 10;
  if (/[@$!%*?&]/.test(password)) strength += 30;
  return Math.min(strength, 100);
}

/**
 * Get password strength label and color
 */
function getPasswordStrengthLabel(
  strength: number
): { label: string; color: string } {
  if (strength < 20) return { label: "Very Weak", color: "bg-red-500" };
  if (strength < 40) return { label: "Weak", color: "bg-orange-500" };
  if (strength < 60) return { label: "Fair", color: "bg-yellow-500" };
  if (strength < 80) return { label: "Good", color: "bg-green-500" };
  return { label: "Strong", color: "bg-green-600" };
}

/**
 * Reset Password page component
 *
 * Features:
 * - Password and confirm password inputs
 * - Password strength indicator
 * - Real-time validation with react-hook-form
 * - Submit to `/api/v1/auth/reset-password` endpoint
 * - Redirect to login after successful reset
 * - Responsive design
 *
 * Reference:
 * - UI spec: @specs/001-sdd-initialization/ui/pages.md §Reset Password Page
 * - API spec: rest-endpoints.md §POST /api/v1/auth/reset-password
 */
export default function ResetPasswordPage() {
  const router = useRouter();
  const params = useParams();
  const token = params.token as string;

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isValid },
  } = useForm<ResetPasswordFormData>({
    resolver: zodResolver(resetPasswordSchema),
    mode: "onChange",
  });

  const passwordValue = watch("password");
  const strength = calculatePasswordStrength(passwordValue || "");
  const strengthLabel = getPasswordStrengthLabel(strength);

  /**
   * Handle form submission
   * Reset password using token
   */
  async function onSubmit(data: ResetPasswordFormData) {
    try {
      setSubmitError(null);
      setIsSubmitting(true);

      const response = await apiPost("/api/v1/auth/reset-password", {
        reset_token: token,
        new_password: data.password,
      });

      if (response.ok) {
        setSuccessMessage(
          "Password reset successfully! Redirecting to login..."
        );
        setTimeout(() => {
          router.push(ROUTES.LOGIN);
        }, 3000);
      }
    } catch (error) {
      console.error("Password reset failed:", error);
      setSubmitError(
        error instanceof Error ? error.message : "Password reset failed"
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
            Set new password
          </h2>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Enter your new password below.
          </p>
        </div>

        {/* Success message */}
        {successMessage && (
          <div className="rounded-md bg-green-50 dark:bg-green-900/20 p-4 border border-green-200 dark:border-green-800">
            <p className="text-sm font-medium text-green-800 dark:text-green-200">
              {successMessage}
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

            {/* Password field */}
            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300"
              >
                New Password
              </label>
              <PasswordInput
                id="password"
                placeholder="••••••••"
                disabled={isSubmitting}
                {...register("password")}
                className="mt-1"
              />

              {/* Password strength indicator */}
              {passwordValue && (
                <div className="mt-2">
                  <div className="flex items-center justify-between text-xs text-gray-600 dark:text-gray-400 mb-1">
                    <span>Password strength:</span>
                    <span className={strengthLabel.color.replace("bg-", "text-")}>
                      {strengthLabel.label}
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div
                      className={`${strengthLabel.color} h-2 rounded-full transition-all`}
                      style={{ width: `${strength}%` }}
                    />
                  </div>
                </div>
              )}

              {errors.password && (
                <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                  {errors.password.message}
                </p>
              )}
            </div>

            {/* Confirm password field */}
            <div>
              <label
                htmlFor="confirmPassword"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300"
              >
                Confirm Password
              </label>
              <PasswordInput
                id="confirmPassword"
                placeholder="••••••••"
                disabled={isSubmitting}
                {...register("confirmPassword")}
                className="mt-1"
              />
              {errors.confirmPassword && (
                <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                  {errors.confirmPassword.message}
                </p>
              )}
            </div>

            {/* Submit button */}
            <button
              type="submit"
              disabled={!isValid || isSubmitting}
              className="btn-primary w-full mt-4"
            >
              {isSubmitting ? "Resetting..." : "Reset password"}
            </button>
          </form>
        )}

        {/* Footer links */}
        {!successMessage && (
          <div className="text-center">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Remember your password?{" "}
              <Link
                href={ROUTES.LOGIN}
                className="font-medium text-blue-600 hover:text-blue-500"
              >
                Sign in
              </Link>
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
