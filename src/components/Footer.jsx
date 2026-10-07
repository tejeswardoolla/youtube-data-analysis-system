import React from 'react';
import { YoutubeIcon } from './YoutubeIcon';

export const Footer = () => (
  <footer className="mt-12 py-6 text-center text-xs text-slate-500"
    style={{ borderTop: '1px solid rgba(255,255,255,0.06)' }}>
    <div className="flex flex-col sm:flex-row items-center justify-between gap-3 max-w-full">
      {/* Brand */}
      <div className="flex items-center gap-2">
        <div className="w-5 h-5 rounded-md flex items-center justify-center p-0.5" style={{ background: '#dc2626' }}>
          <YoutubeIcon className="w-3.5 h-3.5 text-white" />
        </div>
        <span className="font-semibold text-slate-300 text-xs">YouTube Data Analysis Dashboard</span>
      </div>

      {/* Attribution */}
      <p className="text-[11px] text-slate-500">
        Built using{' '}
        <span className="text-slate-300">React</span>{' '}•{' '}
        <span className="text-slate-300">Pandas Analysis</span>{' '}•{' '}
        <span className="text-slate-300">YouTube Dataset</span>
      </p>

      {/* Status */}
      <div className="flex items-center gap-1.5 text-[11px]">
        <span className="text-slate-500">College DAE Project</span>
        <span className="mx-1 text-slate-600">·</span>
        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block" />
        <span className="text-emerald-400 font-medium">Production Ready</span>
      </div>
    </div>
  </footer>
);
