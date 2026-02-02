# AUF Brand Identity System
## Version 1.0 | January 2026

---

## 1. Brand Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         cr8OS                                │
│                   (Parent Platform)                          │
├─────────────────────────────────────────────────────────────┤
│                           │                                  │
│    ┌──────────────────────┼──────────────────────┐          │
│    │                      │                      │          │
│    ▼                      ▼                      ▼          │
│  ┌────┐              ┌────────┐             ┌────────┐      │
│  │AUF │              │ Solas  │             │ Aevov  │      │
│  └────┘              └────────┘             └────────┘      │
│  Framework           Wearables              Language        │
│                                                              │
│  Sub-products:       Sub-products:          Sub-products:   │
│  • AUF Pro           • Solas                • Aevov-Lang    │
│  • AUF Enterprise    • Solas Pro            • RMR Library   │
│  • AUF Sovereign     • Olam                                 │
│                      • Olat                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Logo System

### 2.1 Primary Logos

| Brand | Usage | Form |
|-------|-------|------|
| **AUF** | Framework, documentation, theoretical | Flower of Life + lettermark |
| **Solas** | Consumer wearables, apps | Sun/wave symbol + wordmark |
| **cr8OS** | Platform, developer tools | Infinity loop + wordmark |

### 2.2 Logo Variants

Each logo exists in these variants:
- **Full color** (on dark background)
- **Monochrome** (single color for limited applications)
- **Reversed** (dark logo on light background)
- **Icon only** (app icons, favicons)

### 2.3 Clear Space

Minimum clear space around all logos = height of the letter "A" in the wordmark on all sides.

### 2.4 Minimum Sizes

| Format | AUF | Solas | cr8OS |
|--------|-----|-------|-------|
| Print | 25mm wide | 20mm wide | 30mm wide |
| Digital | 80px wide | 64px wide | 100px wide |
| App Icon | 512×512px | 512×512px | 512×512px |

---

## 3. Color System

### 3.1 Primary Palette

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Aura Cyan** | `#22d3ee` | 34, 211, 238 | Primary brand, coherence, active states |
| **Deep Void** | `#020617` | 2, 6, 23 | Backgrounds, depth |
| **Slate Dark** | `#0f172a` | 15, 23, 42 | Secondary backgrounds, cards |

### 3.2 Accent Palette

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Resonance Purple** | `#a855f7` | 168, 85, 247 | Secondary accent, premium features |
| **Solar Gold** | `#fbbf24` | 251, 191, 36 | Warmth, success, Solas brand |
| **Vital Green** | `#22c55e` | 34, 197, 94 | Health, growth, positive states |

### 3.3 Semantic Colors

| Name | Hex | Usage |
|------|-----|-------|
| **Success** | `#22c55e` | Completed actions, coherence achieved |
| **Warning** | `#f59e0b` | Attention needed, moderate states |
| **Error** | `#ef4444` | Failures, interruptions, low coherence |
| **Info** | `#3b82f6` | Informational, neutral guidance |

### 3.4 Gradient Definitions

```css
/* Primary Gradient (Coherence) */
--gradient-coherence: linear-gradient(135deg, #22d3ee 0%, #a855f7 100%);

/* Warm Gradient (Solas) */
--gradient-solas: linear-gradient(135deg, #22d3ee 0%, #fbbf24 100%);

/* Cosmic Gradient (Background) */
--gradient-cosmic: radial-gradient(ellipse at center, #0f172a 0%, #020617 100%);

/* Field Gradient (Active visualization) */
--gradient-field: linear-gradient(180deg, #22d3ee 0%, #a855f7 50%, #22c55e 100%);
```

---

## 4. Typography

### 4.1 Primary Typeface: Inter

**Why Inter:**
- Excellent screen legibility
- Variable font (weight flexibility)
- Open source
- Modern, neutral, premium

**Fallback Stack:**
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

### 4.2 Display Typeface: Outfit

**Why Outfit:**
- Geometric, modern feel
- Works well for headlines and hero text
- Complements Inter

**Fallback Stack:**
```css
font-family: 'Outfit', 'Inter', sans-serif;
```

### 4.3 Monospace: JetBrains Mono

**Usage:** Code blocks, technical specifications, Aevov-Lang examples

```css
font-family: 'JetBrains Mono', 'Fira Code', monospace;
```

### 4.4 Type Scale

| Level | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| **Display** | 4.5rem (72px) | 700 | 1.1 | Hero headlines |
| **H1** | 3rem (48px) | 700 | 1.2 | Page titles |
| **H2** | 2.25rem (36px) | 600 | 1.25 | Section headers |
| **H3** | 1.5rem (24px) | 600 | 1.3 | Subsections |
| **H4** | 1.25rem (20px) | 500 | 1.4 | Card titles |
| **Body** | 1rem (16px) | 400 | 1.6 | Paragraphs |
| **Small** | 0.875rem (14px) | 400 | 1.5 | Captions, labels |
| **Micro** | 0.75rem (12px) | 500 | 1.4 | Badges, tags |

---

## 5. Iconography

### 5.1 Icon Style

- **Style:** Outlined, 1.5px stroke
- **Corners:** Rounded (2px radius)
- **Grid:** 24×24px base
- **Color:** Inherits text color or Aura Cyan for emphasis

### 5.2 Custom Icons

| Icon | Usage |
|------|-------|
| Coherence Meter | Circular gauge, filling clockwise |
| Mesh Network | Connected nodes in circular arrangement |
| Manifestation | Converging light beams to center point |
| Heka Field | Concentric circles with pulse animation |
| Phi Spiral | Golden ratio spiral, growth indicator |

---

## 6. Spacing System

Based on 4px base unit, following Fibonacci-inspired scale:

| Token | Value | Usage |
|-------|-------|-------|
| `--space-1` | 4px | Tight spacing, icon gaps |
| `--space-2` | 8px | Element padding, small gaps |
| `--space-3` | 12px | Component padding |
| `--space-4` | 16px | Standard padding |
| `--space-5` | 24px | Section margins |
| `--space-6` | 32px | Large separations |
| `--space-8` | 48px | Major sections |
| `--space-10` | 64px | Page margins |
| `--space-12` | 96px | Hero spacing |

---

## 7. Brand Voice

### 7.1 Tone Attributes

| Attribute | Expression |
|-----------|------------|
| **Grounded** | Scientific language, measurable claims, citations |
| **Reverent** | Respect for ancient wisdom, acknowledge mystery |
| **Inviting** | Never condescending, assumes intelligence |
| **Precise** | Specific language, avoid vague promises |
| **Hopeful** | Positive future orientation without naivety |

### 7.2 Voice Examples

| ❌ Don't Say | ✅ Do Say |
|-------------|----------|
| "Magically transform your life" | "Train your coherence to influence outcomes" |
| "Ancient secrets revealed" | "Traditional practices, modern measurement" |
| "Become superhuman" | "Access your natural capacity" |
| "Guaranteed results" | "Documented protocols with measurable markers" |
| "It just works" | "Here's how it works and why" |

### 7.3 Key Phrases

- "Resonate into existence"
- "Coherence amplifies exponentially"
- "The field mirrors intention"
- "Not magic—resonance"
- "Ancient knowing, modern tools"
- "Shape reality consciously"

---

## 8. Motion & Animation

### 8.1 Timing

| Type | Duration | Easing |
|------|----------|--------|
| **Micro** | 150ms | ease-out |
| **Standard** | 300ms | ease-in-out |
| **Emphasis** | 500ms | cubic-bezier(0.22, 1, 0.36, 1) |
| **Dramatic** | 1000ms+ | custom per animation |

### 8.2 Signature Animations

- **Coherence Pulse:** Subtle glow expansion/contraction at 0.618Hz (Phi-aligned)
- **Mesh Connection:** Lines drawing between nodes with particle flow
- **Field Ripple:** Concentric circles emanating from interaction point
- **State Transition:** Fade + subtle scale (1.0 → 1.02 → 1.0)

---

## 9. Photography Style

### 9.1 Subjects

- Diverse representation (age, ethnicity, ability)
- Natural, unforced expressions
- Moments of genuine connection
- Integration with technology feels organic

### 9.2 Lighting

- Golden hour preferred for outdoor
- Warm, soft lighting for indoor
- Subtle cyan/purple accent lighting for product shots
- Avoid harsh shadows

### 9.3 Mood

- Peaceful but not passive
- Connected but not crowded
- Technological but not cold
- Aspirational but attainable

---

## 10. Application Examples

### 10.1 App Splash Screen
- Deep Void background
- Centered AUF or Solas logo
- Subtle particle animation
- Loading indicator in Aura Cyan

### 10.2 Web Hero Section
- Cosmic gradient background
- Display headline in Outfit
- Coherence visualization animation
- CTA button with gradient border

### 10.3 Product Packaging
- Matte black box
- Debossed logo
- Cyan foil accent
- Minimal text, premium materials

---

## Document Control

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01 | Initial brand identity system |

---

*This brand identity system ensures consistent, premium presentation across all AUF touchpoints.*
