# Design Audit

## Command
`design-audit`

## Description
Audit existing React component code for adherence to Design ProMax design system standards. Checks design token usage, component structure, and pattern compliance.

## Usage
```
design-audit --file <path> [--fix]
```

### Options
- `--file` — Path to the React component file to audit
- `--fix` — Automatically fix common issues (optional)

## Checks
1. Uses `"use client"` directive
2. Uses `React.forwardRef` for reusable components
3. Uses `cn()` for className merging
4. Uses HeroUI semantic tokens (no raw Tailwind colors)
5. Data separated from presentation
6. Uses `@iconify/react` with `solar:` or `gravity-ui:` prefix
7. Has `displayName` on forwarded components

## Output
- Pass/fail for each check
- Specific line numbers for issues found
- Suggested fixes referencing source patterns from `skill/sources/`
