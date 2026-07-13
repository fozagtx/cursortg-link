---
name: web-animation-guidelines
description: Production-tested web animation reference — easing curves, timing tables, copy-paste CSS/Framer Motion patterns, accessibility, and a pre-ship checklist. Use when the user says "animate this", "add animation", "animation timing", "easing curve", "spring animation", "fade in", "slide in", "stagger", "hover animation", "button press", "modal entrance", "loading spinner", "page transition", "animation feels off", "animation best practices", "prefers-reduced-motion", "60fps animation", "animation performance", "what duration should I use", "what easing", or when writing/reviewing any web animation code (CSS transitions, keyframes, Framer Motion, GSAP, Motion One, React Spring). Use proactively whenever generating animated UI components.
---

# Web Animation Best Practices & Guidelines

A production-tested reference for creating high-quality web animations. All timings, easing curves, and code patterns here are battle-tested and ready to use.

## When to apply this skill

Apply automatically whenever you:
- Write CSS `transition` or `@keyframes` rules
- Use Framer Motion, React Spring, GSAP, Motion One, Anime.js, or Auto Animate
- Add hover, press, focus, or state-change animations
- Animate modals, drawers, tooltips, dropdowns, page transitions
- Review existing animation code for performance or polish

If the task only needs a quick value (e.g. "what duration for a tooltip?"), answer directly from the timing table below — no need to dump the full doc.

## Core principles (the non-negotiables)

1. **Natural motion** — Use spring physics or custom cubic-bezier; never `linear` for UI motion (loaders excepted).
2. **Speed** — Target <300ms. Use ease-out so it starts fast.
3. **Purposeful placement** — Animate state changes, modals, enter/exit, feedback. Skip animations on keyboard-driven actions power users repeat all day.
4. **Performance** — 60fps minimum. Animate **only `transform` and `opacity`**. Never animate `width`, `height`, `top`, `left`, `padding`, `margin` (they trigger layout + paint).
5. **Interruptibility** — Users must be able to interrupt mid-animation. Prefer CSS transitions and Framer Motion over keyframe libraries that lock the UI.
6. **Accessibility** — Always respect `prefers-reduced-motion`. No exceptions.
7. **Cohesion** — Match easing/duration across similar components. Define tokens once.

## The three production easing curves

Memorize these. They cover ~95% of UI animation needs.

| Name | Curve | Feel | Use for |
|------|-------|------|---------|
| **Spring-like** | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Energetic overshoot | Buttons, cards, hover, success, micro-interactions |
| **Smooth ease-out** | `cubic-bezier(0.16, 1, 0.3, 1)` | Gentle, professional, no bounce | Modals, page transitions, drawers, large movements |
| **Fast response** | `cubic-bezier(0.4, 0, 0.2, 1)` | Snappy, no hang time | Toggles, checkboxes, tooltips, icon swaps, spinners |

**Don't use** `linear`, `ease`, `ease-in`, `ease-in-out`, or `ease-out` (built-ins) for UI — they feel generic.

## Timing reference

| Element | Duration | Easing |
|---------|----------|--------|
| Button hover | 200ms | Spring-like |
| Button press | 80–100ms | Fast response |
| Modal entrance | 250–300ms | Smooth ease-out |
| Slide transitions | 300ms | Spring-like |
| Success feedback | 600ms | Spring-like (overshoot ok) |
| Micro-interactions | 150–200ms | Spring-like |
| Tooltip appear | 100ms | Fast response |
| Loading spinner | 150ms | Fast response |
| Page transition | 300ms | Smooth ease-out |
| Dropdown menu | 200ms | Smooth ease-out |

## Good vs. great (where to push)

- **Origin** — Animate from contextually meaningful locations. Use `transform-origin` so a dropdown opens from its trigger, not the screen center.
- **Easing** — Custom cubic-bezier > built-ins. Generate at [easing.dev](https://easing.dev).
- **Spring physics for decoration** — `useSpring` (Framer Motion / React Spring) for cursors, decorative motion. Keep functional UI predictable.
- **Advanced properties** — `clip-path`, `mask`, `filter` enable unified animations (e.g. tab indicator that morphs through colors).

## Pre-ship checklist

Before shipping any animation:

- [ ] Completes in <300ms (unless intentionally slow for emphasis)
- [ ] Animates only `transform` and/or `opacity`
- [ ] Uses a custom cubic-bezier (not a default ease)
- [ ] Respects `prefers-reduced-motion`
- [ ] Interruptible — no UI lock
- [ ] Originates from a meaningful location
- [ ] Adds genuine UX value (not animation for its own sake)
- [ ] Consistent with sibling components in the system
- [ ] 60fps verified on a mid-range Android (not just MacBook)
- [ ] Cross-browser tested (Chrome, Firefox, Safari, mobile)

## Reduced-motion baseline

Always include this in any stylesheet that defines animations:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

For Framer Motion, use `useReducedMotion()` and shorten/skip accordingly.

## Quick patterns

For copy-paste-ready CSS and Framer Motion patterns (fade-in-scale, button press, hover lift, slide-up, stagger, spinner), see `references/patterns.md`.

For deeper material — common mistakes, performance debugging, FLIP layout animations, `will-change` / `contain` usage — see `references/advanced.md`.

## Common mistakes

1. Animating `height`/`width` instead of `transform: scaleY()` with `transform-origin`
2. Skipping `prefers-reduced-motion`
3. Over-animating — every state change does not need motion
4. Random durations/easings per component — define tokens
5. Locking interactions during animation playback

## Tools

- **Easing**: [easing.dev](https://easing.dev), [cubic-bezier.com](https://cubic-bezier.com), [easings.net](https://easings.net)
- **Libraries**: Framer Motion, React Spring, Auto Animate, GSAP, Motion One, Anime.js
- **Performance**: Chrome DevTools Performance tab, Paint flashing overlay, real mid-range Android testing

## Output rules when generating animation code

When you produce animation code in response to a request:

1. Include the `prefers-reduced-motion` block — every time.
2. Use one of the three named easings above unless there's a specific reason not to.
3. Pick duration from the timing table; if the use case isn't listed, pick the closest analog and say so.
4. Animate `transform`/`opacity` only. If the natural property is `height`/`width`/`top`, refactor to `transform: scale*` / `translate*` with appropriate `transform-origin`.
5. After writing the code, briefly note which checklist items are satisfied and which the user must verify (e.g. 60fps on device, cross-browser).
