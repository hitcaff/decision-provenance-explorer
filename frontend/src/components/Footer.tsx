export default function Footer() {
  return (
    <footer className="border-t border-slate-800 bg-slate-900/60 py-4">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-slate-500">
        <span>Contract: 0x31e8…1fb3 on Polygon Amoy</span>
        <a
          href="https://amoy.polygonscan.com/tx/27c82e2e48cc320b54bb0961dd8926234208eb58c2418c79dd88ca72c4363e12"
          target="_blank"
          rel="noreferrer"
          className="text-primary-500 hover:underline"
        >
          Verified Anchor
        </a>
      </div>
    </footer>
  );
}
