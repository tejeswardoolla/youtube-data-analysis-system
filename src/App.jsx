import React, { useState, useEffect, useMemo } from 'react';
import { loadYouTubeData } from './data/dataLoader';
import {
  filterData,
  calculateKPIs,
  getViewsTrend,
  getTopChannelsByViews,
  getEngagementBreakdown,
  getKeyInsights,
  getFilterOptions,
} from './utils/analytics';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { FilterBar } from './components/FilterBar';
import { KpiCards } from './components/KpiCards';
import { KeyInsights } from './components/KeyInsights';
import { OverviewTab } from './components/Tabs/OverviewTab';
import { TrendingTab } from './components/Tabs/TrendingTab';
import { ChannelsTab } from './components/Tabs/ChannelsTab';
import { EngagementTab } from './components/Tabs/EngagementTab';
import { PublishingTab } from './components/Tabs/PublishingTab';
import { Footer } from './components/Footer';
import { Sparkles, AlertCircle } from 'lucide-react';
import { YoutubeIcon } from './components/YoutubeIcon';

export function App() {
  const [rawData, setRawData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadStatus, setLoadStatus] = useState({ percent: 10, text: 'Initializing...' });
  const [error, setError] = useState(null);

  const [activeTab, setActiveTab] = useState('overview');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Filter state
  const [filters, setFilters] = useState({
    year: 'all',
    channel: 'all',
    category: 'all',
    day: 'all',
  });

  // Load CSV once on mount
  useEffect(() => {
    loadYouTubeData((percent, text) => {
      setLoadStatus({ percent, text });
    })
      .then((data) => {
        setRawData(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load dataset:', err);
        setError(err.message || 'Failed to load youtube_dashboard_data.csv');
        setLoading(false);
      });
  }, []);

  // Filter options extracted from raw data
  const filterOptions = useMemo(() => {
    return getFilterOptions(rawData);
  }, [rawData]);

  // Dynamically filter data
  const filteredData = useMemo(() => {
    return filterData(rawData, filters);
  }, [rawData, filters]);

  // Dynamic calculations based on current filtered slice
  const kpis = useMemo(() => calculateKPIs(filteredData), [filteredData]);
  const viewsTrendData = useMemo(() => getViewsTrend(filteredData), [filteredData]);
  const topChannelsData = useMemo(() => getTopChannelsByViews(filteredData, 10), [filteredData]);
  const engagementBreakdownData = useMemo(() => getEngagementBreakdown(filteredData, 7), [filteredData]);
  const keyInsights = useMemo(() => getKeyInsights(filteredData), [filteredData]);

  // Loading Screen
  if (loading) {
    return (
      <div className="min-h-screen bg-[#08090d] flex items-center justify-center p-4 relative overflow-hidden">
        {/* Glow backdrop */}
        <div className="w-96 h-96 rounded-full bg-red-600/15 blur-3xl absolute top-1/3 left-1/3 -translate-x-1/2 -translate-y-1/2" />
        <div className="w-96 h-96 rounded-full bg-amber-500/10 blur-3xl absolute bottom-1/4 right-1/4" />

        <div className="w-full max-w-md p-8 rounded-3xl glass-panel relative z-10 text-center space-y-6">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-red-600 to-amber-500 p-0.5 mx-auto shadow-xl shadow-red-600/20">
            <div className="w-full h-full bg-[#0d0f17] rounded-[14px] flex items-center justify-center">
              <YoutubeIcon className="w-8 h-8 text-red-500 animate-pulse" />
            </div>
          </div>

          <div>
            <h2 className="text-xl font-bold text-white font-heading tracking-wide">
              YT ANALYTICS
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Loading YouTube Analysis System
            </p>
          </div>

          {/* Progress bar */}
          <div className="space-y-2">
            <div className="w-full h-2 rounded-full bg-white/[0.06] overflow-hidden border border-white/[0.08]">
              <div
                className="h-full bg-gradient-to-r from-red-500 via-amber-500 to-yellow-400 transition-all duration-300 rounded-full"
                style={{ width: `${loadStatus.percent}%` }}
              />
            </div>
            <div className="flex justify-between items-center text-[11px] text-slate-400 font-mono">
              <span>{loadStatus.text}</span>
              <span>{loadStatus.percent}%</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Error Screen
  if (error) {
    return (
      <div className="min-h-screen bg-[#08090d] flex items-center justify-center p-4">
        <div className="max-w-md p-6 rounded-3xl glass-panel border-red-500/30 text-center space-y-4">
          <AlertCircle className="w-12 h-12 text-red-400 mx-auto" />
          <h2 className="text-lg font-bold text-white">Data Loading Error</h2>
          <p className="text-xs text-red-300 font-mono">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-red-600 hover:bg-red-500 text-white transition-colors"
          >
            Retry Loading
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#08090d] text-slate-100 relative selection:bg-amber-500/30 selection:text-amber-200">
      {/* Ambient background glows matching reference design */}
      <div className="fixed top-[-10%] right-[-5%] w-[680px] h-[680px] rounded-full bg-gradient-to-br from-amber-500/18 via-orange-600/10 to-transparent blur-[120px] pointer-events-none -z-10" />
      <div className="fixed bottom-[-10%] left-[-5%] w-[580px] h-[580px] rounded-full bg-gradient-to-tr from-purple-800/14 via-rose-700/8 to-transparent blur-[120px] pointer-events-none -z-10" />
      <div className="fixed top-[40%] right-[30%] w-[420px] h-[420px] rounded-full bg-red-600/5 blur-[100px] pointer-events-none -z-10" />

      {/* Sidebar */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        totalRecords={rawData.length}
        isOpen={mobileMenuOpen}
        onClose={() => setMobileMenuOpen(false)}
      />

      {/* Main Content Area */}
      <main className="lg:pl-64 min-h-screen flex flex-col justify-between transition-all duration-300">
        <div className="max-w-[1560px] mx-auto w-full p-4 sm:p-6 lg:p-8">
          {/* Top Header (rebalanced without global search) */}
          <Header
            activeTab={activeTab}
            totalRecords={rawData.length}
            onOpenMobileMenu={() => setMobileMenuOpen(true)}
          />

          {/* Interactive Filters Bar */}
          <FilterBar
            filterOptions={filterOptions}
            filters={filters}
            setFilters={setFilters}
            totalFiltered={filteredData.length}
            totalOriginal={rawData.length}
          />

          {/* 4 Reference-Styled KPI Cards */}
          <KpiCards kpis={kpis} />

          {/* Dynamic Key Insights Strip */}
          <KeyInsights insights={keyInsights} />

          {/* Active Tab View */}
          <div className="transition-all duration-300">
            {activeTab === 'overview' && (
              <OverviewTab
                viewsTrendData={viewsTrendData}
                topChannelsData={topChannelsData}
                engagementBreakdownData={engagementBreakdownData}
              />
            )}

            {activeTab === 'trending' && <TrendingTab data={filteredData} />}

            {activeTab === 'channels' && <ChannelsTab data={filteredData} />}

            {activeTab === 'engagement' && (
              <EngagementTab
                kpis={kpis}
                engagementBreakdownData={engagementBreakdownData}
                viewsTrendData={viewsTrendData}
              />
            )}

            {activeTab === 'publishing' && <PublishingTab data={filteredData} />}
          </div>

          {/* Footer */}
          <Footer />
        </div>
      </main>
    </div>
  );
}

export default App;
