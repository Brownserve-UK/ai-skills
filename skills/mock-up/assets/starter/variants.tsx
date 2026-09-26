import { useState, type ReactNode } from 'react';
import clsx from 'clsx';

export type Variant = {
  id: string;
  label: string;
  render: () => ReactNode;
};

function initialId(items: Variant[]) {
  const requested = new URLSearchParams(window.location.search).get('v');
  const match = items.find((item) => item.id === requested);
  return (match ?? items[0])?.id;
}

export function Variants({ items }: { items: Variant[] }) {
  const [id, setId] = useState(() => initialId(items));
  const current = items.find((item) => item.id === id) ?? items[0];

  if (!current) return null;

  const select = (next: string) => {
    const url = new URL(window.location.href);
    url.searchParams.set('v', next);
    window.history.replaceState(null, '', url);
    setId(next);
  };

  return (
    <>
      {current.render()}
      {items.length > 1 && (
        <nav
          aria-label="Design variants"
          className="fixed right-3 bottom-3 z-[9999] flex gap-1 rounded-full border border-black/10 bg-white/90 p-1 font-sans text-xs font-medium text-neutral-700 opacity-60 shadow-lg backdrop-blur transition-opacity focus-within:opacity-100 hover:opacity-100"
        >
          {items.map((item) => (
            <button
              key={item.id}
              type="button"
              aria-pressed={item.id === current.id}
              onClick={() => select(item.id)}
              className={clsx(
                'rounded-full px-3 py-1.5 transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-neutral-900',
                item.id === current.id ? 'bg-neutral-900 text-white' : 'hover:bg-black/5',
              )}
            >
              {item.label}
            </button>
          ))}
        </nav>
      )}
    </>
  );
}
