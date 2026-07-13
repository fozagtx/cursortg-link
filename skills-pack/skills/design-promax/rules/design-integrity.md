# Design Integrity Rules

These rules enforce consistency between the agent's generated code and the real source files in `skill/sources/`.

## Rule 1: Source-First
Always read the actual `.js`/`.tsx` source file from `skill/sources/{Category}/` before generating any UI code. Never guess or hallucinate component APIs, classNames, or icon names.

## Rule 2: Pattern Fidelity
Generated code must match the structural patterns found in the source files:
- `React.forwardRef` wrapping
- `cn()` utility for class merging
- `"use client"` directive at the top
- `displayName` assignment

## Rule 3: Token Integrity
Use only HeroUI semantic design tokens found in the source files:
- Backgrounds: `bg-content1`, `bg-content2`, `bg-content3`, `bg-content4`
- Text: `text-default-500`, `text-default-900`, `text-foreground`
- Borders: `border-default-200`, `border-foreground/10`
- Semantic: `text-warning`, `text-success`, `text-danger`, `text-primary`
- Shadows: `shadow-small`, `shadow-medium`, `shadow-large`

Never use raw Tailwind color classes like `bg-gray-100` or `text-blue-500`.

## Rule 4: Icon Sourcing
All icons must use `@iconify/react` `Icon` component with `solar:` or `gravity-ui:` prefixes. Icon names must be verified against real source file imports — never invented.

## Rule 5: Data Separation
Component state, mock data, and configuration must be in separate data files/modules. Never inline large data structures inside component render logic.

## Rule 6: Source Verification
If a generated component's pattern is uncertain, re-read the relevant source file. The answer is always in `skill/sources/`.
