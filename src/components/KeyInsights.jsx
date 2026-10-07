import React from 'react';
import { Trophy, Award, Play, Heart, Calendar, Clock, Zap } from 'lucide-react';
import { formatCompact } from '../utils/formatters';

const INSIGHT_CONFIG = [
  {
    title: 'Top Channel (Views)',
    getLabel: (ins) => ins.topChannelViews.name,
    getSub: (ins) => `${formatCompact(ins.topChannelViews.value)} total views`,
    icon: Trophy,
    iconStyle: { background: 'rgba(245,158,11,0.12)', border: '1px solid rgba(245,158,11,0.25)', color: '#fcd34d' },
    accentStyle: { borderLeft: '3px solid rgba(245,158,11,0.5)' },
  },
  {
    title: 'Top Channel (Likes)',
    getLabel: (ins) => ins.topChannelLikes.name,
    getSub: (ins) => `${formatCompact(ins.topChannelLikes.value)} total likes`,
    icon: Award,
    iconStyle: { background: 'rgba(244,63,94,0.12)', border: '1px solid rgba(244,63,94,0.25)', color: '#fda4af' },
    accentStyle: { borderLeft: '3px solid rgba(244,63,94,0.5)' },
  },
  {
    title: 'Most Viral Video',
    getLabel: (ins) => ins.maxViewsVideo.title,
    getSub: (ins) => `${formatCompact(ins.maxViewsVideo.views)} views · ${ins.maxViewsVideo.channel}`,
    icon: Play,
    iconStyle: { background: 'rgba(139,92,246,0.12)', border: '1px solid rgba(139,92,246,0.25)', color: '#c4b5fd' },
    accentStyle: { borderLeft: '3px solid rgba(139,92,246,0.5)' },
    isTitle: true,
  },
  {
    title: 'Most Liked Video',
    getLabel: (ins) => ins.maxLikesVideo.title,
    getSub: (ins) => `${formatCompact(ins.maxLikesVideo.likes)} likes · ${ins.maxLikesVideo.channel}`,
    icon: Heart,
    iconStyle: { background: 'rgba(239,68,68,0.12)', border: '1px solid rgba(239,68,68,0.25)', color: '#fca5a5' },
    accentStyle: { borderLeft: '3px solid rgba(239,68,68,0.5)' },
    isTitle: true,
  },
  {
    title: 'Peak Upload Day',
    getLabel: (ins) => ins.peakDay.day,
    getSub: (ins) => `${ins.peakDay.count.toLocaleString()} uploads in dataset`,
    icon: Calendar,
    iconStyle: { background: 'rgba(14,165,233,0.12)', border: '1px solid rgba(14,165,233,0.25)', color: '#7dd3fc' },
    accentStyle: { borderLeft: '3px solid rgba(14,165,233,0.5)' },
  },
  {
    title: 'Peak Upload Hour',
    getLabel: (ins) => ins.peakHour.label,
    getSub: (ins) => `${ins.peakHour.count.toLocaleString()} uploads in dataset`,
    icon: Clock,
    iconStyle: { background: 'rgba(16,185,129,0.12)', border: '1px solid rgba(16,185,129,0.25)', color: '#6ee7b7' },
    accentStyle: { borderLeft: '3px solid rgba(16,185,129,0.5)' },
  },
];

export const KeyInsights = ({ insights }) => {
  if (!insights) return null;

  return (
    <div className="mb-6">
      {/* Section heading */}
      <div className="flex items-center gap-2 mb-3">
        <Zap className="w-4 h-4 text-amber-400" />
        <h3 className="text-xs font-bold uppercase tracking-[0.12em] text-slate-300">
          Key Insights & Highlights
        </h3>
        <span className="text-[10px] text-slate-500 font-medium">(dynamically calculated from filtered data)</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-3">
        {INSIGHT_CONFIG.map((cfg, idx) => {
          const Icon = cfg.icon;
          const label = cfg.getLabel(insights);
          const sub = cfg.getSub(insights);
          return (
            <div
              key={idx}
              className="p-3.5 rounded-2xl transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg"
              style={{
                background: 'rgba(14,16,26,0.7)',
                backdropFilter: 'blur(16px)',
                border: '1px solid rgba(255,255,255,0.07)',
                ...cfg.accentStyle,
              }}
            >
              {/* Icon + Title */}
              <div className="flex items-center gap-2 mb-2">
                <div className="p-1.5 rounded-lg shrink-0" style={cfg.iconStyle}>
                  <Icon className="w-3.5 h-3.5" />
                </div>
                <span className="text-[10px] font-semibold text-slate-400 truncate uppercase tracking-wider">
                  {cfg.title}
                </span>
              </div>
              {/* Value */}
              <p className="text-xs font-bold text-white truncate" title={label}>
                {label}
              </p>
              {/* Supporting text */}
              <p className="text-[10px] text-slate-400 truncate mt-0.5" title={sub}>
                {sub}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
