# Build UI Component

## Command
`build-ui`

## Description
Build a React UI component or page using Design ProMax patterns. Routes to the correct source files, reads real code, and adapts it.

## Usage
```
build-ui --type <category> --name <component-name> [options]
```

### Options
- `--type` — Component category: `ai`, `application`, `charts`, `ecommerce`, `marketing`
- `--name` — Component name (e.g., `pricing-page`, `login-form`, `chat-interface`)
- `--output` — Output file path (optional)

## Workflow
1. Identify the category from the lookup table in `skill/SKILL.md`
2. Read the corresponding source files from `skill/sources/{Category}/`
3. Extract patterns: component structure, props, design tokens, icon names
4. Build the component adapting real code to the user's needs
5. Output fully functional React component with `"use client"`, `React.forwardRef`, `cn()`

## Examples
```
build-ui --type marketing --name pricing-page --output ./components/pricing.tsx
build-ui --type application --name login-form --output ./components/auth/login.tsx
```
