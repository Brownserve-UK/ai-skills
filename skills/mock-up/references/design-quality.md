# Design quality bar

Check every screenshot against this list before handover. A mock-up should look like a shipped product, not a wireframe.

## Content

- Realistic copy and data: real names, plausible numbers, dates and lengths. For redesigns, use the app's actual copy and data shapes. Never lorem ipsum.
- No grey placeholder boxes where real UI belongs. Build the component, or use a lucide icon, a gradient or an avatar with initials.
- Cover the states that matter for the screen: empty, loading (skeletons), error, and long or overflowing text. Put them behind the variant switcher or an in-page toggle if they don't fit in one view.

## Typography and layout

- A clear type scale with few sizes (roughly 4 to 6), with deliberate weights and line heights. Headings are tight, body text is comfortable (1.5ish).
- A consistent spacing rhythm on the Tailwind scale. Related things sit closer together than unrelated things.
- Aligned edges and a clear hierarchy: the eye knows where to go first.
- Line length for body text stays under about 75 characters.

## Colour

- Restrained palette: neutrals plus one accent, with semantic colours (success, warning, danger) used only for meaning.
- Text and essential icons meet WCAG AA contrast (4.5:1 for body text, 3:1 for large text and UI boundaries).
- For redesigns, start from the app's real colour and type tokens, recreated in `@theme`.

## Components and interaction

- One icon set (lucide) at consistent sizes and stroke widths.
- Interactive elements look interactive, with hover, active and disabled states where relevant.
- Visible focus states on everything focusable (`focus-visible:` outlines or rings).
- Touch targets are at least 44px on the mobile viewport.
- Motion only where it explains something (state change, entry, reordering). Keep it short (150 to 300ms) and settled within a second.

## Responsive

- Works at both review viewports: 412x915 and 1440x900. No horizontal scrolling, clipped text or overlapping elements on mobile, and no stretched, sparse layouts on desktop (cap content width).
- The variant switcher doesn't hide anything important in either viewport.
