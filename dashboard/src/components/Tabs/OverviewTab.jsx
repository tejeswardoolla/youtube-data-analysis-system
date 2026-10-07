import React from 'react';
import {
  AreaChart, Area,
  BarChart, Bar,
  XAxis, YAxis,
  CartesianGrid, Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { TrendingUp, Award, BarChart3, Activity } from 'lucide-react';
import { formatCompact, formatNumber, formatPercentage } from '../../utils/formatters';

/* ---- Shared glass tooltip ---- */
const GlassTooltip = ({ active, payload, label, formatter }) => {
  if (active && payload && payload.length) {
    return (
      <div className="p-3 rounded-xl text-xs space-y-1 z-50"
        style={{
          background: 'rgba(11,13,20,0.97)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(255,255,255,0.1)',
          boxShadow: '0 16px 48px rgba(0,0,0,0.7)',
        }}>
        <p className="font-semibold text-slate-200 pb-1 border-b border-white/[0.08]">{label}</p>
        {payload.map((item, idx) => (
          <div key={idx} className="flex items-center justify-between gap-4">
            <span className="flex items-center gap-1.5 text-slate-400">
              <span className="w-2 h-2 rounded-full" style={{ backgroundColor: item.color || item.fill }} />
              {item.name}:
            </span>
            <span className="font-mono font-bold text-white">
              {formatter ? formatter(item.value, item.name) : formatNumber(item.value)}
            </span>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

/* ---- Card wrapper ---- */
const ChartCard = ({ title, subtitle, badge, badgeColor, icon: Icon, iconColor, children }) => (
  <div className="glass-panel rounded-3xl p-5 lg:p-6 relative overflow-hidden">
    <div className="absolute top-0 right-0 w-40 h-40 rounded-full blur-3xl pointer-events-none"
      style={{ background: 'rgba(255,255,255,0.015)' }} />
    <div className="flex items-center justify-between mb-5">
      <div>
        <div className="flex items-center gap-2 mb-0.5">
          <Icon className={`w-4 h-4 ${iconColor}`} />
          <h3 className="text-sm font-bold text-white font-heading">{title}</h3>
        </div>
        <p className="text-[11px] text-slate-400">{subtitle}</p>
      </div>
      {badge && (
        <span className="text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full"
          style={{ background: `${badgeColor}18`, border: `1px solid ${badgeColor}40`, color: badgeColor }}>
          {badge}
        </span>
      )}
    </div>
    {children}
  </div>
);

/* ---- Chart height constant ---- */
const H = 280;

export const OverviewTab = ({
  viewsTrendData,
  topChannelsData,
  engagementBreakdownData,
}) => {
  return (
    <div className="space-y-5">
      {/* Row 1: Views Trend (wider) + Top Channels */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">

        {/* CHART 1: Views Trend Area */}
        <div className="lg:col-span-7">
          <ChartCard
            title="Views Trend"
            subtitle="Aggregate views across trending dates"
            badge="Timeline"
            badgeColor="#f59e0b"
            icon={TrendingUp}
            iconColor="text-amber-400"
          >
            <div style={{ height: H }}>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={viewsTrendData} margin={{ top: 5, right: 6, left: -18, bottom: 0 }}>
                  <defs>
                    <linearGradient id="gradViews" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%"  stopColor="#f59e0b" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.045)" vertical={false} />
                  <XAxis
                    dataKey="date"
                    tick={{ fill: '#64748b', fontSize: 10 }}
                    tickLine={false}
                    axisLine={{ stroke: 'rgba(255,255,255,0.07)' }}
                    tickFormatter={(v) => v.slice(5)}
                  />
                  <YAxis
                    tick={{ fill: '#64748b', fontSize: 10 }}
                    tickLine={false}
                    axisLine={false}
                    tickFormatter={(v) => formatCompact(v)}
                  />
                  <Tooltip content={<GlassTooltip formatter={(v) => `${formatCompact(v)} (${formatNumber(v)})`} />} />
                  <Area
                    type="monotone"
                    dataKey="views"
                    name="Views"
                    stroke="#f59e0b"
                    strokeWidth={2.5}
                    fill="url(#gradViews)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </ChartCard>
        </div>

        {/* CHART 2: Top Channels horizontal bar */}
        <div className="lg:col-span-5">
          <ChartCard
            title="Top Channels by Views"
            subtitle="Top 10 creators by aggregate view volume"
            badge="Ranked"
            badgeColor="#a855f7"
            icon={Award}
            iconColor="text-purple-400"
          >
            <div style={{ height: H }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={topChannelsData}
                  layout="vertical"
                  margin={{ top: 4, right: 12, left: 30, bottom: 4 }}
                >
                  <defs>
                    <linearGradient id="gradChannel" x1="0" y1="0" x2="1" y2="0">
                      <stop offset="0%"   stopColor="#8b5cf6" />
                      <stop offset="100%" stopColor="#ec4899" />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.045)" horizontal={false} />
                  <XAxis
                    type="number"
                    tick={{ fill: '#64748b', fontSize: 10 }}
                    tickLine={false}
                    axisLine={{ stroke: 'rgba(255,255,255,0.07)' }}
                    tickFormatter={(v) => formatCompact(v)}
                  />
                  <YAxis
                    type="category"
                    dataKey="channel"
                    tick={{ fill: '#cbd5e1', fontSize: 11 }}
                    tickLine={false}
                    axisLine={false}
                    width={88}
                    tickFormatter={(v) => (v.length > 11 ? `${v.slice(0, 10)}…` : v)}
                  />
                  <Tooltip content={<GlassTooltip formatter={(v) => `${formatCompact(v)} views`} />} />
                  <Bar
                    dataKey="views"
                    name="Views"
                    fill="url(#gradChannel)"
                    radius={[0, 5, 5, 0]}
                    barSize={13}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </ChartCard>
        </div>
      </div>

      {/* Row 2: Engagement Breakdown + Engagement Rate */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">

        {/* CHART 3: Engagement Breakdown grouped bars */}
        <div className="lg:col-span-7">
          <ChartCard
            title="Engagement Breakdown by Category"
            subtitle="Likes, comments & dislikes across top categories"
            badge="Interactions"
            badgeColor="#f43f5e"
            icon={BarChart3}
            iconColor="text-rose-400"
          >
            {/* Legend */}
            <div className="flex items-center gap-4 mb-3 text-[11px] text-slate-400">
              {[['#f43f5e','Likes'],['#0ea5e9','Comments'],['#475569','Dislikes']].map(([c,l]) => (
                <span key={l} className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full" style={{ background: c }} />{l}
                </span>
              ))}
            </div>
            <div style={{ height: H - 24 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={engagementBreakdownData}
                  margin={{ top: 4, right: 6, left: -18, bottom: 28 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.045)" vertical={false} />
                  <XAxis
                    dataKey="category"
                    tick={{ fill: '#64748b', fontSize: 10 }}
                    tickLine={false}
                    axisLine={{ stroke: 'rgba(255,255,255,0.07)' }}
                    angle={-15}
                    textAnchor="end"
                    interval={0}
                  />
                  <YAxis
                    tick={{ fill: '#64748b', fontSize: 10 }}
                    tickLine={false}
                    axisLine={false}
                    tickFormatter={(v) => formatCompact(v)}
                  />
                  <Tooltip content={<GlassTooltip formatter={(v) => formatCompact(v)} />} />
                  <Bar dataKey="likes"    name="Likes"    fill="#f43f5e" radius={[3,3,0,0]} maxBarSize={20} />
                  <Bar dataKey="comments" name="Comments" fill="#0ea5e9" radius={[3,3,0,0]} maxBarSize={20} />
                  <Bar dataKey="dislikes" name="Dislikes" fill="#475569" radius={[3,3,0,0]} maxBarSize={20} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </ChartCard>
        </div>

        {/* CHART 4: Engagement Rate trend */}
        <div className="lg:col-span-5">
          <ChartCard
            title="Engagement Rate Trend"
            subtitle="Avg engagement rate (%) over trending dates"
            badge="Interaction %"
            badgeColor="#10b981"
            icon={Activity}
            iconColor="text-emerald-400"
          >
            <div style={{ height: H }}>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={viewsTrendData} margin={{ top: 5, right: 6, left: -22, bottom: 0 }}>
                  <defs>
                    <linearGradient id="gradEngRate" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%"  stopColor="#10b981" stopOpacity={0.38} />
                      <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.045)" vertical={false} />
                  <XAxis
                    dataKey="date"
                    tick={{ fill: '#64748b', fontSize: 10 }}
                    tickLine={false}
                    axisLine={{ stroke: 'rgba(255,255,255,0.07)' }}
                    tickFormatter={(v) => v.slice(5)}
                  />
                  <YAxis
                    tick={{ fill: '#64748b', fontSize: 10 }}
                    tickLine={false}
                    axisLine={false}
                    tickFormatter={(v) => `${v}%`}
                  />
                  <Tooltip content={<GlassTooltip formatter={(v) => formatPercentage(v)} />} />
                  <Area
                    type="monotone"
                    dataKey="avgEngagementRate"
                    name="Avg Engagement Rate"
                    stroke="#10b981"
                    strokeWidth={2.5}
                    fill="url(#gradEngRate)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </ChartCard>
        </div>
      </div>
    </div>
  );
};
