/**
 * Task: T070 | Spec: @specs/001-sdd-initialization/ui/pages.md §Dashboard Page
 * Description: Dashboard page with task list and CRUD operations
 * Purpose: Display and manage user's tasks with full CRUD functionality
 * Reference: Constitution III (User Isolation), plan.md Step 5
 */

"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { apiCall } from "@/lib/api";
import type { Task, TaskCreate } from "@/types/task";
import { TaskStatus } from "@/types/task";

/**
 * Dashboard page component
 *
 * Features:
 * - Display list of user's tasks
 * - Create new task with simple form
 * - Mark tasks as complete
 * - Delete tasks
 * - User isolation enforced via JWT (Constitution III)
 *
 * Reference:
 * - UI spec: @specs/001-sdd-initialization/ui/pages.md §Dashboard Page
 * - API spec: rest-endpoints.md §Task CRUD endpoints
 * - User Story: US-Task-1, US-Task-2, US-Task-4
 */
export default function DashboardPage() {
  const { user, isLoading: authLoading } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Form state
  const [newTaskTitle, setNewTaskTitle] = useState("");
  const [newTaskDescription, setNewTaskDescription] = useState("");
  const [isCreating, setIsCreating] = useState(false);

  /**
   * Load tasks from API
   * Constitution III: User isolation enforced by backend filtering by user_id
   */
  async function loadTasks() {
    try {
      setLoading(true);
      setError(null);

      const response = await apiCall("/api/v1/tasks?page=1&limit=100");

      if (!response.ok) {
        throw new Error(`Failed to load tasks: ${response.statusText}`);
      }

      const data = await response.json();
      setTasks(data.data || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load tasks");
    } finally {
      setLoading(false);
    }
  }

  /**
   * Create new task
   * Constitution III: user_id automatically assigned from JWT on backend
   */
  async function handleCreateTask(e: React.FormEvent) {
    e.preventDefault();

    if (!newTaskTitle.trim()) {
      setError("Task title is required");
      return;
    }

    try {
      setIsCreating(true);
      setError(null);

      const taskData: TaskCreate = {
        title: newTaskTitle.trim(),
        description: newTaskDescription.trim() || undefined,
      };

      const response = await apiCall("/api/v1/tasks", {
        method: "POST",
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Failed to create task");
      }

      // Clear form
      setNewTaskTitle("");
      setNewTaskDescription("");

      // Reload tasks
      await loadTasks();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create task");
    } finally {
      setIsCreating(false);
    }
  }

  /**
   * Toggle task completion status
   */
  async function handleToggleComplete(task: Task) {
    try {
      const newStatus = task.status === TaskStatus.COMPLETED ? TaskStatus.PENDING : TaskStatus.COMPLETED;

      const response = await apiCall(`/api/v1/tasks/${task.id}`, {
        method: "PATCH",
        body: JSON.stringify({ status: newStatus }),
      });

      if (!response.ok) {
        throw new Error("Failed to update task");
      }

      // Update local state
      setTasks(tasks.map(t =>
        t.id === task.id ? { ...t, status: newStatus } : t
      ));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update task");
    }
  }

  /**
   * Delete task
   * Constitution III: Backend verifies user owns the task before deletion
   */
  async function handleDeleteTask(taskId: string) {
    if (!confirm("Are you sure you want to delete this task?")) {
      return;
    }

    try {
      const response = await apiCall(`/api/v1/tasks/${taskId}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("Failed to delete task");
      }

      // Remove from local state
      setTasks(tasks.filter(t => t.id !== taskId));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete task");
    }
  }

  /**
   * Load tasks on component mount
   */
  useEffect(() => {
    if (!authLoading && user) {
      loadTasks();
    }
  }, [authLoading, user]);

  // Show loading state during auth check
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  // Show error if not authenticated (should not happen due to middleware)
  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-lg text-red-600">Please log in to access the dashboard</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-6xl py-6 sm:py-8 lg:py-12">
        {/* Header Section */}
        <div className="mb-8">
          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 dark:text-white">
            Dashboard
          </h1>
          <p className="mt-2 text-sm sm:text-base text-gray-600 dark:text-gray-400">
            Welcome, {user.email}
          </p>
        </div>

        {/* Error Alert - Responsive */}
        {error && (
          <div className="mb-6 rounded-md bg-red-50 dark:bg-red-900/20 p-4 sm:p-5 border border-red-200 dark:border-red-800">
            <p className="text-xs sm:text-sm font-medium text-red-800 dark:text-red-200">
              {error}
            </p>
            <button
              onClick={() => setError(null)}
              className="mt-2 text-xs sm:text-sm text-red-600 dark:text-red-400 hover:underline"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Create Task Form - Responsive */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 sm:p-6 mb-8">
          <h2 className="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Create New Task
          </h2>
          <form onSubmit={handleCreateTask} className="space-y-4">
            <div>
              <label htmlFor="title" className="block text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300 mb-1 sm:mb-2">
                Title *
              </label>
              <input
                id="title"
                type="text"
                value={newTaskTitle}
                onChange={(e) => setNewTaskTitle(e.target.value)}
                placeholder="Enter task title"
                className="input w-full text-sm sm:text-base mt-1"
                disabled={isCreating}
                required
                maxLength={255}
              />
            </div>

            <div>
              <label htmlFor="description" className="block text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300 mb-1 sm:mb-2">
                Description (optional)
              </label>
              <textarea
                id="description"
                value={newTaskDescription}
                onChange={(e) => setNewTaskDescription(e.target.value)}
                placeholder="Enter task description"
                className="input w-full text-sm sm:text-base mt-1"
                disabled={isCreating}
                rows={3}
                maxLength={2000}
              />
            </div>

            <button
              type="submit"
              disabled={isCreating || !newTaskTitle.trim()}
              className="btn-primary w-full text-sm sm:text-base"
            >
              {isCreating ? "Creating..." : "Create Task"}
            </button>
          </form>
        </div>

        {/* Task List - Responsive Grid */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 sm:p-6">
          <h2 className="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white mb-4">
            My Tasks ({tasks.length})
          </h2>

          {loading ? (
            <div className="text-center py-8 sm:py-12">
              <div className="text-sm sm:text-base text-gray-600 dark:text-gray-400">Loading tasks...</div>
            </div>
          ) : tasks.length === 0 ? (
            <div className="text-center py-8 sm:py-12">
              <p className="text-sm sm:text-base text-gray-600 dark:text-gray-400">
                No tasks yet. Create one to get started!
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4 sm:gap-5 lg:gap-6">
              {tasks.map((task) => (
                <div
                  key={task.id}
                  className="flex flex-col sm:flex-row sm:items-start gap-3 sm:gap-4 p-3 sm:p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                >
                  {/* Checkbox */}
                  <input
                    type="checkbox"
                    checked={task.status === "Completed"}
                    onChange={() => handleToggleComplete(task)}
                    className="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500 flex-shrink-0"
                  />

                  {/* Task Content */}
                  <div className="flex-1 min-w-0">
                    <h3
                      className={`text-base sm:text-lg font-medium break-words ${
                        task.status === TaskStatus.COMPLETED
                          ? "line-through text-gray-500 dark:text-gray-500"
                          : "text-gray-900 dark:text-white"
                      }`}
                    >
                      {task.title}
                    </h3>
                    {task.description && (
                      <p className="mt-1 text-xs sm:text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
                        {task.description}
                      </p>
                    )}
                    <div className="mt-2 flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-3 text-xs text-gray-500 dark:text-gray-500">
                      <span
                        className={`px-2 py-1 rounded-full w-fit ${
                          task.status === TaskStatus.COMPLETED
                            ? "bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300"
                            : task.status === TaskStatus.IN_PROGRESS
                            ? "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300"
                            : "bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300"
                        }`}
                      >
                        {task.status}
                      </span>
                      <span className="text-xs">
                        Created: {new Date(task.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>

                  {/* Delete Button */}
                  <button
                    onClick={() => handleDeleteTask(task.id)}
                    className="btn-secondary text-xs sm:text-sm px-3 py-1 text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300 w-full sm:w-auto"
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
