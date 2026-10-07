import React, { useState, useMemo } from 'react';
import { Tv, Search, X, ArrowUpDown, ChevronLeft, ChevronRight } from 'lucide-react';
import { getAllChannelsPerformance } from '../../utils/analytics';
import { formatNumber, formatPercentage } from '../../utils/formatters';

const PAGE_SIZE = 15;

const SORT_FIELDS = [
  { key: 'views',              label: 'Total Views',       align: 'right' },
  { key: 'likes',              label: 'Total Likes',       align: 'right' },
  { key: 'comments',           label: 'Total Comments',    align: 'right' },
  { key: 'videos',             label: 'Videos',            align: 'right' },
  { key: 'avgEngagementRate',  label: 'Engagement Rate',   align: 'right' },
  { key: 'channel',            label: 'Channel',           align: 'left'  },
];

export const ChannelsTab = ({ data }) => {
  const [search, setSearch] = useState('');
  const [sortField, setSortField] = useState('views');
  const [sortDir, setSortDir] = useState('desc');
  const [page, setPage] = useState(1);

  const rawChannels = useMemo(() => getAllChannelsPerformance(data), [data]);

  const filtered = useMemo(() => {
    if (!search.trim()) return rawChannels;
    const q = search.toLowerCase();
    return rawChannels.filter((c) => c.channel.toLowerCase().includes(q));
  }, [rawChannels, search]);

  const sorted = useMemo(() => {
    const list = [...filtered];
    list.sort((a, b) => {
      const va = a[sortField];
      const vb = b[sortField];
      if (typeof va === 'string') {
        return sortDir === 'asc' ? va.localeCompare(vb) : vb.localeCompare(va);
      }
      return sortDir === 'asc' ? va - vb : vb - va;
    });
    return list;
  }, [filtered, sortField, sortDir]);

  const totalPages = Math.max(1, Math.ceil(sorted.length / PAGE_SIZE));
  const paged = useMemo(() => sorted.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE), [sorted, page]);

  const handleSort = (field) => {
    if (sortField === field) setSortDir((d) => (d === 'desc' ? 'asc' : 'desc'));
    else { setSortField(field); setSortDir('desc'); }
    setPage(1);
  };

  const SortTh = ({ fieldKey, children, align = 'right' }) => {
    const active = sortField === fieldKey;
    return (
      <th
        className={`py-3.5 px-4 text-[10px] font-bold uppercase tracking-wider text-slate-500 cursor-pointer select-none hover:text-slate-300 transition-colors ${align === 'right' ? 'text-right' : 'text-left'}`}
        onClick={() => handleSort(fieldKey)}
      >
        <span className={`flex items-center gap-1 ${align === 'right' ? 'justify-end' : ''}`}>
          {children}
          <ArrowUpDown className={`w-3 h-3 ${active ? 'text-amber-400' : 'text-slate-600'}`} />
        </span>
      </th>
    );
  };

  const RANK_STYLES = [
    { bg: 'rgba(245,158,11,0.15)', border: '1px solid rgba(245,158,11,0.35)', color: '#fbbf24' },
    { bg: 'rgba(148,163,184,0.12)', border: '1px solid rgba(148,163,184,0.3)', color: '#cbd5e1' },
    { bg: 'rgba(180,83,9,0.15)', border: '1px solid rgba(180,83,9,0.35)', color: '#fb923c' },
  ];

  return (
    <div className="space-y-5">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 p-3.5 rounded-2xl"
        style={{ background: 'rgba(14,16,26,0.75)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.07)' }}>
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl"
            style={{ background: 'rgba(139,92,246,0.12)', border: '1px solid rgba(139,92,246,0.25)' }}>
            <Tv className="w-4 h-4 text-purple-400" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white font-heading">Channel Leaderboard</h3>
            <p className="text-[11px] text-slate-400 mt-0.5">
              {rawChannels.length.toLocaleString()} unique creators · sorted by {sortField} ({sortDir})
            </p>
          </div>
        </div>

        {/* Search */}
        <div className="relative w-full sm:w-64">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400 pointer-events-none" />
          <input
            type="text"
            value={search}
            onChange={(e) => { setSearch(e.target.value); setPage(1); }}
            placeholder="Search channel name..."
            className="w-full pl-9 pr-8 py-2 text-xs text-slate-100 placeholder:text-slate-500 rounded-xl focus:outline-none transition-all"
            style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.09)' }}
          />
          {search && (
            <button onClick={() => { setSearch(''); setPage(1); }}
              className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white transition-colors">
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      </div>

      {/* Table */}
      <div className="rounded-3xl overflow-hidden"
        style={{ background: 'rgba(12,14,22,0.8)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.07)' }}>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr style={{ background: 'rgba(255,255,255,0.025)', borderBottom: '1px solid rgba(255,255,255,0.07)' }}>
                <th className="py-3.5 px-4 w-16 text-center text-[10px] font-bold uppercase tracking-wider text-slate-500">Rank</th>
                <SortTh fieldKey="channel" align="left">Channel</SortTh>
                <SortTh fieldKey="videos">Videos</SortTh>
                <SortTh fieldKey="views">Total Views</SortTh>
                <SortTh fieldKey="likes">Total Likes</SortTh>
                <SortTh fieldKey="comments">Total Comments</SortTh>
                <SortTh fieldKey="avgEngagementRate">Engagement Rate</SortTh>
              </tr>
            </thead>
            <tbody>
              {paged.length > 0 ? paged.map((ch, idx) => {
                const rank = (page - 1) * PAGE_SIZE + idx + 1;
                const rs = RANK_STYLES[rank - 1] || null;
                return (
                  <tr key={ch.channel}
                    style={{ borderBottom: '1px solid rgba(255,255,255,0.04)' }}
                    onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.03)'}
                    onMouseLeave={(e) => e.currentTarget.style.background = ''}
                    className="transition-colors group"
                  >
                    <td className="py-3 px-4 text-center">
                      <span className="inline-flex items-center justify-center w-7 h-7 rounded-xl text-xs font-bold font-mono"
                        style={rs ? { background: rs.bg, border: rs.border, color: rs.color }
                          : { background: 'rgba(255,255,255,0.03)', color: '#64748b' }}>
                        {rank}
                      </span>
                    </td>

                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2.5">
                        <div className="w-7 h-7 rounded-lg flex items-center justify-center font-bold text-xs text-purple-300 shrink-0"
                          style={{ background: 'rgba(139,92,246,0.12)', border: '1px solid rgba(139,92,246,0.2)' }}>
                          {ch.channel.charAt(0).toUpperCase()}
                        </div>
                        <span className="font-semibold text-slate-200 group-hover:text-white transition-colors">{ch.channel}</span>
                      </div>
                    </td>

                    <td className="py-3 px-4 text-right font-mono text-slate-300">{formatNumber(ch.videos)}</td>
                    <td className="py-3 px-4 text-right font-mono font-bold text-amber-300">{formatNumber(ch.views)}</td>
                    <td className="py-3 px-4 text-right font-mono text-rose-300">{formatNumber(ch.likes)}</td>
                    <td className="py-3 px-4 text-right font-mono text-sky-300">{formatNumber(ch.comments)}</td>
                    <td className="py-3 px-4 text-right">
                      <span className="inline-block px-2 py-0.5 rounded-md font-mono text-[11px] font-semibold"
                        style={{ background: 'rgba(16,185,129,0.1)', border: '1px solid rgba(16,185,129,0.2)', color: '#6ee7b7' }}>
                        {formatPercentage(ch.avgEngagementRate)}
                      </span>
                    </td>
                  </tr>
                );
              }) : (
                <tr>
                  <td colSpan="7" className="py-12 text-center text-slate-500 text-sm">
                    No channels found{search ? ` matching "${search}"` : ''}.
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
            {' '}–{' '}<span className="font-semibold text-slate-200">{Math.min(page * PAGE_SIZE, sorted.length)}</span>
            {' '}of <span className="font-semibold text-slate-200">{sorted.length}</span> channels
          </span>
          <div className="flex items-center gap-1.5">
            <button onClick={() => setPage((p) => Math.max(1, p - 1))} disabled={page === 1}
              className="p-1.5 rounded-lg disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
              style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.08)' }}>
              <ChevronLeft className="w-4 h-4 text-slate-300" />
            </button>
            <span className="text-xs font-mono text-slate-300 px-2">{page} / {totalPages}</span>
            <button onClick={() => setPage((p) => Math.min(totalPages, p + 1))} disabled={page === totalPages}
              className="p-1.5 rounded-lg disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
              style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.08)' }}>
              <ChevronRight className="w-4 h-4 text-slate-300" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
