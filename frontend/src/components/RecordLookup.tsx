import { useQuery } from '@tanstack/react-query';
import { Shield } from 'lucide-react';
import { fetchRecords } from '../api';

export default function RecordLookup() {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['records'],
    queryFn: fetchRecords,
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-semibold">Record Lookup</h2>
          <p className="text-slate-400 text-sm">Inspect tamper-evident provenance records</p>
        </div>
        <button
          onClick={() => refetch()}
          className="px-3 py-2 text-sm bg-slate-800 border border-slate-700 rounded hover:bg-slate-700"
        >
          Refresh
        </button>
      </div>

      {isLoading && <p className="text-slate-400">Loading records…</p>}
      {error && <p className="text-red-400">Failed to load records</p>}

      {data && (
        <div className="space-y-4">
          {data.records.length === 0 ? (
            <div className="rounded-lg border border-slate-800 bg-slate-900/50 p-6 text-center text-slate-400">
              <Shield className="mx-auto mb-2" size={24} />
              No records yet. Anchor a chain to see records here.
            </div>
          ) : (
            data.records.map((r: any) => (
              <div key={r.id} className="rounded-lg border border-slate-800 bg-slate-900/50 p-4">
                <div className="flex flex-wrap items-center gap-2 mb-2">
                  <span className="px-2 py-1 text-xs font-mono bg-slate-800 border border-slate-700 rounded">
                    {r.id?.slice(0, 8) ?? '—'}
                  </span>
                  <span className="px-2 py-1 text-xs bg-primary-500/20 text-primary-300 border border-primary-500/30 rounded">
                    {r.label_display ?? '—'}
                  </span>
                  <span className="text-sm text-slate-400">score {r.score?.toFixed(2) ?? '—'}</span>
                </div>
                <pre className="text-xs text-slate-300 bg-slate-950/60 p-3 rounded overflow-auto">
                  {JSON.stringify({ input_features: r.input_features, output: r.output }, null, 2)}
                </pre>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
