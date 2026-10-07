import React from 'react';
import { Film, Eye, ThumbsUp, Activity, TrendingUp, ArrowUpRight } from 'lucide-react';
import { formatCompact, formatNumber, formatPercentage } from '../utils/formatters';

const CARDS = [
  {
    id: 'videos',
    label: 'Total Videos',
    valueKey: 'totalVideos',
    formatter: (v) => formatNumber(v),
    subtext: 'Filtered video records',
    badge: 'Dataset',
    icon: Film,
    glowClass: 'card-glow-cyan',
    iconStyle: { background: 'rgba(6,182,212,0.12)', border: '1px solid rgba(6,182,212,0.25)', color: '#67e8f9' },
    trendColor: 'text-cyan-400',
  },
  {
    id: 'views',
    label: 'Total Views',
    valueKey: 'totalViews',
    formatter: (v) => formatCompact(v),
    exactKey: 'totalViews',
    subtext: 'Across all analyzed videos',
    badge: 'Views Volume',
    icon: Eye,
    glowClass: 'card-glow-purple',
    iconStyle: { background: 'rgba(139,92,246,0.12)', border: '1px solid rgba(139,92,246,0.25)', color: '#c4b5fd' },
    trendColor: 'text-purple-300',
  },
  {
    id: 'likes',
    label: 'Total Likes',
    valueKey: 'totalLikes',
    formatter: (v) => formatCompact(v),
    exactKey: 'totalLikes',
    subtext: 'Positive community response',
    badge: 'Appreciation',
    icon: ThumbsUp,
    glowClass: 'card-glow-rose',
    iconStyle: { background: 'rgba(244,63,94,0.12)', border: '1px solid rgba(244,63,94,0.25)', color: '#fda4af' },
    trendColor: 'text-rose-300',
  },
  {
    id: 'engagement',
    label: 'Avg Engagement Rate',
    valueKey: 'avgEngagementRate',
    formatter: (v) => formatPercentage(v),
    subtext: '(Likes + Dislikes + Comments) / Views',
    badge: 'High Impact',
    icon: Activity,
    glowClass: 'card-glow-amber',
    iconStyle: { background: 'rgba(245,158,11,0.12)', border: '1px solid rgba(245,158,11,0.25)', color: '#fde68a' },
    trendColor: 'text-amber-300',
  },
];

export const KpiCards = ({ kpis }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 lg:gap-5 mb-6">
      {CARDS.map((card, i) => {
        const Icon = card.icon;
        const value = card.formatter(kpis[card.valueKey]);
        const exact = card.exactKey ? formatNumber(kpis[card.exactKey]) : null;

        return (
          <div
            key={card.id}
            className={`
              relative overflow-hidden rounded-2xl lg:rounded-3xl p-5 lg:p-6
              transition-all duration-300 hover:-translate-y-1.5 cursor-default
              animate-fade-up anim-delay-${i + 1}
              ${card.glowClass}
            `}
          >
            {/* Corner ambient glow */}
            <div className="absolute top-0 right-0 w-28 h-28 rounded-full blur-2xl pointer-events-none"
              style={{ background: 'rgba(255,255,255,0.025)' }} />

            {/* Icon + Badge row */}
            <div className="flex items-center justify-between mb-4">
              <div className="p-2.5 rounded-xl" style={card.iconStyle}>
                <Icon className="w-5 h-5" />
              </div>
              <span className="text-[10px] font-bold tracking-wider uppercase px-2.5 py-1 rounded-full"
                style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.08)', color: '#94a3b8' }}>
                {card.badge}
              </span>
            </div>

            {/* Label + Number */}
            <p className="text-[11px] font-semibold tracking-widest text-slate-400 uppercase mb-1.5">
              {card.label}
            </p>
            <h2
              className="text-2xl lg:text-3xl font-extrabold tracking-tight text-white font-heading leading-none"
              title={exact || value}
            >
              {value}
            </h2>

            {/* Footer divider + subtext */}
            <div className="mt-4 pt-3 flex items-center justify-between text-xs text-slate-400"
              style={{ borderTop: '1px solid rgba(255,255,255,0.06)' }}>
              <span className="truncate pr-2">{card.subtext}</span>
              <ArrowUpRight className={`w-3.5 h-3.5 shrink-0 ${card.trendColor}`} />
            </div>
          </div>
        );
      })}
    </div>
  );
};
