/**
 * Task: T075 | Spec: @specs/001-sdd-initialization/ui/pages.md §Design System
 * Description: Tailwind CSS configuration with violet theme and custom utilities
 * Purpose: Centralize design system tokens (colors, typography, spacing, components)
 * Reference: plan.md Step 5, Constitution VI (Code Quality)
 */

import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      /**
       * Typography System
       * Configured with Inter and Geist fonts with system fallback
       * Reference: ui/pages.md §Typography
       */
      fontFamily: {
        sans: [
          "var(--font-inter)",
          "var(--font-geist-sans)",
          "system-ui",
          "ui-sans-serif",
          "sans-serif",
        ],
        mono: [
          "var(--font-geist-mono)",
          "system-ui",
          "ui-monospace",
          "monospace",
        ],
      },

      /**
       * Color Palette System
       * Primary: Violet/Indigo (#7c3aed) instead of blue
       * Alerts: Soft green (success), soft red (error)
       * Reference: ui/pages.md §Design System, video requirements
       */
      colors: {
        /**
         * Primary Color: Violet/Indigo Theme
         * Used for buttons, links, active states
         * Main color: #7c3aed (primary-700)
         */
        primary: {
          50: "#faf5ff",
          100: "#f3e8ff",
          200: "#e9d5ff",
          300: "#d8b4fe",
          400: "#c084fc",
          500: "#a855f7",
          600: "#9333ea",
          700: "#7c3aed", // Main violet
          800: "#6b21a8",
          900: "#581c87",
          950: "#3b0764",
        },

        /**
         * Secondary Color: Green
         * Used for success states, positive actions
         */
        success: {
          50: "#f0fdf4",
          100: "#dcfce7",
          200: "#bbf7d0",
          500: "#22c55e", // Soft green
          600: "#16a34a",
        },

        /**
         * Warning Color: Orange
         * Used for warning states, alerts
         */
        warning: {
          50: "#fffbeb",
          100: "#fef3c7",
          500: "#f59e0b",
          600: "#d97706",
        },

        /**
         * Error Color: Red
         * Used for error states, destructive actions
         */
        error: {
          50: "#fef2f2",
          100: "#fee2e2",
          500: "#ef4444", // Soft red
          600: "#dc2626",
        },

        /**
         * Neutral Colors
         * Background and border colors
         * Reference: ui/pages.md §Design System
         */
        background: {
          DEFAULT: "#ffffff",
          secondary: "#f9fafb", // Light gray background
        },
        border: {
          light: "#f3f4f6", // Light gray borders
          DEFAULT: "#e5e7eb", // Medium gray borders
        },
      },

      /**
       * Border Radius System
       * Custom xl (12px) for cards and buttons
       * Reference: ui/pages.md §Spacing, video requirements
       */
      borderRadius: {
        xs: "4px",
        sm: "6px",
        DEFAULT: "8px",
        md: "12px",
        lg: "14px",
        xl: "12px", // Custom size for cards/buttons as per video
        "2xl": "16px",
        "3xl": "24px",
        full: "9999px",
      },

      /**
       * Spacing System
       * Base unit: 8px
       * Reference: ui/pages.md §Spacing
       */
      spacing: {
        px: "1px",
        0.5: "2px",
        1: "4px",
        1.5: "6px",
        2: "8px",
        2.5: "10px",
        3: "12px",
        3.5: "14px",
        4: "16px",
        5: "20px",
        6: "24px",
        7: "28px",
        8: "32px",
        9: "36px",
        10: "40px",
        12: "48px",
        14: "56px",
        16: "64px",
        20: "80px",
        24: "96px",
        28: "112px",
        32: "128px",
        36: "144px",
        40: "160px",
        44: "176px",
        48: "192px",
        52: "208px",
        56: "224px",
        60: "240px",
        64: "256px",
        72: "288px",
        80: "320px",
        96: "384px",
      },

      /**
       * Shadow System
       * Subtle shadows for depth
       */
      boxShadow: {
        xs: "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        sm: "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
        DEFAULT:
          "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        md: "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
        lg: "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
        xl: "0 25px 50px -12px rgba(0, 0, 0, 0.15)",
      },

      /**
       * Backdrop Blur Effects
       * For navigation/header with subtle blur effect
       * Reference: video requirements
       */
      backdropBlur: {
        sm: "4px",
        DEFAULT: "8px",
        md: "12px",
        lg: "16px",
        xl: "20px",
      },

      /**
       * Responsive Breakpoints
       * Mobile: <640px (sm), Tablet: 640px-1024px, Desktop: >1024px
       * Reference: ui/pages.md §Responsive Breakpoints
       */
      screens: {
        xs: "375px",
        sm: "640px",
        md: "768px",
        lg: "1024px",
        xl: "1280px",
        "2xl": "1536px",
      },

      /**
       * Transition/Animation System
       */
      transitionDuration: {
        DEFAULT: "200ms",
        fast: "100ms",
        normal: "200ms",
        slow: "300ms",
      },
      transitionTimingFunction: {
        DEFAULT: "cubic-bezier(0.4, 0, 0.2, 1)",
        in: "cubic-bezier(0.4, 0, 1, 1)",
        out: "cubic-bezier(0, 0, 0.2, 1)",
        "in-out": "cubic-bezier(0.4, 0, 0.2, 1)",
      },
    },
  },

  /**
   * Component Layer
   * Define reusable component classes for consistency
   * Reference: video requirements for button styles, card styles
   */
  plugins: [
    function ({ addComponents, theme }) {
      addComponents({
        // Button Styles

        /**
         * Primary Button
         * Solid violet background with white text
         * Used for main actions (Create, Update, Submit)
         */
        ".btn-primary": {
          "@apply inline-flex items-center justify-center px-6 py-2 rounded-xl font-medium text-white bg-primary-700 hover:bg-primary-800 active:bg-primary-900 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-fast":
            {},
        },

        /**
         * Secondary Button
         * Outlined violet with text
         * Used for secondary actions (Cancel, Back)
         */
        ".btn-secondary": {
          "@apply inline-flex items-center justify-center px-6 py-2 rounded-xl font-medium text-primary-700 border-2 border-primary-700 hover:bg-primary-50 active:bg-primary-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-fast":
            {},
        },

        /**
         * Destructive Button
         * Red background for delete/destructive actions
         */
        ".btn-destructive": {
          "@apply inline-flex items-center justify-center px-6 py-2 rounded-xl font-medium text-white bg-error-500 hover:bg-error-600 active:bg-error-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-fast":
            {},
        },

        /**
         * Ghost Button
         * Minimal style, text only
         */
        ".btn-ghost": {
          "@apply inline-flex items-center justify-center px-4 py-2 rounded-xl font-medium text-gray-700 hover:bg-gray-100 active:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-fast":
            {},
        },

        // Card Styles

        /**
         * Base Card Component
         * White background with rounded corners and subtle border
         * Reference: video requirements for card styling
         */
        ".card": {
          "@apply bg-white rounded-xl shadow-sm border border-border-light": {},
        },

        /**
         * Card with Hover State
         * Elevated card for interactive elements
         */
        ".card-interactive": {
          "@apply bg-white rounded-xl shadow-sm border border-border-light hover:shadow-md hover:border-border-DEFAULT transition-all duration-normal":
            {},
        },

        /**
         * Card Header
         * For card title sections
         */
        ".card-header": {
          "@apply px-6 py-4 border-b border-border-light": {},
        },

        /**
         * Card Content
         * For card body sections
         */
        ".card-content": {
          "@apply px-6 py-4": {},
        },

        /**
         * Card Footer
         * For card action sections
         */
        ".card-footer": {
          "@apply px-6 py-4 border-t border-border-light bg-background-secondary":
            {},
        },

        // Form Styles

        /**
         * Form Input Base
         * Reusable input styling
         */
        ".input-base": {
          "@apply w-full px-4 py-2 border border-border-DEFAULT rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors":
            {},
        },

        /**
         * Form Input Error State
         */
        ".input-error": {
          "@apply border-error-500 bg-error-50 focus:ring-error-500": {},
        },

        /**
         * Form Label
         */
        ".label": {
          "@apply block text-sm font-medium text-gray-900 mb-2": {},
        },

        /**
         * Form Label Required Indicator
         */
        ".label-required": {
          "@apply text-error-500": {},
        },

        // Layout Styles

        /**
         * Page Container
         * Standard page layout wrapper
         */
        ".page-container": {
          "@apply min-h-screen bg-background-secondary": {},
        },

        /**
         * Content Wrapper
         * Standard content max-width and padding
         */
        ".content-wrapper": {
          "@apply max-w-7xl mx-auto px-4 sm:px-6 lg:px-8": {},
        },

        /**
         * Section Spacing
         * Standard vertical spacing between sections
         */
        ".section-spacing": {
          "@apply space-y-8": {},
        },

        // Alert Styles

        /**
         * Alert Container
         * Base alert styling
         */
        ".alert": {
          "@apply rounded-xl p-4 flex items-start gap-4": {},
        },

        /**
         * Success Alert
         */
        ".alert-success": {
          "@apply bg-success-50 border border-success-200 text-success-900":
            {},
        },

        /**
         * Error Alert
         */
        ".alert-error": {
          "@apply bg-error-50 border border-error-200 text-error-900": {},
        },

        /**
         * Warning Alert
         */
        ".alert-warning": {
          "@apply bg-warning-50 border border-warning-200 text-warning-900":
            {},
        },

        /**
         * Info Alert
         */
        ".alert-info": {
          "@apply bg-blue-50 border border-blue-200 text-blue-900": {},
        },

        // Utility Classes

        /**
         * Text Truncation
         * Single line ellipsis
         */
        ".truncate-1": {
          "@apply truncate": {},
        },

        /**
         * Multi-line Truncation
         * Up to 2 lines
         */
        ".truncate-2": {
          "@apply line-clamp-2": {},
        },

        /**
         * Multi-line Truncation
         * Up to 3 lines
         */
        ".truncate-3": {
          "@apply line-clamp-3": {},
        },

        /**
         * Fade In Animation
         * Subtle fade-in effect for components
         */
        ".fade-in": {
          "@apply animate-fade-in": {},
        },

        /**
         * Scrollbar Styling
         * Custom scrollbar for modern look
         */
        ".scrollbar-thin": {
          "@apply scrollbar-w-2 scrollbar-track-gray-100 scrollbar-thumb-gray-300 hover:scrollbar-thumb-gray-400":
            {},
        },
      });
    },

    function ({ addUtilities }) {
      addUtilities({
        ".animation-delay-100": {
          "animation-delay": "100ms",
        },
        ".animation-delay-200": {
          "animation-delay": "200ms",
        },
        ".animation-delay-300": {
          "animation-delay": "300ms",
        },
      });
    },
  ],
};

export default config;
