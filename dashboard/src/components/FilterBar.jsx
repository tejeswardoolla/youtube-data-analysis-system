import React from 'react';
import { RotateCcw, Calendar, Tv, Tag, Clock, SlidersHorizontal } from 'lucide-react';

export const FilterBar = ({
  filterOptions,
  filters,
  setFilters,
  totalFiltered,
  totalOriginal
}) => {
  const isFiltered = 
    filters.year !== 'all' || 
    filters.channel !== 'all' || 
    filters.category !== 'all' || 
    filters.day !== 'all';

  const handleReset = () => {
    setFilters({
      year: 'all',
      channel: 'all',
      category: 'all',
      day: 'all',
    });
  };

  const selectBase = `
    appearance-none text-xs font-medium text-slate-200
    pl-8 pr-7 py-2 rounded-xl cursor-pointer
    border border-white/[0.08]
    focus:outline-none focus:border-amber-500/50
    transition-all duration-200
  `;

  const selectBg = {
    background: 'rgba(255,255,255,0.045)',
  };

  return (
    <div className="py-3.5">
      <div className="flex flex-wrap items-center justify-between gap-3 px-3 py-2.5 rounded-2xl"
        style={{
          background: 'rgba(14,16,26,0.75)',
          backdropFilter: 'blur(20px)',
          WebkitBackdropFilter: 'blur(20px)',
          border: '1px solid rgba(255,255,255,0.075)',
          boxShadow: '0 4px 24px rgba(0,0,0,0.35)',
        }}>

        {/* Left: Filters Label + Selects */}
        <div className="flex flex-wrap items-center gap-2">
          {/* Label */}
          <div className="flex items-center gap-1.5 pr-2 border-r border-white/[0.08] mr-1">
            <SlidersHorizontal className="w-3.5 h-3.5 text-slate-400" />
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider hidden sm:block">Filters</span>
          </div>

          {/* Year */}
          <div className="relative">
            <Calendar className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400 pointer-events-none z-10" />
            <select
              value={filters.year}
              onChange={(e) => setFilters((p) => ({ ...p, year: e.target.value }))}
              className={selectBase}
              style={selectBg}
            >
              <option value="all" className="bg-[#0e1018]">All Years</option>
              {filterOptions.years.map((y) => (
                <option key={y} value={y} className="bg-[#0e1018]">Year {y}</option>
              ))}
            </select>
            <span className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-500 text-[9px] pointer-events-none">▼</span>
          </div>

          {/* Channel */}
          <div className="relative">
            <Tv className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400 pointer-events-none z-10" />
            <select
              value={filters.channel}
              onChange={(e) => setFilters((p) => ({ ...p, channel: e.target.value }))}
              className={`${selectBase} max-w-[165px]`}
              style={selectBg}
            >
              <option value="all" className="bg-[#0e1018]">All Channels</option>
              {filterOptions.channels.map((ch) => (
                <option key={ch} value={ch} className="bg-[#0e1018]">{ch}</option>
              ))}
            </select>
            <span className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-500 text-[9px] pointer-events-none">▼</span>
          </div>

          {/* Category */}
          <div className="relative">
            <Tag className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400 pointer-events-none z-10" />
            <select
              value={filters.category}
              onChange={(e) => setFilters((p) => ({ ...p, category: e.target.value }))}
              className={`${selectBase} max-w-[175px]`}
              style={selectBg}
            >
              <option value="all" className="bg-[#0e1018]">All Categories</option>
              {filterOptions.categories.map((cat) => (
                <option key={cat.id} value={cat.id} className="bg-[#0e1018]">{cat.name}</option>
              ))}
            </select>
            <span className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-500 text-[9px] pointer-events-none">▼</span>
          </div>

          {/* Day */}
          <div className="relative">
            <Clock className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400 pointer-events-none z-10" />
            <select
              value={filters.day}
              onChange={(e) => setFilters((p) => ({ ...p, day: e.target.value }))}
              className={selectBase}
              style={selectBg}
            >
              <option value="all" className="bg-[#0e1018]">All Days</option>
              {filterOptions.days.map((d) => (
                <option key={d} value={d} className="bg-[#0e1018]">{d}</option>
              ))}
            </select>
            <span className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-500 text-[9px] pointer-events-none">▼</span>
          </div>
        </div>

        {/* Right: Record count + Reset */}
        <div className="flex items-center gap-3 ml-auto">
          <div className="text-[11px] text-slate-400 hidden sm:block">
            Showing{' '}
            <span className="font-semibold text-white font-mono">{totalFiltered.toLocaleString()}</span>
            {' '}of {totalOriginal.toLocaleString()} records
          </div>

          {isFiltered && (
            <button
              onClick={handleReset}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all hover:scale-105"
              style={{
                color: '#fbbf24',
                background: 'rgba(245,158,11,0.1)',
                border: '1px solid rgba(245,158,11,0.28)',
              }}
              title="Reset all filters"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reset</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
