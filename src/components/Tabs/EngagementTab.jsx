import React from 'react';
import {
  BarChart, Bar,
  AreaChart, Area,
  XAxis, YAxis,
  CartesianGrid, Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { Eye, ThumbsUp, MessageSquare, Percent, BarChart3, TrendingUp } from 'lucide-react';
import { formatCompact, formatNumber, formatPercentage } from '../../utils/formatters';

const GlassTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="p-3 rounded-xl text-xs space-y-1"
        style={{ background: 'rgba(11,13,20,0.97)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.1)', boxShadow: '0 16px 48px rgba(0,0,0,0.7)' }}>
        <p className="font-semibold text-slate-200 pb-1" style={{ borderBottom: '1px solid rgba(255,255,255,0.08)' }}>{label}</p>
        {payload.map((item, idx) => (
          <div key={idx} className="flex items-center justify-between gap-4">
            <span className="flex items-center gap-1.5 text-slate-400">
              <span className="w-2 h-2 rounded-full" style={{ background: item.color || item.fill }} />
              {item.name}:
            </span>
            <span className="font-mono font-bold text-white">
              {item.name.includes('Rate') ? formatPercentage(item.value) : formatCompact(item.value)}
            </span>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

const AVG_CARDS = [
  { label: 'Average Views per Video',    key: 'avgViews',           fmt: formatCompact,    color: '#0ea5e9', glow: '14,165,233' },
  { label: 'Average Likes per Video',    key: 'avgLikes',           fmt: formatCompact,    color: '#f43f5e', glow: '244,63,94'  },
  { label: 'Average Comments per Video', key: 'avgComments',        fmt: formatCompact,    color: '#a855f7', glow: '168,85,247' },
  { label: 'Average Engagement Rate',    key: 'avgEngagementRate',  fmt: formatPercentage, color: '#f59e0b', glow: '245,158,11' },
];
const AVG_ICONS = [Eye, ThumbsUp, MessageSquare, Percent];

export const EngagementTab = ({ kpis, engagementBreakdownData, viewsTrendData }) => {
  return (
    <div className="space-y-5">
      {/* 4 Average Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        {AVG_CARDS.map((card, i) => {
          const Icon = AVG_ICONS[i];
          return (
            <div key={card.key} className="p-5 rounded-2xl transition-all duration-200 hover:-translate-y-1 animate-fade-up"
              style={{
                background: `linear-gradient(140deg, rgba(${card.glow},0.14) 0%, rgba(${card.glow},0.04) 50%, rgba(12,14,22,0.8) 100%)`,
                border: `1px solid rgba(${card.glow},0.22)`,
                boxShadow: `0 8px 28px -8px rgba(${card.glow},0.18)`,
                animationDelay: `${i * 60}ms`,
              }}>
              <div className="flex items-center justify-between mb-3">
                <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">{card.label}</p>
                <div className="p-2 rounded-xl"
                  style={{ background: `rgba(${card.glow},0.12)`, border: `1px solid rgba(${card.glow},0.22)` }}>
                  <Icon className="w-4 h-4" style={{ color: card.color }} />
                </div>
              </div>
              <h3 className="text-2xl font-extrabold text-white font-heading" title={formatNumber(kpis[card.key])}>
                {card.fmt(kpis[card.key])}
              </h3>
              <p className="text-[10px] text-slate-500 mt-1 font-mono">
                Exact: {card.key === 'avgEngagementRate'
                  ? `${kpis[card.key].toFixed(4)}%`
                  : formatNumber(kpis[card.key])}
              </p>
            </div>
          );
        })}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Interaction Comparison */}
        <div className="lg:col-span-7 glass-panel p-5 lg:p-6 rounded-3xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <div className="flex items-center gap-2">
                <BarChart3 className="w-4 h-4 text-rose-400" />
                <h3 className="text-sm font-bold text-white font-heading">Interaction Comparison by Category</h3>
              </div>
              <p className="text-[11px] text-slate-400 mt-0.5">Likes vs Comments breakdown across categories</p>
            </div>
            <div className="flex items-center gap-3 text-[11px]">
              {[['#f43f5e','Likes'],['#0ea5e9','Comments']].map(([c,l]) => (
                <span key={l} className="flex items-center gap-1.5 text-slate-400">
                  <span className="w-2 h-2 rounded-full" style={{ background: c }} />{l}
                </span>
              ))}
            </div>
          </div>

          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={engagementBreakdownData} margin={{ top: 4, right: 6, left: -18, bottom: 28 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" vertical={false} />
                <XAxis dataKey="category" tick={{ fill: '#64748b', fontSize: 10 }} tickLine={false}
                  axisLine={{ stroke: 'rgba(255,255,255,0.07)' }} angle={-15} textAnchor="end" interval={0} />
                <YAxis tick={{ fill: '#64748b', fontSize: 10 }} tickLine={false} axisLine={false}
                  tickFormatter={(v) => formatCompact(v)} />
                <Tooltip content={<GlassTooltip />} />
                <Bar dataKey="likes"    name="Likes"    fill="#f43f5e" radius={[3,3,0,0]} maxBarSize={24} />
                <Bar dataKey="comments" name="Comments" fill="#0ea5e9" radius={[3,3,0,0]} maxBarSize={24} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Engagement Rate Timeline */}
        <div className="lg:col-span-5 glass-panel p-5 lg:p-6 rounded-3xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <div className="flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-amber-400" />
                <h3 className="text-sm font-bold text-white font-heading">Engagement Rate Timeline</h3>
              </div>
              <p className="text-[11px] text-slate-400 mt-0.5">Avg engagement % over trending dates</p>
            </div>
            <span className="text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full"
              style={{ background: 'rgba(245,158,11,0.12)', border: '1px solid rgba(245,158,11,0.3)', color: '#fbbf24' }}>
              Avg {formatPercentage(kpis.avgEngagementRate)}
            </span>
          </div>

          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={viewsTrendData} margin={{ top: 4, right: 6, left: -22, bottom: 0 }}>
                <defs>
                  <linearGradient id="gradEngTab" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor="#f59e0b" stopOpacity={0.38} />
                    <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" vertical={false} />
                <XAxis dataKey="date" tick={{ fill: '#64748b', fontSize: 10 }} tickLine={false}
                  axisLine={{ stroke: 'rgba(255,255,255,0.07)' }} tickFormatter={(v) => v.slice(5)} />
                <YAxis tick={{ fill: '#64748b', fontSize: 10 }} tickLine={false} axisLine={false}
                  tickFormatter={(v) => `${v}%`} />
                <Tooltip content={<GlassTooltip />} />
                <Area type="monotone" dataKey="avgEngagementRate" name="Engagement Rate"
                  stroke="#f59e0b" strokeWidth={2.5} fill="url(#gradEngTab)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
