import React, { useState, useMemo } from 'react';
import { Eye, ThumbsUp, MessageSquare, ChevronLeft, ChevronRight, Play, Search, X } from 'lucide-react';
import { getTrendingVideos } from '../../utils/analytics';
import { formatNumber, formatPercentage } from '../../utils/formatters';

const SORT_TABS = [
  { key: 'views',    label: 'Most Viewed',    icon: Eye,           accent: '#f59e0b' },
  { key: 'likes',    label: 'Most Liked',     icon: ThumbsUp,      accent: '#f43f5e' },
  { key: 'comments', label: 'Most Commented', icon: MessageSquare, accent: '#a855f7' },
];

const RANK_STYLES = [
  { bg: 'rgba(245,158,11,0.15)', border: '1px solid rgba(245,158,11,0.35)', color: '#fbbf24' }, // Gold
  { bg: 'rgba(148,163,184,0.12)', border: '1px solid rgba(148,163,184,0.3)', color: '#cbd5e1' }, // Silver
  { bg: 'rgba(180,83,9,0.15)',  border: '1px solid rgba(180,83,9,0.35)',  color: '#fb923c' }, // Bronze
];

const PAGE_SIZE = 15;

export const TrendingTab = ({ data }) => {
  const [activeSort, setActiveSort] = useState('views');
  const [page, setPage] = useState(1);
  const [searchQuery, setSearchQuery] = useState('');

  const allVideos = useMemo(() => getTrendingVideos(data, activeSort, 200), [data, activeSort]);

  const filtered = useMemo(() => {
    if (!searchQuery.trim()) return allVideos;
    const q = searchQuery.toLowerCase();
    return allVideos.filter(
      (v) => v.title.toLowerCase().includes(q) || v.channel_title.toLowerCase().includes(q)
    );
  }, [allVideos, searchQuery]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const paged = useMemo(() => filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE), [filtered, page]);

  const handleSortChange = (key) => { setActiveSort(key); setPage(1); };
  const handleSearch = (v) => { setSearchQuery(v); setPage(1); };

  return (
    <div className="space-y-5">
      {/* Controls */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 p-3 rounded-2xl"
        style={{ background: 'rgba(14,16,26,0.75)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.07)' }}>

        {/* Sort tabs */}
        <div className="flex items-center gap-1 p-1 rounded-xl" style={{ background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.07)' }}>
          {SORT_TABS.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeSort === tab.key;
            return (
              <button
                key={tab.key}
                onClick={() => handleSortChange(tab.key)}
                className="flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs font-semibold transition-all duration-200"
                style={isActive ? {
                  background: `${tab.accent}20`,
                  border: `1px solid ${tab.accent}40`,
                  color: tab.accent,
                  boxShadow: `0 2px 12px ${tab.accent}20`,
                } : {
                  color: '#64748b',
                  border: '1px solid transparent',
                }}
              >
                <Icon className="w-3.5 h-3.5" />
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Search */}
        <div className="relative w-full sm:w-60">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400 pointer-events-none" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => handleSearch(e.target.value)}
            placeholder="Filter trending list..."
            className="w-full pl-9 pr-8 py-2 text-xs text-slate-100 placeholder:text-slate-500 rounded-xl
              focus:outline-none transition-all"
            style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.09)' }}
          />
          {searchQuery && (
            <button onClick={() => handleSearch('')} className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white transition-colors">
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      </div>

      {/* Table */}
      <div className="rounded-3xl overflow-hidden" style={{ background: 'rgba(12,14,22,0.8)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.07)' }}>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr style={{ background: 'rgba(255,255,255,0.025)', borderBottom: '1px solid rgba(255,255,255,0.07)' }}>
                <th className="py-3.5 px-4 w-14 text-center text-[10px] font-bold uppercase tracking-wider text-slate-500">Rank</th>
                <th className="py-3.5 px-4 text-[10px] font-bold uppercase tracking-wider text-slate-500 min-w-[300px]">Video Title</th>
                <th className="py-3.5 px-4 text-[10px] font-bold uppercase tracking-wider text-slate-500 min-w-[150px]">Channel</th>
                <th className="py-3.5 px-4 text-right text-[10px] font-bold uppercase tracking-wider text-slate-500">Views</th>
                <th className="py-3.5 px-4 text-right text-[10px] font-bold uppercase tracking-wider text-slate-500">Likes</th>
                <th className="py-3.5 px-4 text-right text-[10px] font-bold uppercase tracking-wider text-slate-500">Comments</th>
                <th className="py-3.5 px-4 text-right text-[10px] font-bold uppercase tracking-wider text-slate-500">Engagement</th>
              </tr>
            </thead>
            <tbody>
              {paged.length > 0 ? paged.map((video, idx) => {
                const rank = (page - 1) * PAGE_SIZE + idx + 1;
                const rankStyle = RANK_STYLES[rank - 1] || null;
                return (
                  <tr
                    key={video.video_id + idx}
                    className="transition-colors group"
                    style={{ borderBottom: '1px solid rgba(255,255,255,0.04)' }}
                    onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.03)'}
                    onMouseLeave={(e) => e.currentTarget.style.background = ''}
                  >
                    <td className="py-3 px-4 text-center">
                      <span className="inline-flex items-center justify-center w-7 h-7 rounded-xl text-xs font-bold font-mono"
                        style={rankStyle ? { background: rankStyle.bg, border: rankStyle.border, color: rankStyle.color }
                          : { background: 'rgba(255,255,255,0.03)', color: '#64748b' }}>
                        {rank}
                      </span>
                    </td>

                    <td className="py-3 px-4">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-lg shrink-0 flex items-center justify-center transition-colors"
                          style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.2)' }}>
                          <Play className="w-3.5 h-3.5 text-red-400 fill-red-400" />
                        </div>
                        <div className="overflow-hidden">
                          <p className="font-semibold text-slate-200 truncate max-w-xs group-hover:text-white transition-colors"
                            title={video.title}>
                            {video.title}
                          </p>
                          <p className="text-[10px] text-slate-500 mt-0.5">{video.category} · {video.publish_day}</p>
                        </div>
                      </div>
                    </td>

                    <td className="py-3 px-4">
                      <span className="font-medium text-slate-300 truncate max-w-[140px] inline-block group-hover:text-white transition-colors"
                        title={video.channel_title}>
                        {video.channel_title}
                      </span>
                    </td>

                    <td className="py-3 px-4 text-right font-mono font-bold text-white">
                      {formatNumber(video.views)}
                    </td>
                    <td className="py-3 px-4 text-right font-mono text-rose-300">
                      {formatNumber(video.likes)}
                    </td>
                    <td className="py-3 px-4 text-right font-mono text-sky-300">
                      {formatNumber(video.comment_count)}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <span className="inline-block px-2 py-0.5 rounded-md font-mono text-[11px] font-semibold"
                        style={{ background: 'rgba(16,185,129,0.1)', border: '1px solid rgba(16,185,129,0.2)', color: '#6ee7b7' }}>
                        {formatPercentage(video.engagement_rate)}
                      </span>
                    </td>
                  </tr>
                );
              }) : (
                <tr>
                  <td colSpan="7" className="py-12 text-center text-slate-500 text-sm">
                    No videos match your filter.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="flex items-center justify-between px-5 py-3.5"
          style={{ borderTop: '1px solid rgba(255,255,255,0.06)', background: 'rgba(255,255,255,0.01)' }}>
          <span className="text-[11px] text-slate-400">
            Showing{' '}<span className="font-semibold text-slate-200">{(page - 1) * PAGE_SIZE + 1}</span>
            {' '}–{' '}<span className="font-semibold text-slate-200">{Math.min(page * PAGE_SIZE, filtered.length)}</span>
            {' '}of <span className="font-semibold text-slate-200">{filtered.length}</span> videos
          </span>
          <div className="flex items-center gap-1.5">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
              className="p-1.5 rounded-lg transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
              style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.08)' }}
            >
              <ChevronLeft className="w-4 h-4 text-slate-300" />
            </button>
            <span className="text-xs text-slate-300 px-2 font-mono">{page} / {totalPages}</span>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="p-1.5 rounded-lg transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
              style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.08)' }}
            >
              <ChevronRight className="w-4 h-4 text-slate-300" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
