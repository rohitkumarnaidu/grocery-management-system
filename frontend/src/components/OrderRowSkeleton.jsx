// frontend/src/components/OrderRowSkeleton.jsx
// Skeleton placeholder that mimics the Order Ledger table row:
// Order ID | Date & Time | Items | Total (4 columns)

import React from 'react';
import { TableRow, TableCell } from '@/components/ui/table';
import { Skeleton } from '@/components/ui/Skeleton';

export default function OrderRowSkeleton() {
  return (
    <TableRow className="border-slate-100 dark:border-slate-700" aria-hidden="true">
      {/* Order ID column */}
      <TableCell className="px-6 py-4">
        <Skeleton className="h-4 w-20 rounded-md" />
      </TableCell>

      {/* Date & Time column */}
      <TableCell className="py-4">
        <Skeleton className="h-4 w-32 rounded-md" />
      </TableCell>

      {/* Items column */}
      <TableCell className="py-4">
        <Skeleton className="h-4 w-48 rounded-md" />
      </TableCell>

      {/* Total column */}
      <TableCell className="text-right pr-6 py-4">
        <Skeleton className="h-4 w-16 ml-auto rounded-md" />
      </TableCell>
    </TableRow>
  );
}
