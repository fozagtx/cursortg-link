# Advanced Animation Concepts

## CSS containment for performance

```css
.animated-card {
  contain: layout style paint;
}
```

Tells the browser changes inside the element won't affect the outside — isolates work.

## `will-change` (use sparingly)

```css
.will-animate-soon { will-change: transform, opacity; }
.animation-complete { will-change: auto; }
```

**Warning**: overusing `will-change` hurts performance — it allocates GPU layers. Only add it when profiling shows benefit, and remove it after the animation ends.

## FLIP technique (layout animations)

- **F**irst: record initial position
- **L**ast: move element to final position instantly
- **I**nvert: apply transform that visually puts it back at start
- **P**lay: animate the transform to 0

Framer Motion does this automatically via the `layout` prop.

## Common mistakes

### 1. Animating layout properties

❌ Bad — triggers layout/paint every frame:
```css
.dropdown { transition: height 300ms; height: 0; }
.dropdown.open { height: 200px; }
```

✅ Good — composite-only:
```css
.dropdown {
  transition: transform 300ms cubic-bezier(0.16, 1, 0.3, 1);
  transform: scaleY(0);
  transform-origin: top;
}
.dropdown.open { transform: scaleY(1); }
```

### 2. Ignoring reduced motion
Always include the `@media (prefers-reduced-motion: reduce)` block.

### 3. Over-animating
Not every state change needs motion. Reserve animation for meaningful transitions and feedback.

### 4. Inconsistent timing
Define design tokens (duration + easing) once and reuse. Random per-component values feel chaotic.

### 5. Blocking interactions
Animations must be interruptible. CSS transitions handle this naturally; Framer Motion does too. Keyframe libraries that lock the UI mid-playback are a regression.

## Performance debugging

If animations feel janky:

1. **DevTools → Performance** — record, look for dropped frames in the FPS chart.
2. Look for **Layout**, **Paint**, **Recalculate Style** entries — these mean you're animating the wrong properties.
3. Confirm only `transform`/`opacity` are changing.
4. **Paint flashing** (DevTools rendering panel) — green flashes show repaints; an animated element should not flash.
5. Test on a real mid-range Android — desktop is misleading.
6. Strip the animation back until it's smooth, then add complexity to find the offender.
7. Audit bundle size — large animation libs can delay first paint more than the animation gains back.

## Reduced-motion strategies

- **Skip** the animation entirely (set duration to 0.01ms).
- **Replace** with a simpler one (slide → fade).
- **Shorten** duration significantly.

In Framer Motion:

```tsx
const reduce = useReducedMotion();
const transition = reduce
  ? { duration: 0.01 }
  : { duration: 0.3, ease: [0.16, 1, 0.3, 1] };
```

## Origin awareness

Animations should originate from a contextually meaningful location:

- Dropdown below a button → `transform-origin: top center` (or `top left/right`)
- Tooltip → origin near the trigger
- Modal triggered by a button in the corner → consider radial expansion from that corner

Spatial continuity helps users build a mental model of the UI.
