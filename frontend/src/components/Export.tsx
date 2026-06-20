import { useState } from 'react';
import { FileDown, Loader2 } from 'lucide-react';

export default function ExportPanel() {
  const [loading, setLoading] = useState(false);

  const handleExport = async () => {
    setLoading(true);
    try {
      const base = (import.meta.env.VITE_API_BASE_URL ?? '').replace(/\/$/, '');
      const res = await fetch(`${base}/records/export/eu_ai_act`);
      if (!res.ok) throw new Error('Export failed');
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'provenance_export_eu_ai_act_report.json';
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
        Download an EU AI Act Article 13 compliance report from the backend.
      </p>

      <div className="rounded-lg border border-slate-800 bg-slate-900/50 p-6">
        <div className="flex flex-wrap items-center gap-4">
          <button
            onClick={handleExport}
            disabled={loading}
            className="inline-flex items-center gap-2 px-4 py-2 text-sm bg-primary-600 hover:bg-primary-700 disabled:opacity-50 rounded"
          >
            {loading ? <Loader2 size={16} className="animate-spin" /> : <FileDown size={16} />}
            Download EU AI Act Report
          </button>
        </div>

        <p className="mt-4 text-xs text-slate-400">
          Requires backend at <code className="text-primary-400">{import.meta.env.VITE_API_BASE_URL}</code>
        </p>
      </div>
    </div>
  );
}
