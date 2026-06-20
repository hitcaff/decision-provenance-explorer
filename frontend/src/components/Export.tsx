import { useState } from 'react';
import { FileDown, Loader2 } from 'lucide-react';

export default function ExportPanel() {
  const [format, setFormat] = useState<'jsonl' | 'eu_ai_act'>('jsonl');
  const [loading, setLoading] = useState(false);

  const handleExport = async () => {
    setLoading(true);
    try {
      const base = import.meta.env.VITE_API_BASE_URL ?? '';
      const res = await fetch(`${base}/export/${format}`);
      if (!res.ok) throw new Error('Export failed');
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `provenance_export_${format === 'eu_ai_act' ? 'report' : 'audit'}.${format === 'eu_ai_act' ? 'json' : 'jsonl'}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch {
      alert('Failed to export. Ensure backend is reachable.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <h2 className="text-2xl font-semibold mb-2">Export</h2>
      <p className="text-slate-400 text-sm mb-6">
        Download audit logs and compliance reports from the backend.
      </p>

      <div className="rounded-lg border border-slate-800 bg-slate-900/50 p-6">
        <div className="flex flex-wrap items-center gap-4">
          <select
            value={format}
            onChange={(e) => setFormat(e.target.value as 'jsonl' | 'eu_ai_act')}
            className="bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm"
          >
            <option value="jsonl">JSONL Audit Log</option>
            <option value="eu_ai_act">EU AI Act Compliance Report</option>
          </select>

          <button
            onClick={handleExport}
            disabled={loading}
            className="inline-flex items-center gap-2 px-4 py-2 text-sm bg-primary-600 hover:bg-primary-700 disabled:opacity-50 rounded"
          >
            {loading ? <Loader2 size={16} className="animate-spin" /> : <FileDown size={16} />}
            Download Export
          </button>
        </div>

        <p className="mt-4 text-xs text-slate-400">
          Requires backend at <code className="text-primary-400">{import.meta.env.VITE_API_BASE_URL}</code>
        </p>
      </div>
    </div>
  );
}
