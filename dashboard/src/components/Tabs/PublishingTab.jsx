import React, { useMemo } from 'react';
import {
  BarChart, Bar,
  LineChart, Line,
  XAxis, YAxis,
  CartesianGrid, Tooltip,
  ResponsiveContainer,
  AreaChart, Area
} from 'recharts';
import { Calendar, Clock, Sparkles, TrendingUp, Compass } from 'lucide-react';
import { getPublishingByDay, getPublishingByMonth, getPublishingByHour } from '../../utils/analytics';
import { formatCompact, formatNumber, formatPercentage } from '../../utils/formatters';

const CustomPublishingTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="p-3.5 rounded-xl bg-[#12141f]/95 backdrop-blur-xl border border-white/10 shadow-2xl text-xs space-y-1 z-50">
        <p className="font-semibold text-slate-300 pb-1 border-b border-white/10">{label}</p>
        {payload.map((item, idx) => (
          <div key={idx} className="flex items-center justify-between gap-4">
            <span className="flex items-center gap-1.5 text-slate-400">
              <span className="w-2 h-2 rounded-full" style={{ backgroundColor: item.color || item.fill }} />
              {item.name}:
            </span>
            <span className="font-mono font-bold text-white">
              {item.name.includes('Rate') ? formatPercentage(item.value) : formatNumber(item.value)}
            </span>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

export const PublishingTab = ({ data }) => {
  const dayData = useMemo(() => getPublishingByDay(data), [data]);
  const monthData = useMemo(() => getPublishingByMonth(data), [data]);
  const hourData = useMemo(() => getPublishingByHour(data), [data]);

  // Find peak day & hour
  const peakDay = useMemo(() => {
    let best = dayData[0];
    dayData.forEach((d) => {
      if (d.videos > (best?.videos || 0)) best = d;
    });
    return best;
  }, [dayData]);

  const peakHour = useMemo(() => {
    let best = hourData[0];
    hourData.forEach((h) => {
      if (h.videos > (best?.videos || 0)) best = h;
    });
    return best;
  }, [hourData]);

  return (
    <div className="space-y-6">
      {/* Recommendation Banner - Dataset Frequency Analysis */}
      <div className="p-5 rounded-2xl glass-panel bg-gradient-to-r from-amber-500/10 via-orange-500/10 to-red-500/10 border border-amber-500/20">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-amber-500/20 text-amber-300 border border-amber-500/30">
              <Compass className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white font-heading">
                Publishing Patterns (Frequency-Based Analysis)
              </h3>
              <p className="text-xs text-slate-300 mt-0.5">
                Highest publishing frequency in this dataset calculated across {data?.length.toLocaleString() || '33,089'} records
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3 text-xs">
            <div className="px-3 py-1.5 rounded-xl bg-white/[0.06] border border-white/10">
              <span className="text-slate-400">Peak Upload Day: </span>
              <span className="font-bold text-amber-300">{peakDay?.day}</span>
              <span className="text-[11px] text-slate-400 ml-1">({formatNumber(peakDay?.videos)} uploads)</span>
            </div>
            <div className="px-3 py-1.5 rounded-xl bg-white/[0.06] border border-white/10">
              <span className="text-slate-400">Peak Upload Hour: </span>
              <span className="font-bold text-orange-300">{peakHour?.hourLabel}</span>
              <span className="text-[11px] text-slate-400 ml-1">({formatNumber(peakHour?.videos)} uploads)</span>
            </div>
          </div>
        </div>
      </div>

      {/* Grid: Day of Week & Month */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* CHART A: Videos Published by Day */}
        <div className="lg:col-span-6 glass-panel p-6 rounded-3xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4 text-amber-400" />
                <h3 className="text-base font-bold text-white font-heading">Videos Published by Day</h3>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">Distribution across Monday through Sunday</p>
            </div>
            <span className="text-[11px] font-medium text-amber-400 bg-amber-400/10 px-2.5 py-1 rounded-full border border-amber-400/20">
              7 Days
            </span>
          </div>

          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={dayData} margin={{ top: 10, right: 10, left: -15, bottom: 5 }}>
                <defs>
                  <linearGradient id="dayBarGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#f59e0b" />
                    <stop offset="100%" stopColor="#d97706" />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis 
                  dataKey="shortDay" 
                  tick={{ fill: '#94a3b8', fontSize: 11 }}
                  tickLine={false}
                  axisLine={{ stroke: 'rgba(255,255,255,0.08)' }}
                />
                <YAxis 
                  tick={{ fill: '#94a3b8', fontSize: 10 }}
                  tickLine={false}
                  axisLine={false}
                  tickFormatter={(val) => formatCompact(val)}
                />
                <Tooltip content={<CustomPublishingTooltip />} />
                <Bar 
                  dataKey="videos" 
                  name="Videos Published" 
                  fill="url(#dayBarGrad)" 
                  radius={[6, 6, 0, 0]} 
                  maxBarSize={38} 
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* CHART B: Videos Published by Month */}
        <div className="lg:col-span-6 glass-panel p-6 rounded-3xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4 text-purple-400" />
                <h3 className="text-base font-bold text-white font-heading">Videos Published by Month</h3>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">Chronological month sequence (Jan - Dec)</p>
            </div>
            <span className="text-[11px] font-medium text-purple-400 bg-purple-400/10 px-2.5 py-1 rounded-full border border-purple-400/20">
              12 Months
            </span>
          </div>

          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={monthData} margin={{ top: 10, right: 10, left: -15, bottom: 5 }}>
                <defs>
                  <linearGradient id="monthBarGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#a855f7" />
                    <stop offset="100%" stopColor="#6366f1" />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis 
                  dataKey="month" 
                  tick={{ fill: '#94a3b8', fontSize: 10 }}
                  tickLine={false}
                  axisLine={{ stroke: 'rgba(255,255,255,0.08)' }}
                />
                <YAxis 
                  tick={{ fill: '#94a3b8', fontSize: 10 }}
                  tickLine={false}
                  axisLine={false}
                  tickFormatter={(val) => formatCompact(val)}
                />
                <Tooltip content={<CustomPublishingTooltip />} />
                <Bar 
                  dataKey="videos" 
                  name="Videos Published" 
                  fill="url(#monthBarGrad)" 
                  radius={[6, 6, 0, 0]} 
                  maxBarSize={28} 
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* CHART C: Videos Published by Hour (0 to 23) */}
      <div className="glass-panel p-6 rounded-3xl">
        <div className="flex items-center justify-between mb-4">
          <div>
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-rose-400" />
              <h3 className="text-base font-bold text-white font-heading">
                Videos Published by Hour (24-Hour Timeline)
              </h3>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              Upload frequency hourly pattern (0:00 to 23:00)
            </p>
          </div>
          <span className="text-[11px] font-medium text-rose-400 bg-rose-400/10 px-2.5 py-1 rounded-full border border-rose-400/20">
            0h - 23h
          </span>
        </div>

        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={hourData} margin={{ top: 10, right: 10, left: -15, bottom: 5 }}>
              <defs>
                <linearGradient id="hourGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.45} />
                  <stop offset="95%" stopColor="#f43f5e" stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
              <XAxis 
                dataKey="hour" 
                tick={{ fill: '#94a3b8', fontSize: 10 }}
                tickLine={false}
                axisLine={{ stroke: 'rgba(255,255,255,0.08)' }}
                tickFormatter={(h) => (h % 3 === 0 ? `${h}:00` : '')}
              />
              <YAxis 
                tick={{ fill: '#94a3b8', fontSize: 10 }}
                tickLine={false}
                axisLine={false}
                tickFormatter={(val) => formatCompact(val)}
              />
              <Tooltip content={<CustomPublishingTooltip />} />
              <Area 
                type="monotone" 
                dataKey="videos" 
                name="Videos Published" 
                stroke="#f43f5e" 
                strokeWidth={2.5}
                fillOpacity={1}
                fill="url(#hourGrad)" 
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
