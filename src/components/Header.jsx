import React from 'react';
import { Bell, Menu, Sparkles, Database, CheckCircle2 } from 'lucide-react';
import { formatNumber } from '../utils/formatters';

const TITLE_MAP = {
  overview: { title: 'Overview', subtitle: 'YouTube Data Analysis & Performance Insights' },
  trending: { title: 'Trending Videos', subtitle: 'Top performing content by Views, Likes & Comments' },
  channels: { title: 'Channel Performance', subtitle: 'Aggregated analytics across YouTube creators' },
  engagement: { title: 'Engagement Analysis', subtitle: 'Audience interaction ratios & community response' },
  publishing: { title: 'Publishing Insights', subtitle: 'Upload frequency and distribution by Day, Month & Hour' },
};

export const Header = ({ 
  activeTab, 
  totalRecords = 33089,
  onOpenMobileMenu 
}) => {
  const current = TITLE_MAP[activeTab] || TITLE_MAP.overview;

  return (
    <header className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-white/[0.06]">
      {/* Left Title, Subtitle & Status Badge */}
      <div className="flex items-center gap-3.5">
        <button 
          onClick={onOpenMobileMenu}
          className="lg:hidden p-2 rounded-xl bg-white/[0.05] border border-white/10 text-slate-300 hover:text-white"
          aria-label="Open Navigation Menu"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl lg:text-3xl font-bold tracking-tight text-white font-heading">
              {current.title}
            </h1>
            <span className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-red-500/10 text-red-400 border border-red-500/20 shadow-sm">
              <span className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse" />
              Live Dataset
            </span>
          </div>
          <p className="text-xs lg:text-sm text-slate-400 mt-1">
            {current.subtitle}
          </p>
        </div>
      </div>

      {/* Right Controls Group (Rebalanced without global search) */}
      <div className="flex items-center gap-3 self-end sm:self-auto">
        {/* Dataset Verification Capsule */}
        <div className="hidden md:flex items-center gap-2.5 px-3.5 py-2 rounded-2xl bg-[#12141f]/80 backdrop-blur-md border border-white/[0.08] shadow-sm">
          <Database className="w-3.5 h-3.5 text-amber-400" />
          <span className="text-xs font-medium text-slate-300">
            <span className="font-semibold text-white font-mono">{formatNumber(totalRecords)}</span> Records Analyzed
          </span>
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
        </div>

        {/* System Notification Icon */}
        <button 
          className="relative p-2.5 rounded-2xl bg-[#12141f]/80 backdrop-blur-md border border-white/[0.08] text-slate-300 hover:text-white hover:bg-white/[0.08] transition-all hover:scale-105"
          title="System Notifications: Dataset Connected"
        >
          <Bell className="w-4 h-4" />
          <span className="absolute top-2 right-2 w-2 h-2 rounded-full bg-red-500 ring-2 ring-[#08090d]" />
        </button>

        {/* Profile Avatar circle matching the reference top right */}
        <div className="flex items-center gap-2.5 pl-1">
          <div className="w-9 h-9 rounded-2xl bg-gradient-to-tr from-amber-500 via-orange-500 to-rose-500 p-0.5 shadow-md shadow-orange-500/20 cursor-pointer hover:scale-105 transition-transform">
            <div className="w-full h-full bg-[#0d0f17] rounded-[14px] flex items-center justify-center font-bold text-xs text-amber-400">
              DA
            </div>
          </div>
          <div className="hidden xl:block text-left text-xs">
            <p className="font-semibold text-white leading-tight">DAE Project</p>
            <p className="text-[10px] text-slate-400">Analyst View</p>
          </div>
        </div>
      </div>
    </header>
  );
};
