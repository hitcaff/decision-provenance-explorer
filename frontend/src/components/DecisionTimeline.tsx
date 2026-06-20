import { useQuery } from '@tanstack/react-query';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { fetchRecords } from '../api';

export default function DecisionTimeline() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['records'],
    queryFn: fetchRecords,
  });

  const records = data?.data ?? [];

  const chartData = records.map((r: any, idx: number) => ({
    index: idx + 1,
    score: Number(r.score ?? 0),
    label: r.label_display,
  }));

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <h2 className="text-2xl font-semibold mb-6">Decision Timeline</h2>

      {isLoading && <p className="text-slate-400">Loading…</p>}
      {error && <p className="text-red-400">Failed to load timeline</p>}

      {records.length > 0 ? (
        <div className="rounded-lg border border-slate-800 bg-slate-900/50 p-4">
          <ResponsiveContainer width="100%" height={320}>
            <LineChart data={chartData}>
              <XAxis dataKey="index" stroke="#94a3b8" />
              <YAxis domain={[0, 1]} stroke="#94a3b8" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0f172a',
                  border: '1px solid #1e293b',
                  borderRadius: '8px',
                  color: '#f8fafc',
                }}
              />
              <Line type="monotone" dataKey="score" stroke="#0ea5e9" strokeWidth={2} dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <p className="text-slate-400">No timeline data available.</p>
      )}
    </div>
  );
}
