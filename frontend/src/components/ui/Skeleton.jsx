// frontend/src/components/ui/Skeleton.jsx
// Base Skeleton component with animate-pulse + dark mode support
// Variants: SkeletonText, SkeletonCard, SkeletonRow

import React from 'react';
import { cn } from '@/lib/utils';

/**
 * Base Skeleton — animated pulse placeholder block.
 */
export function Skeleton({ className, ...props }) {
  return (
    <div
      className={cn(
        'animate-pulse rounded-lg bg-slate-200 dark:bg-slate-700',
        className
      )}
      aria-hidden="true"
      {...props}
    />
  );
}

/**
 * SkeletonText — single line of placeholder text.
 */
export function SkeletonText({ className }) {
  return <Skeleton className={cn('h-4 w-full rounded-md', className)} />;
}

/**
 * SkeletonCard — card-shaped placeholder block.
 */
export function SkeletonCard({ className }) {
  return (
    <Skeleton
      className={cn('h-40 w-full rounded-2xl', className)}
    />
  );
}

/**
 * SkeletonRow — single table-row-shaped placeholder.
 */
export function SkeletonRow({ className }) {
  return (
    <div className={cn('flex items-center gap-4 px-6 py-4', className)} aria-hidden="true">
      <Skeleton className="h-4 w-24" />
      <Skeleton className="h-4 w-32" />
      <Skeleton className="h-4 flex-1" />
      <Skeleton className="h-4 w-16" />
    </div>
  );
}
