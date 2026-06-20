import { Shield } from 'lucide-react';

export default function Header() {
  return (
    <header className="border-b border-slate-800 bg-slate-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-primary-600 flex items-center justify-center text-white font-bold">DP</div>
          <div>
            <h1 className="text-lg font-semibold leading-tight">Decision Provenance Explorer</h1>
            <p className="text-xs text-slate-400">Tamper-evident ML decision log</p>
          </div>
        </div>
        <div className="hidden md:flex items-center gap-2 text-xs text-slate-400">
          <Shield size={14} />
          <span>Pocket Network · Polygon Amoy</span>
        </div>
      </div>
    </header>
  );
}
