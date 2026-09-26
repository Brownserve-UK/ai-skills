import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './style.css';
import { Variants } from './variants';

function App() {
  return (
    <main className="grid min-h-dvh place-items-center bg-neutral-50 p-6 text-neutral-900">
      <div className="max-w-sm text-center">
        <h1 className="text-2xl font-semibold tracking-tight">Prototype ready</h1>
        <p className="mt-2 text-sm text-neutral-600">Replace this with the first variant.</p>
      </div>
    </main>
  );
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Variants items={[{ id: 'a', label: 'A', render: () => <App /> }]} />
  </StrictMode>,
);
