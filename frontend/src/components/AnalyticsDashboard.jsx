import React from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend, AreaChart, Area
} from 'recharts';
import { TrendingUp, PieChartIcon } from 'lucide-react';

// ── Colour palette for the pie chart slices ──────────────────────────────────
const PIE_COLORS = [
  '#7c3aed', // violet-700
  '#059669', // emerald-600
  '#d97706', // amber-600
  '#2563eb', // blue-600
  '#db2777', // pink-600
  '#0891b2', // cyan-600
  '#65a30d', // lime-600
  '#9333ea', // purple-600
  '#ea580c', // orange-600
  '#0d9488', // teal-600
];

// ── Custom Tooltip for the Line/Area chart ───────────────────────────────────
function RevenueTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-white/90 dark:bg-slate-800/90 border border-violet-200 dark:border-violet-700 rounded-2xl px-4 py-3 shadow-xl shadow-violet-100/40 dark:shadow-violet-900/30 backdrop-blur-md">
      <p className="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-1">{label}</p>
      <p className="text-lg font-extrabold text-violet-700 dark:text-violet-400">
        ${payload[0].value.toFixed(2)}
      </p>
    </div>
  );
}

// ── Custom Tooltip for the Pie chart ─────────────────────────────────────────
function PieTooltip({ active, payload }) {
  if (!active || !payload?.length) return null;
  const entry = payload[0];
  return (
    <div className="bg-white/90 dark:bg-slate-800/90 border border-slate-200 dark:border-slate-700 rounded-2xl px-4 py-3 shadow-xl backdrop-blur-md">
      <p className="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-0.5">{entry.name}</p>
      <p className="text-base font-bold" style={{ color: entry.payload.fill }}>
        {entry.value} units
      </p>
      <p className="text-xs text-slate-400 mt-0.5">
        {(entry.percent * 100).toFixed(1)}% of total
      </p>
    </div>
  );
}

// ── Custom Legend for Pie chart ───────────────────────────────────────────────
function CustomLegend({ payload }) {
  if (!payload?.length) return null;
  return (
    <ul className="flex flex-wrap gap-x-4 gap-y-2 justify-center mt-4 px-2">
      {payload.map((entry, idx) => (
        <li key={idx} className="flex items-center gap-1.5 text-xs font-semibold text-slate-600 dark:text-slate-300">
          <span
            className="w-2.5 h-2.5 rounded-full flex-shrink-0"
            style={{ backgroundColor: entry.color }}
          />
          {entry.value}
        </li>
      ))}
    </ul>
  );
}

// ── Empty-state placeholder ───────────────────────────────────────────────────
function EmptyChart({ label }) {
  return (
    <div className="flex flex-col items-center justify-center h-48 gap-3 text-slate-400">
      <div className="w-12 h-12 rounded-full bg-slate-100 dark:bg-slate-700 flex items-center justify-center text-2xl">
        📊
      </div>
      <p className="text-sm font-medium">{label}</p>
      <p className="text-xs text-slate-400">Place an order to see data here</p>
    </div>
  );
}

// ── Main component ────────────────────────────────────────────────────────────
export default function AnalyticsDashboard({ analyticsData }) {
  const revenueData   = analyticsData?.revenue_last_7_days   ?? [];
  const categoryData  = analyticsData?.quantity_by_category  ?? [];
  const totalRevenue  = analyticsData?.total_revenue          ?? 0;
  const totalOrders   = analyticsData?.total_orders           ?? 0;

  const hasRevenueData  = revenueData.some(d => d.revenue > 0);
  const hasCategoryData = categoryData.length > 0;

  return (
    <div className="bg-white/60 dark:bg-slate-900/60 border border-slate-200/50 dark:border-slate-700/50 backdrop-blur-xl rounded-3xl p-8 shadow-sm space-y-8">

      {/* ── Section header ──────────────────────────────────────────────── */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-violet-100 dark:bg-violet-900/50 rounded-xl">
            <TrendingUp className="w-5 h-5 text-violet-600 dark:text-violet-400" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-800 dark:text-slate-100 tracking-tight">
              Analytics Overview
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">Visual summary of recent sales performance</p>
          </div>
        </div>

        {/* ── KPI pills ─────────────────────────────────────────────────── */}
        <div className="flex gap-3 flex-wrap">
          <div className="flex flex-col items-center px-5 py-3 bg-violet-50 dark:bg-violet-950/50 border border-violet-100 dark:border-violet-800/50 rounded-2xl min-w-[100px]">
            <span className="text-[11px] font-semibold uppercase tracking-widest text-violet-500 dark:text-violet-400">Revenue</span>
            <span className="text-xl font-extrabold text-violet-700 dark:text-violet-300 mt-0.5">
              ${totalRevenue.toFixed(2)}
            </span>
          </div>
          <div className="flex flex-col items-center px-5 py-3 bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-100 dark:border-emerald-800/50 rounded-2xl min-w-[100px]">
            <span className="text-[11px] font-semibold uppercase tracking-widest text-emerald-500 dark:text-emerald-400">Orders</span>
            <span className="text-xl font-extrabold text-emerald-700 dark:text-emerald-300 mt-0.5">
              {totalOrders}
            </span>
          </div>
        </div>
      </div>

      {/* ── Charts grid ─────────────────────────────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

        {/* ── Line / Area Chart — Revenue Trend ─────────────────────────── */}
        <div className="bg-white dark:bg-slate-800/80 rounded-2xl border border-slate-100 dark:border-slate-700/50 p-6 shadow-sm">
          <div className="flex items-center gap-2 mb-5">
            <TrendingUp className="w-4 h-4 text-violet-500" />
            <h3 className="text-sm font-bold text-slate-700 dark:text-slate-200 uppercase tracking-wider">
              Revenue — Last 7 Days
            </h3>
          </div>

          {hasRevenueData ? (
            <ResponsiveContainer width="100%" height={220}>
              <AreaChart data={revenueData} margin={{ top: 4, right: 4, left: -10, bottom: 0 }}>
                <defs>
                  <linearGradient id="revenueGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor="#7c3aed" stopOpacity={0.25} />
                    <stop offset="95%" stopColor="#7c3aed" stopOpacity={0.02} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.15)" vertical={false} />
                <XAxis
                  dataKey="date"
                  tick={{ fontSize: 11, fill: '#94a3b8', fontWeight: 600 }}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis
                  tick={{ fontSize: 11, fill: '#94a3b8', fontWeight: 600 }}
                  axisLine={false}
                  tickLine={false}
                  tickFormatter={v => `$${v}`}
                />
                <Tooltip content={<RevenueTooltip />} cursor={{ stroke: '#7c3aed', strokeWidth: 1.5, strokeDasharray: '4 4' }} />
                <Area
                  type="monotone"
                  dataKey="revenue"
                  stroke="#7c3aed"
                  strokeWidth={2.5}
                  fill="url(#revenueGradient)"
                  dot={{ r: 4, fill: '#7c3aed', strokeWidth: 2, stroke: '#fff' }}
                  activeDot={{ r: 6, fill: '#7c3aed', strokeWidth: 2, stroke: '#fff' }}
                />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <EmptyChart label="No revenue data yet" />
          )}
        </div>

        {/* ── Pie Chart — Category Popularity ───────────────────────────── */}
        <div className="bg-white dark:bg-slate-800/80 rounded-2xl border border-slate-100 dark:border-slate-700/50 p-6 shadow-sm">
          <div className="flex items-center gap-2 mb-5">
            <PieChartIcon className="w-4 h-4 text-emerald-500" />
            <h3 className="text-sm font-bold text-slate-700 dark:text-slate-200 uppercase tracking-wider">
              Units Sold by Category
            </h3>
          </div>

          {hasCategoryData ? (
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie
                  data={categoryData}
                  dataKey="quantity"
                  nameKey="category"
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={90}
                  paddingAngle={3}
                  strokeWidth={0}
                >
                  {categoryData.map((_, idx) => (
                    <Cell
                      key={idx}
                      fill={PIE_COLORS[idx % PIE_COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip content={<PieTooltip />} />
                <Legend content={<CustomLegend />} />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <EmptyChart label="No category data yet" />
          )}
        </div>
      </div>
    </div>
  );
}
