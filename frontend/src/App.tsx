import { lazy, Suspense } from 'react';
import { Routes, Route, NavLink } from 'react-router-dom';
import { Activity, Shield, Workflow, GitCompare, FileDown, Search } from 'lucide-react';
import Header from './components/Header';
import Footer from './components/Footer';

const RecordLookup = lazy(() => import('./components/RecordLookup'));
const AnchorFeed = lazy(() => import('./components/AnchorFeed'));
const DecisionTimeline = lazy(() => import('./components/DecisionTimeline'));
const ConfigHistory = lazy(() => import('./components/ConfigHistory'));
const DiffTool = lazy(() => import('./components/DiffTool'));
const ExportPanel = lazy(() => import('./components/Export'));

function Loading() {
  return <div className="p-6 text-slate-400">Loading…</div>;
}

export default function App() {
  const links = [
    { to: '/records', label: 'Record Lookup', Icon: Search },
    { to: '/anchors', label: 'Anchor Feed', Icon: Activity },
    { to: '/timeline', label: 'Decision Timeline', Icon: Shield },
    { to: '/config', label: 'Config History', Icon: Workflow },
    { to: '/diff', label: 'Diff Tool', Icon: GitCompare },
    { to: '/export', label: 'Export', Icon: FileDown },
  ];

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <nav className="border-b border-slate-800 bg-slate-900/60 backdrop-blur">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 flex gap-1 overflow-x-auto">
          {links.map(({ to, label, Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-2 px-3 py-3 text-sm border-b-2 transition-colors whitespace-nowrap ${
                  isActive
                    ? 'border-primary-500 text-primary-500'
                    : 'border-transparent text-slate-400 hover:text-slate-200'
                }`}
            >
              <Icon size={16} />
              {label}
            </NavLink>
          ))}
        </div>
      </nav>
      <main className="flex-1">
        <Suspense fallback={<Loading />}>
          <Routes>
            <Route path="/" element={<RecordLookup />} />
            <Route path="/records" element={<RecordLookup />} />
            <Route path="/anchors" element={<AnchorFeed />} />
            <Route path="/timeline" element={<DecisionTimeline />} />
            <Route path="/config" element={<ConfigHistory />} />
            <Route path="/diff" element={<DiffTool />} />
            <Route path="/export" element={<ExportPanel />} />
          </Routes>
        </Suspense>
      </main>
      <Footer />
    </div>
  );
}
