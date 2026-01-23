/**
 * Task: T060 | Spec: @specs/001-sdd-initialization/ui/pages.md §Registration Page
 * Description: User registration page with form validation and email verification
 * Purpose: Allow new users to create accounts with email and password
 * Reference: Constitution II (JWT Bridge), rest-endpoints.md §POST /api/v1/auth/register
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
import {
  ROUTES,
  ERROR_MESSAGES,
  PASSWORD_REQUIREMENTS,
  EMAIL_REGEX,
} from "@/config/constants";
import { PasswordInput } from "@/components/common/PasswordInput";

/**
 * Registration form validation schema
 * Reference: @specs/001-sdd-initialization/features/authentication.md §FR-001-003
 */
const registerSchema = z
  .object({
    email: z
      .string()
      .email("Invalid email address")
      .regex(EMAIL_REGEX, "Invalid email format"),
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
    terms: z
      .boolean()
      .refine((val) => val === true, "You must accept the terms and conditions"),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: ERROR_MESSAGES.PASSWORDS_DO_NOT_MATCH,
    path: ["confirmPassword"],
  });

type RegisterFormData = z.infer<typeof registerSchema>;

/**
 * Calculate password strength (0-100)
 * Used for strength indicator
 */
function calculatePasswordStrength(password: string): number {
  let strength = 0;

  // Length (0-30 points)
  strength += Math.min(password.length * 3, 30);

  // Has uppercase (10 points)
  if (/[A-Z]/.test(password)) strength += 10;

  // Has lowercase (10 points)
  if (/[a-z]/.test(password)) strength += 10;

  // Has numbers (10 points)
  if (/\d/.test(password)) strength += 10;

  // Has special characters (30 points)
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
 * Registration page component
 *
 * Features:
 * - Email, password, confirm password inputs
 * - Password strength indicator
 * - Real-time validation with react-hook-form
 * - Terms & conditions checkbox (required)
 * - Submit to `/api/v1/auth/register` endpoint
 * - Success message with verification instructions
 * - Auto-redirect to login after 5 seconds
 * - Responsive design
 *
 * Reference:
 * - UI spec: @specs/001-sdd-initialization/ui/pages.md §Registration Page
 * - API spec: rest-endpoints.md §POST /api/v1/auth/register
 * - Auth flow: plan.md Step 4 §Frontend Authentication
 */
export default function RegisterPage() {
  const router = useRouter();
  const { user, isLoading: authLoading } = useAuth();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isValid },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    mode: "onChange",
  });

  const passwordValue = watch("password");

  // Update password strength when password changes
  const strength = calculatePasswordStrength(passwordValue || "");
  const strengthLabel = getPasswordStrengthLabel(strength);

  /**
   * Redirect if already authenticated
   */
  if (!authLoading && user) {
    router.push(ROUTES.DASHBOARD);
    return null;
  }

  /**
   * Handle form submission
   * Call Better Auth signUp method with email and password
   */
  async function onSubmit(data: RegisterFormData) {
    try {
      setSubmitError(null);
      setIsSubmitting(true);

      // Use Better Auth to sign up
      // This sends request to /api/v1/auth/register
      const result = await authClient.signUp.email({
        email: data.email,
        password: data.password,
        name: data.email.split("@")[0], // Use email username as name
      });

      if (result) {
        // Registration successful
        setSuccessMessage(
          "Account created! Please check your email to verify your account. Redirecting to login..."
        );

        // Redirect to login after 5 seconds
        setTimeout(() => {
          router.push(ROUTES.LOGIN);
        }, 5000);
      }
    } catch (error) {
      console.error("Registration failed:", error);

      // Check if error message indicates email already exists
      const errorMessage =
        error instanceof Error ? error.message : "Registration failed";

      if (errorMessage.includes("already")) {
        setSubmitError(ERROR_MESSAGES.EMAIL_ALREADY_REGISTERED);
      } else if (errorMessage.includes("password")) {
        setSubmitError(ERROR_MESSAGES.WEAK_PASSWORD);
      } else {
        setSubmitError(errorMessage);
      }
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
            Create your account
          </h2>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Or{" "}
            <Link
              href={ROUTES.LOGIN}
              className="font-medium text-blue-600 hover:text-blue-500"
            >
              sign in to your existing account
            </Link>
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
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Confirm password
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

            {/* Terms checkbox */}
            <div className="flex items-center">
              <input
                id="terms"
                type="checkbox"
                {...register("terms")}
                className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 dark:bg-gray-800 dark:border-gray-600"
                disabled={isSubmitting}
              />
              <label htmlFor="terms" className="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                I agree to the{" "}
                <a href="#" className="text-blue-600 hover:text-blue-500">
                  Terms & Conditions
                </a>
              </label>
            </div>
            {errors.terms && (
              <p className="text-sm text-red-600 dark:text-red-400">
                {errors.terms.message}
              </p>
            )}

            {/* Submit button */}
            <button
              type="submit"
              disabled={!isValid || isSubmitting}
              className="btn-primary w-full mt-4"
            >
              {isSubmitting ? "Creating account..." : "Sign up"}
            </button>
          </form>
        )}

        {/* Footer links */}
        {!successMessage && (
          <div className="text-center">
            <p className="text-xs text-gray-500 dark:text-gray-500">
              By creating an account, you agree to our Terms & Conditions and
              Privacy Policy
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
