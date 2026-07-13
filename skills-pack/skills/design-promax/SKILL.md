---
name: design-promax
description: Build premium React UIs using HeroUI Pro design patterns. Reference library of 30+ component categories across AI, Application, Charts, E-commerce, and Marketing domains. Use when building any React UI, designing components, creating dashboards, landing pages, pricing pages, auth forms, sidebars, navbars, checkout flows, product pages, chat interfaces, or any frontend that needs polished, production-ready design. Use proactively whenever writing React/Next.js UI code — do not wait to be asked.
---

# Design ProMax Design System

**CRITICAL: This skill contains REAL source code in `sources/`. Always read the actual `.js`/`.tsx` files — never guess or hallucinate patterns. The file index is at [sources/FILE_INDEX.md](sources/FILE_INDEX.md).**

## Stack

Every component uses: **React 18 + `@heroui/react` + Tailwind CSS 3 + Framer Motion + `@iconify/react`**

```js
import { Button, Input, Card, Avatar, Badge, Tooltip, Tabs, Tab, Chip,
         Divider, Link, Select, SelectItem, Dropdown, DropdownItem,
         DropdownMenu, DropdownTrigger, User, Listbox, ListboxItem,
         Accordion, AccordionItem, Breadcrumbs, BreadcrumbItem,
         Checkbox, Form, Textarea, Switch, Slider, Progress,
         Table, TableHeader, TableColumn, TableBody, TableRow, TableCell,
         cn } from "@heroui/react";
import { Icon } from "@iconify/react";
```

## How To Use This Skill

1. **Identify the category** from the lookup table below
2. **Read the actual source files** from `sources/{Category}/` — NEVER guess
3. **Copy the patterns exactly** — component structure, props, classNames, icon names
4. **Adapt** the real code to the user's needs

## Lookup Table — What To Read

| User asks for... | Read these files from `sources/` |
|---|---|
| **Login / Signup / Auth** | `Application/authentication (24)__App.js` for form patterns |
| **Sidebar / Navigation** | `Application/sidebars (19)__sidebar*.js`, `Application/sidebars (19)__sidebar*.tsx` |
| **Navbar / Header** | `Application/navbars (3)__*.js`, `Application/Navigation Headers (5)__*.js` |
| **Cards (account, payment, notification, plan, user)** | `Application/cards (20)__*.js` — read the specific card type |
| **Settings / Profile page** | `Application/Layouts (2)__*-setting.js`, `Application/Layouts (2)__sidebar*.js` |
| **Multi-step form / Wizard** | `Application/forms (1)__*.js` — ALL files in this dir |
| **Stepper / Step indicator** | `Application/steppers (7)__*.js` |
| **Data table** | `Application/tables (1)__*.js` |
| **Command palette / Search** | `Application/Command Menus (1)__*.js` |
| **Calendar / Booking** | `Application/calendar (3)__*.js` |
| **Feedback / Rating** | `Application/feedbacks (4)__*.js` |
| **Scrolling banner / Carousel** | `Application/scrolling-banners (5)__*.js` |
| **Chat / AI interface / Messages** | `AI/prompt-containers (11)__conversation*.js`, `AI/prompt-containers (11)__message-card*.js`, `AI/prompt-containers (11)__prompt-input*.js`, `AI/prompt-containers (11)__messages.js` |
| **AI playground** | `AI/playgrounds (1)__*.js` |
| **AI feature cards** | `AI/features (1)__*.js` |
| **Prompt inputs** | `AI/prompt-inputs (11)__*.js` |
| **Charts / Bar / Donut / Pie** | `Charts/Bars-and-Circles (10)__*.tsx` |
| **Charts / Line / Area / Graph** | `Charts/Graphs (2)__*.tsx` |
| **KPI stat cards** | `Charts/KPI-stats (9)__*.tsx` |
| **Pricing page / Tiers** | `Marketing/pricing (8)__pricing*.js`, `Marketing/pricing (8)__pricing*.tsx` |
| **Pricing comparison table** | `Marketing/pricing-comparison (8)__*.js` |
| **Hero section / Landing** | `Marketing/hero-sections (4)__*.js` |
| **FAQ accordion** | `Marketing/faqs (4)__*.js` |
| **Cookie consent** | `Marketing/cookie-consents (8)__*.js` |
| **Marketing banner** | `Marketing/banners (8)__*.js` |
| **Footer** | `Marketing/footers (4)__*.js` |
| **Team page** | `Marketing/teams (1)__*.js` |
| **Product listing / Grid** | `E-commerce/product-list (9)__*.js` |
| **Product detail / View** | `E-commerce/product-view (1)__*.js` |
| **Product filters** | `E-commerce/filters (9)__*.js` |
| **Shopping cart / Checkout** | `E-commerce/checkouts (4)__*.js` |
| **Reviews / Ratings** | `E-commerce/reviews (6)__review*.js`, `E-commerce/reviews (6)__rating*.js` |

## Core Patterns (verified from real source files)

### Component Structure — ALWAYS
```js
"use client";
import React from "react";
import { cn } from "@heroui/react";

const ComponentName = React.forwardRef(({ className, children, ...props }, ref) => (
  <div ref={ref} className={cn("base-classes", className)} {...props}>
    {children}
  </div>
));
ComponentName.displayName = "ComponentName";
export default ComponentName;
```

### Data Separation — data in dedicated files, never inline
Read `sources/AI/prompt-containers (11)__messages.js` for the pattern.

### cn() Utility — ALWAYS use, never string concat
HeroUI-specific classes: `text-small`, `text-tiny`, `shadow-small/medium/large`, `rounded-small/medium/large`, `bg-content1/2/3/4`, `text-default-500/900`, `border-default-200`

### Icons — ALWAYS from @iconify/react with solar: or gravity-ui: prefix
Read actual icon usage from any source file — never guess icon names.

### Design Tokens — ALWAYS semantic, never raw
- Backgrounds: `bg-content1` (primary surface), `bg-content2` (secondary), `bg-content3` (tertiary/user bubbles)
- Text: `text-default-500` (body), `text-default-900` (headings)
- Borders: `border-default-200`, `border-foreground/10` (subtle)
- Semantic: `text-warning` (stars), `text-success`, `text-danger`
- Shadows: `shadow-small` (cards), `shadow-medium` (dropdowns), `shadow-large` (modals)

## Rules (from real source analysis)

1. **Always** `"use client"` directive
2. **Always** `React.forwardRef` for reusable components
3. **Always** `cn()` for class merging
4. **Always** HeroUI semantic tokens — never raw Tailwind colors
5. **Always** separate data from presentation
6. **Always** `@iconify/react` with `solar:` or `gravity-ui:` prefix
7. **Always** add `displayName` to forwarded components
8. **Always** spread `className` and merge with `cn()`
9. **Always** read the actual source file before writing code
10. **Never** hallucinate icon names, classNames, or component APIs