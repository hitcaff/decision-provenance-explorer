import { useQuery } from '@tanstack/react-query';
import { User } from 'lucide-react';
import { fetchConfigHistory } from '../api';

export default function ConfigHistory() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['configHistory'],
    queryFn: fetchConfigHistory,
  });

  const items = data ?? [];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <h2 className="text-2xl font-semibold mb-6">Config History</h2>
      {isLoading && <p className="text-slate-400">Loading…</p>}
      {error && <p className="text-red-400">Failed to load config history</p>}

      <div className="space-y-3">
        {items.length === 0 && <p className="text-slate-400">No config changes recorded.</p>}
        {items.map((c: any, idx: number) => (
          <div key={c.config_id ?? idx} className="rounded-lg border border-slate-800 bg-slate-900/50 p-4">
            <div className="flex flex-wrap items-center gap-3 mb-2">
              <span className="px-2 py-1 text-xs bg-slate-800 border border-slate-700 rounded font-mono">
                v{c.config_version ?? idx + 1}
              </span>
              <span className="text-sm font-medium">
                threshold {Number(c.threshold ?? 0).toFixed(2)}
              </span>
              <span className="text-xs text-slate-400">
                label: {c.threshold_label_id ?? '—'}
              </span>
            </div>
            <div className="flex items-center gap-2 text-xs text-slate-400">
              <User size={12} />
              <span>{c.changed_by ?? '—'}</span>
            </div>
            {c.change_reason && (
              <p className="mt-1 text-xs text-slate-400">{c.change_reason}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
