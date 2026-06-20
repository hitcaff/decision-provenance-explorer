import { useState } from 'react';
import { GitCompare } from 'lucide-react';

export default function DiffTool() {
  const [a, setA] = useState('');
  const [b, setB] = useState('');

  const same = a && b && a === b;
  const both = a && b;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <div className="mb-6">
        <h2 className="text-2xl font-semibold">Diff Tool</h2>
        <p className="text-slate-400 text-sm">Compare two record IDs or chain roots</p>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <div>
          <label className="block text-xs text-slate-400 mb-1">Record A</label>
          <textarea
            value={a}
            onChange={(e) => setA(e.target.value)}
            className="w-full h-40 p-3 bg-slate-900 border border-slate-800 rounded text-sm font-mono"
            placeholder="Paste record ID or hash"
          />
        </div>
        <div>
          <label className="block text-xs text-slate-400 mb-1">Record B</label>
          <textarea
            value={b}
            onChange={(e) => setB(e.target.value)}
            className="w-full h-40 p-3 bg-slate-900 border border-slate-800 rounded text-sm font-mono"
            placeholder="Paste record ID or hash"
          />
        </div>
      </div>

      {both && (
        <div className="mt-4 rounded-lg border border-slate-800 bg-slate-900/50 p-4">
          <div className="flex items-center gap-2">
            <GitCompare size={16} />
            <span className="text-sm font-medium">
              {same ? 'Exact match' : 'Values differ'}
            </span>
          </div>
          <p className="mt-2 text-xs text-slate-400">
            {same
              ? 'Both IDs point to the same record state.'
              : 'Use the verification portal to independently check each record.'}
          </p>
        </div>
      )}
    </div>
  );
}
