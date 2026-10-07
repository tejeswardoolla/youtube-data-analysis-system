import React from 'react';
import { 
  LayoutDashboard, 
  Flame, 
  Tv, 
  HeartHandshake, 
  CalendarClock,
  Database,
  X
} from 'lucide-react';
import { YoutubeIcon } from './YoutubeIcon';
import { formatNumber } from '../utils/formatters';

const NAV_ITEMS = [
  { id: 'overview',   label: 'Overview',        icon: LayoutDashboard },
  { id: 'trending',   label: 'Trending Videos', icon: Flame },
  { id: 'channels',   label: 'Channels',         icon: Tv },
  { id: 'engagement', label: 'Engagement',       icon: HeartHandshake },
  { id: 'publishing', label: 'Publishing',       icon: CalendarClock },
];

export const Sidebar = ({ 
  activeTab, 
  setActiveTab, 
  totalRecords = 33089,
  isOpen = false,
  onClose
}) => {
  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black/75 backdrop-blur-sm lg:hidden"
          onClick={onClose}
        />
      )}

      <aside className={`
        fixed top-0 bottom-0 left-0 z-50 w-64
        flex flex-col justify-between
        transition-transform duration-300 ease-out
        lg:translate-x-0 ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `} style={{
        background: 'rgba(11, 13, 20, 0.96)',
        backdropFilter: 'blur(28px)',
        WebkitBackdropFilter: 'blur(28px)',
        borderRight: '1px solid rgba(255,255,255,0.07)',
        boxShadow: '4px 0 32px rgba(0,0,0,0.5)',
      }}>

        {/* Top Brand Header */}
        <div className="flex-1 overflow-y-auto overflow-x-hidden p-5">
          {/* Brand Row */}
          <div className="flex items-center justify-between pb-5 mb-4 border-b border-white/[0.06]">
            <div className="flex items-center gap-3">
              {/* YT Icon with gradient ring */}
              <div className="relative w-10 h-10 rounded-xl shrink-0">
                <div className="absolute inset-0 rounded-xl bg-gradient-to-tr from-red-600 via-rose-500 to-amber-500 opacity-90" />
                <div className="absolute inset-[2px] rounded-[10px] bg-[#0b0d14] flex items-center justify-center">
                  <YoutubeIcon className="w-5 h-5 text-red-500" />
                </div>
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-heading font-extrabold text-[15px] tracking-widest text-white uppercase">
                    YT Analytics
                  </span>
                  <span className="w-1.5 h-1.5 rounded-full bg-red-500 shadow-[0_0_8px_#ef4444] animate-pulse" />
                </div>
                <p className="text-[10px] text-slate-400 font-medium tracking-wide mt-0.5">
                  Data Analysis System
                </p>
              </div>
            </div>

            {/* Mobile close button */}
            <button 
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/[0.06] lg:hidden transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Navigation Section */}
          <div className="space-y-0.5">
            <p className="px-3 pb-2.5 text-[10px] font-bold uppercase tracking-[0.14em] text-slate-500">
              Analytics Menu
            </p>
            {NAV_ITEMS.map((item, index) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveTab(item.id);
                    if (onClose) onClose();
                  }}
                  className={`
                    w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium
                    transition-all duration-200 group relative
                    ${isActive 
                      ? 'text-white' 
                      : 'text-slate-400 hover:text-slate-100 hover:bg-white/[0.04]'
                    }
                  `}
                  style={isActive ? {
                    background: 'linear-gradient(90deg, rgba(239,68,68,0.18) 0%, rgba(234,88,12,0.10) 60%, transparent 100%)',
                    borderLeft: '2px solid #ef4444',
                    boxShadow: '0 2px 14px rgba(239,68,68,0.1)',
                  } : {
                    borderLeft: '2px solid transparent',
                  }}
                >
                  <Icon className={`w-4 h-4 shrink-0 transition-all duration-200 group-hover:scale-110 ${isActive ? 'text-red-400' : 'text-slate-400 group-hover:text-slate-300'}`} />
                  <span className="text-[13px]">{item.label}</span>
                  {isActive && (
                    <span className="ml-auto w-1.5 h-1.5 rounded-full bg-red-400 shadow-[0_0_8px_#f87171]" />
                  )}
                </button>
              );
            })}
          </div>
        </div>

        {/* Bottom Dataset Info Badge */}
        <div className="p-4 border-t border-white/[0.06]">
          <div className="p-3.5 rounded-2xl" style={{
            background: 'linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%)',
            border: '1px solid rgba(255,255,255,0.07)',
          }}>
            <div className="flex items-center gap-2 mb-2">
              <Database className="w-3.5 h-3.5 text-amber-400 shrink-0" />
              <span className="text-xs font-semibold text-slate-200 truncate">YouTube Data Analysis</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-[11px] text-slate-400">Cleaned Dataset</span>
              <span className="font-mono font-semibold text-[11px] text-amber-400 px-2 py-0.5 rounded-full"
                style={{ background: 'rgba(245,158,11,0.1)', border: '1px solid rgba(245,158,11,0.2)' }}>
                {formatNumber(totalRecords)} Records
              </span>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};
