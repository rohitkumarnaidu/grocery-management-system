// frontend/src/components/ProductCardSkeleton.jsx
// Skeleton placeholder that mimics the product card layout exactly:
// emoji block → title → category tag → price → stock bar → button

import React from 'react';
import { Skeleton } from '@/components/ui/Skeleton';

export default function ProductCardSkeleton() {
  return (
    <div
      className="border border-slate-200/60 dark:border-slate-700/60 rounded-2xl p-5 bg-white dark:bg-slate-800/80"
      aria-hidden="true"
    >
      {/* Emoji / image block */}
      <Skeleton className="w-12 h-12 rounded-full mx-auto mb-4" />

      {/* Product name */}
      <Skeleton className="h-4 w-3/4 mx-auto mb-2 rounded-md" />

      {/* Category tag */}
      <Skeleton className="h-3 w-1/2 mx-auto mb-4 rounded-full" />

      {/* Price */}
      <Skeleton className="h-7 w-1/3 mx-auto mb-4 rounded-md" />

      {/* Stock bar */}
      <Skeleton className="h-8 w-full mb-5 rounded-xl" />

      {/* Add to Cart button */}
      <Skeleton className="h-11 w-full rounded-xl" />
    </div>
  );
}
