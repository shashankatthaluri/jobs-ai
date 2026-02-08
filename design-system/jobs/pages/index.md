# Index Page Overrides

> **PROJECT:** Jobs
> **Generated:** 2026-02-02 14:01:48
> **Page Type:** General

> ⚠️ **IMPORTANT:** Rules in this file **override** the Master file (`design-system/MASTER.md`).
> Only deviations from the Master are documented here. For all other rules, refer to the Master.

---

## Page-Specific Rules

### Layout Overrides

- **Max Width:** 1200px (standard)
- **Layout:** Full-width sections, centered content
- **Sections:** 1. Intro (Vertical), 2. The Journey (Horizontal Track), 3. Detail Reveal, 4. Vertical Footer

### Spacing Overrides

- No overrides — use Master spacing

### Typography Overrides

- No overrides — use Master typography

### Color Overrides

- **Strategy:** Continuous palette transition. Chapter colors. Progress bar #000000.

### Component Overrides

- Avoid: Expect z-index to work across contexts
- Avoid: Use arbitrary large z-index values

---

## Page-Specific Components

- No unique components for this page

---

## Recommendations

- Effects: Minimal glow (text-shadow: 0 0 10px), dark-to-light transitions, low white emission, high readability, visible focus
- Layout: Understand what creates new stacking context
- Layout: Define z-index scale system (10 20 30 50)
- CTA Placement: Floating Sticky CTA or End of Horizontal Track
