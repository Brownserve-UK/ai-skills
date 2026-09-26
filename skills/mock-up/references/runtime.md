# bsdev-proto runtime

`bsdev-proto` is baked into the bsdev image at `/opt/bsdev-proto`. It runs Vite with React Fast Refresh and Tailwind v4, bound to `127.0.0.1`. Nothing is installed into the repo.

## Commands

| Command | Does |
|---|---|
| `bsdev-proto start [repo]` | Start or reuse the server, URL on the last line of stdout |
| `bsdev-proto stop [repo]` | Stop the server |
| `bsdev-proto status` | List all running servers |
| `bsdev-proto url [repo]` | Print the URL of a running server |
| `bsdev-proto logs [repo]` | Vite output, including compile errors |
| `bsdev-proto shot <page> [repo] [--out file.png] [--viewport 412x915] [--full-page]` | Screenshot a page with Playwright, PNG path printed last |

- `[repo]` defaults to the git root of the current directory (or the directory itself).
- Port 5199 by default; the next free port is used if it's taken, so always read the URL from `start` or `url`.
- `start` is idempotent. From a VSCode terminal it opens the host browser on a fresh start (`--no-open` skips that) and the port is forwarded automatically. In a bare `bsdev` session it prints `run on host: bsdev forward <port>`, which the user must run on the host.
- State, logs, the Vite cache and screenshots live in `~/.cache/bsdev-proto`.

## Layout

```plain
<repo>/.agents/prototypes/
  <name>/
    index.html
    main.tsx
    style.css
```

`/` lists every folder with an `index.html`, unless there's a root `index.html`. Pages are served at `/<name>/`.

## Importable packages

Only these bare imports resolve. Anything else fails to compile.

| Package | Version | Use |
|---|---|---|
| `react`, `react-dom` | 19.3.0 | Components; `createRoot` from `react-dom/client` |
| `tailwindcss` | 4.3.3 | `@import "tailwindcss";` in CSS, no config file (use `@theme` for tokens) |
| `lucide-react` | 1.47.0 | Icons |
| `motion` | 13.4.1 | Animation: `import { motion, AnimatePresence } from 'motion/react'` |
| `recharts` | 3.10.1 | Charts |
| `clsx` | 2.1.1 | Conditional class names |
| `@fontsource-variable/inter` | 5.3.0 | Font family `"Inter Variable"` |
| `@fontsource-variable/roboto-flex` | 5.3.0 | Font family `"Roboto Flex Variable"` |

Fonts can be pulled in with `@import` in CSS or `import` in TS.

## Constraints

- Vite's `fs.allow` only covers the prototypes dir, the runtime and the cache. Prototypes **cannot import the app's source**. Recreate tokens and components inside the prototype, and copy any images, icons or fonts it needs into the prototype folder.
- No npm installs. Adding a package means changing the bsdev image.
- Fonts are offline via fontsource only. No CDN links.
- `shot` starts the server if needed, waits 1 second after load, then captures. Entrance animations should settle within that.
- `shot` appends `/` to extension-less pages, so a query string needs the full path: `'<name>/index.html?v=<id>'` (quote it, `?` is a shell glob).
- The default shot path is `~/.cache/bsdev-proto/<key>/shots/<slug>.png`, where the slug comes from the page only. Shots of the same page at different viewports overwrite each other, so pass `--out` with a distinct name. The PNG path is printed last.
- File watching polls under `~/host-repos` automatically (`BSDEV_PROTO_POLL=1` or `0` forces it). If live reload looks stale, check `logs` before anything else.
