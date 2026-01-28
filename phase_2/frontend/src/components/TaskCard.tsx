/**
 * Task: T067 | Spec: @specs/001-sdd-initialization/ui/pages.md §Task Card Component
 * Description: Task card component displaying task with status badge, actions
 * Purpose: Reusable card for displaying task in list or dashboard
 * Reference: plan.md Step 5 §Key Design Pattern, Constitution III (User Isolation)
 */

'use client';

import { useState } from 'react';
import Link from 'next/link';
import { formatDistanceToNow } from 'date-fns';
import { TASK_STATUS, TASK_STATUS_COLORS } from '@/config/constants';

interface Task {
  id: string;
  title: string;
  description?: string;
  status: string;
  created_at: string;
  updated_at: string;
  user_id: string; // From JWT - ensures user isolation
}

interface TaskCardProps {
  task: Task;
  onEdit: (taskId: string) => void;
  onDelete: (taskId: string) => void;
}

/**
 * TaskCard Component
 *
 * Displays a single task with:
 * - Checkbox (visual feedback, not backend update)
 * - Title (clickable to edit)
 * - First line of description
 * - Status badge with color coding
 * - Relative timestamp ("2 hours ago")
 * - Edit button
 * - Delete button (via onDelete callback)
 *
 * User Isolation: Task.user_id must match authenticated user_id
 * This component is rendered only for tasks belonging to current user.
 */
export default function TaskCard({ task, onEdit, onDelete }: TaskCardProps) {
  const [isChecked, setIsChecked] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  // Get status badge color
  const getStatusColor = (status: string): string => {
    const colors: Record<string, string> = {
      [TASK_STATUS.PENDING]: 'bg-blue-100 text-blue-800',
      [TASK_STATUS.IN_PROGRESS]: 'bg-orange-100 text-orange-800',
      [TASK_STATUS.COMPLETED]: 'bg-green-100 text-green-800',
      [TASK_STATUS.ARCHIVED]: 'bg-gray-100 text-gray-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  // Format relative time
  const relativeTime = formatDistanceToNow(new Date(task.created_at), {
    addSuffix: true,
  });

  // Get first line of description
  const descriptionPreview = task.description
    ? task.description.split('\n')[0].substring(0, 100)
    : '';

  const handleDelete = async () => {
    if (window.confirm('Are you sure? This task will be permanently deleted.')) {
      setIsDeleting(true);
      try {
        onDelete(task.id);
      } finally {
        setIsDeleting(false);
      }
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow p-4">
      <div className="flex gap-4">
        {/* Checkbox */}
        <div className="flex items-center pt-1">
          <input
            type="checkbox"
            checked={isChecked}
            onChange={(e) => setIsChecked(e.target.checked)}
            className="w-5 h-5 text-blue-600 rounded cursor-pointer"
            aria-label={`Mark task "${task.title}" as complete`}
          />
        </div>

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          {/* Title and Status */}
          <div className="flex items-start justify-between gap-2 mb-2">
            <button
              onClick={() => onEdit(task.id)}
              className="text-left font-semibold text-gray-900 hover:text-blue-600 transition-colors truncate flex-1"
            >
              {task.title}
            </button>
            <span
              className={`inline-block px-2 py-1 text-xs font-medium rounded-full whitespace-nowrap ${getStatusColor(
                task.status
              )}`}
            >
              {task.status}
            </span>
          </div>

          {/* Description Preview */}
          {descriptionPreview && (
            <p className="text-gray-600 text-sm mb-2 line-clamp-2">
              {descriptionPreview}
              {task.description && task.description.length > 100 && '...'}
            </p>
          )}

          {/* Metadata */}
          <div className="text-gray-500 text-xs">
            Created {relativeTime}
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-2 items-start">
          <Link
            href={`/dashboard/tasks/${task.id}`}
            className="px-3 py-2 text-sm font-medium text-blue-600 hover:bg-blue-50 rounded transition-colors"
            title="Edit task"
          >
            Edit
          </Link>
          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="px-3 py-2 text-sm font-medium text-red-600 hover:bg-red-50 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            title="Delete task"
          >
            {isDeleting ? 'Deleting...' : 'Delete'}
          </button>
        </div>
      </div>
    </div>
  );
}
