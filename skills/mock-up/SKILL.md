---
name: mock-up
description: "Builds interactive, high-fidelity UI mock-ups and redesign prototypes, served locally with live reload through bsdev-proto (nothing is published). Use when the user asks to mock up, prototype or redesign a screen, asks 'what could this screen look like', or wants to explore layouts or design options, for the current repo's app or a greenfield idea. Requires the bsdev container."
argument-hint: "[what to mock up]"
allowed-tools: Bash(bsdev-proto *) Bash(bash ${CLAUDE_SKILL_DIR}/scripts/*)
---

# Mock-up

Design interactive UI prototypes that run locally in the bsdev container, then review your own screenshots before handing over.

## Environment

!`bash "${CLAUDE_SKILL_DIR}/scripts/preflight.sh"`

## Brief

$ARGUMENTS

If the brief is empty, ask what to mock up before doing anything else.

## References

- `${CLAUDE_SKILL_DIR}/references/runtime.md`: commands, importable packages and runtime constraints. Read it before writing any code.
- `${CLAUDE_SKILL_DIR}/references/design-quality.md`: the quality bar for the self-review. Read it before the first review pass.

## Workflow

### 1. Understand the brief

If the brief is thin, ask a small number of targeted questions (platform, key screens and states, tone), all in one message. Don't ask about anything the brief or the repo already answers.

### 2. Ground it (redesigns only)

Explore the repo's real UI before designing: framework, screens, colour and type tokens, components, real copy and data shapes. The prototype mirrors real content, never lorem ipsum.

Prototypes can't import the app's source (see runtime.md), so recreate tokens in `@theme` and rebuild the components you need. Copy any required assets into the prototype folder.

For Android or Compose apps, emulate Material 3 at a 412x915 phone viewport using Roboto Flex (`@import "@fontsource-variable/roboto-flex";` and `--font-sans: "Roboto Flex Variable", ...` in `@theme`).

Greenfield mock-ups skip this step.

### 3. Scaffold

Pick a short kebab-case `<name>` that doesn't clash with the existing prototypes listed above, then copy the starter:

```sh
mkdir -p "<repo>/.agents/prototypes"
cp -r "${CLAUDE_SKILL_DIR}/assets/starter" "<repo>/.agents/prototypes/<name>"
```

The starter has `index.html`, `main.tsx` (renders through `Variants`), `style.css` (Tailwind plus Inter) and `variants.tsx`. Build the screens from there. Split the work into local files (`components/`, `data.ts`) as it grows, rather than one huge `main.tsx`.

Use only the packages listed in runtime.md. For charts, use `recharts`, and follow the `dataviz` skill if it's available.

### 4. Variants

For exploratory asks ("give me options", "explore layouts"), build 2 or 3 genuinely different directions, not colour swaps of one layout. Register each one with the switcher in `main.tsx`:

```tsx
<Variants
  items={[
    { id: 'a', label: 'Cards', render: () => <CardsLayout /> },
    { id: 'b', label: 'Table', render: () => <TableLayout /> },
  ]}
/>
```

`?v=<id>` selects a variant (the first is the default), and the switcher pill only appears when there's more than one. For a single, specific change, build one variant.

### 5. Serve

Run `bsdev-proto start`. It's idempotent and the URL is on the last line. Relay the host-access hint it prints: from a VSCode terminal the port is forwarded automatically, otherwise the user runs `bsdev forward <port>` on the host.

### 6. Self-review (mandatory)

Never hand over without doing this.

1. Run `bsdev-proto logs` and fix every compile or runtime error.
2. For each variant, take a mobile and a desktop shot with distinct output names:

   ```sh
   bsdev-proto shot '<name>/index.html?v=<id>' --viewport 412x915 --out ~/.cache/bsdev-proto/shots/<name>-<id>-mobile.png
   bsdev-proto shot '<name>/index.html?v=<id>' --viewport 1440x900 --full-page --out ~/.cache/bsdev-proto/shots/<name>-<id>-desktop.png
   ```

3. Read each PNG and check it against `design-quality.md`. Fix what's wrong.
4. Repeat until the logs are clean and the shots pass.

If the preflight warned that playwright is missing, still check the logs and tell the user the visual review was skipped.

### 7. Handover

Keep it short:

- the URL (for example `http://localhost:5199/<name>/`)
- one line per variant on what it explores
- trade-offs and open questions worth the user's attention

### 8. Iterate

Apply feedback by editing the files in place; live reload picks it up. Re-run the self-review, then report what changed. Once the user picks a variant, remove the others only if they ask.

## Rules

- Everything stays in `<repo>/.agents/prototypes/<name>/`. Never touch the app's own source.
- Leave `.agents/prototypes` alone in git: don't add it, ignore it or commit it.
- No npm installs, no CDN links, no remote images or fonts.
- Don't stop the server when you're done; the user is probably still looking at it.
