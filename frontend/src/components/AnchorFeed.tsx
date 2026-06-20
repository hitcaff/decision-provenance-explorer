import { useQuery } from '@tanstack/react-query';
import { Activity } from 'lucide-react';
import { fetchAnchors } from '../api';
import { formatDistanceToNow } from '../utils/time';

export default function AnchorFeed() {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['anchors'],
    queryFn: fetchAnchors,
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-semibold">Anchor Feed</h2>
          <p className="text-slate-400 text-sm">Live on-chain anchor events</p>
        </div>
        <button
          onClick={() => refetch()}
          className="px-3 py-2 text-sm bg-slate-800 border border-slate-700 rounded hover:bg-slate-700"
        >
          Refresh
        </button>
      </div>

      {isLoading && <p className="text-slate-400">Loading anchors…</p>}
      {error && <p className="text-red-400">Failed to load anchors</p>}

      {data && (
        <div className="space-y-3">
          {(!data.anchors || data.anchors.length === 0) ? (
            <div className="rounded-lg border border-slate-800 bg-slate-900/50 p-6 text-center text-slate-400">
              <Activity className="mx-auto mb-2" size={24} />
              No anchors yet.
            </div>
          ) : (
            data.anchors.map((a: any) => (
              <div key={a.tx_hash} className="rounded-lg border border-slate-800 bg-slate-900/50 p-4">
                <div className="flex flex-wrap items-center gap-2 mb-2">
                  <a
                    href={`https://amoy.polygonscan.com/tx/${a.tx_hash}`}
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs font-mono text-primary-400 hover:underline"
                  >
                    {a.tx_hash?.slice(0, 10)}…
                  </a>
                  <span className="text-xs text-slate-400">Block {a.block_number ?? '—'}</span>
                  <span className="text-xs text-slate-400">
                    {a.anchored_at ? formatDistanceToNow(a.anchored_at) : ''}
                  </span>
                </div>
                <pre className="text-xs text-slate-300 bg-slate-950/60 p-3 rounded overflow-auto">
                  {JSON.stringify({ model: a.model_id, records: a.record_count, root: a.chain_root?.slice(0, 32) }, null, 2)}
                </pre>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
