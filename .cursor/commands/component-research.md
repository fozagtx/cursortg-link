# Component Research

## Command
`component-research`

## Description
Research a specific UI pattern or component category in the Design ProMax source library. Lists all available source files and their capabilities.

## Usage
```
component-research --category <category> [--pattern <pattern>]
```

### Options
- `--category` — Category to research: `ai`, `application`, `charts`, `ecommerce`, `marketing`
- `--pattern` — Optional pattern filter (e.g., `pricing`, `sidebar`, `card`)

## Workflow
1. Read the lookup table from `skill/SKILL.md` to find the relevant category
2. List available source files in `skill/sources/{Category}/`
3. Summarize available components, their structure, and design patterns
4. Return a research brief with file paths and key findings

## Examples
```
component-research --category marketing --pattern pricing
component-research --category application --pattern sidebar
```
