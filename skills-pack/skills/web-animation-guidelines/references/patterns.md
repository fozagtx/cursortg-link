# Animation Patterns (Copy-Paste Ready)

All patterns animate only `transform`/`opacity` and include reduced-motion fallbacks.

## CSS Patterns

### 1. Fade in with slight scale
**Use case**: Modal entrances, card appearances, content reveals.

```css
.fade-in-scale {
  animation: fadeInScale 300ms cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes fadeInScale {
  from { opacity: 0; transform: scale(0.95); }
  to   { opacity: 1; transform: scale(1); }
}

@media (prefers-reduced-motion: reduce) {
  .fade-in-scale {
    animation: none;
    opacity: 1;
    transform: scale(1);
  }
}
```

### 2. Button press feedback
**Use case**: Any clickable button.

```css
.button {
  transition: transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
.button:active {
  transform: scale(0.95);
  transition-duration: 80ms;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
@media (prefers-reduced-motion: reduce) {
  .button { transition: none; }
}
```

### 3. Hover lift with shadow
**Use case**: Cards, product tiles, interactive panels.

```css
.card {
  transition:
    transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1),
    box-shadow 200ms cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}
@media (prefers-reduced-motion: reduce) {
  .card { transition: box-shadow 200ms ease; }
  .card:hover { transform: none; }
}
```

### 4. Slide in from bottom
**Use case**: Mobile drawers, bottom sheets, notifications.

```css
.slide-up {
  animation: slideUp 300ms cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(100%); }
  to   { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
  .slide-up { animation: fadeIn 150ms ease forwards; }
  @keyframes fadeIn {
    from { opacity: 0; } to { opacity: 1; }
  }
}
```

### 5. Stagger children
**Use case**: List items, grids, navigation menus.

```css
.stagger-container > * {
  animation: fadeInUp 400ms cubic-bezier(0.16, 1, 0.3, 1) backwards;
}
.stagger-container > *:nth-child(1) { animation-delay: 0ms; }
.stagger-container > *:nth-child(2) { animation-delay: 50ms; }
.stagger-container > *:nth-child(3) { animation-delay: 100ms; }
.stagger-container > *:nth-child(4) { animation-delay: 150ms; }
.stagger-container > *:nth-child(5) { animation-delay: 200ms; }

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
  .stagger-container > * {
    animation: none; opacity: 1; transform: none;
  }
}
```

### 6. Loading spinner
**Use case**: Loading states, processing indicators.

```css
.spinner {
  width: 24px; height: 24px;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-top-color: #000;
  border-radius: 50%;
  animation: spin 600ms linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) {
  .spinner { animation-duration: 1200ms; }
}
```

## Framer Motion Patterns

### 1. Basic component animation

```tsx
import { motion } from 'framer-motion';

<motion.div
  initial={{ opacity: 0, scale: 0.95 }}
  animate={{ opacity: 1, scale: 1 }}
  exit={{ opacity: 0, scale: 0.95 }}
  transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
>
  Card content
</motion.div>
```

### 2. Hover and tap

```tsx
<motion.button
  whileHover={{
    scale: 1.05,
    transition: { duration: 0.2, ease: [0.34, 1.56, 0.64, 1] }
  }}
  whileTap={{
    scale: 0.95,
    transition: { duration: 0.08, ease: [0.4, 0, 0.2, 1] }
  }}
>
  Click me
</motion.button>
```

### 3. Stagger children

```tsx
const container = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.05 } }
};
const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map(i => (
    <motion.li key={i.id} variants={item}>{i.text}</motion.li>
  ))}
</motion.ul>
```

### 4. Respect reduced motion

```tsx
import { useReducedMotion, motion } from 'framer-motion';

function AnimatedComponent() {
  const reduce = useReducedMotion();
  return (
    <motion.div
      animate={{ x: 100 }}
      transition={{
        duration: reduce ? 0.01 : 0.3,
        ease: reduce ? 'linear' : [0.16, 1, 0.3, 1]
      }}
    />
  );
}
```
