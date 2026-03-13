# The LEAGUE of Amazing Programmers — Web Brand Guide

This document is a reference for AI agents building League-branded web properties (curriculum sites, landing pages, tools, etc.). It consolidates the official brand style guide with colors and patterns observed on the current website (jointheleague.org).

---

## Color Palette

### Primary Brand Colors

These are the official brand colors. They should dominate any League web property.

| Name | Hex | RGB | Pantone | Use |
|------|-----|-----|---------|-----|
| **League Orange** | `#F37121` | 242, 101, 34 | 165C | Primary accent: buttons, CTAs, logo silhouette, active/hover states, highlights |
| **Black** | `#000000` | 0, 0, 0 | Black | Primary text, headings, logo wordmark, reverse backgrounds |
| **Brand Gray** | `#ABACA5` | 171, 172, 165 | 414C | Supporting text, dividers, secondary UI elements, captions |
| **White** | `#FFFFFF` | 255, 255, 255 | — | Page backgrounds, reverse text on dark/orange backgrounds |

### Website Secondary Colors

These colors are used on the current jointheleague.org website. Use them for web properties to maintain visual consistency with the main site.

| Name | Hex | Use |
|------|-----|-----|
| **Cream Background** | `#FEF7F0` | Hero sections, highlighted content areas, warm background zones |
| **Light Peach** | `#FFF5EE` | Subtle page background tint, alternate section backgrounds |
| **Section Gray** | `#F9FAFB` | Alternating content sections, card backgrounds |
| **Card Border** | `#E5E7EB` | Card outlines, dividers, form borders, subtle separators |
| **Dark Charcoal** | `#1A1A2E` | Footer background, dark section backgrounds |
| **Link Orange** | `#E8611A` | Inline hyperlinks (slightly darker than primary orange for text readability) |
| **Text Dark** | `#1F2937` | Primary body text, headings in content areas |
| **Text Medium** | `#4B5563` | Secondary body text, descriptions, metadata |
| **Text Muted** | `#6B7280` | Muted text, placeholders, timestamps, captions |

### CSS Custom Properties

Define these at `:root` for consistent theming:

```css
:root {
  /* Primary brand */
  --league-orange: #F37121;
  --league-black: #000000;
  --league-gray: #ABACA5;

  /* Web secondary */
  --league-cream: #FEF7F0;
  --league-peach: #FFF5EE;
  --league-section-bg: #F9FAFB;
  --league-card-border: #E5E7EB;
  --league-footer-bg: #1A1A2E;

  /* Text hierarchy */
  --league-text-primary: #1F2937;
  --league-text-secondary: #4B5563;
  --league-text-muted: #6B7280;

  /* Interactive */
  --league-link: #E8611A;
  --league-button-bg: #F37121;
  --league-button-hover: #E06010;
}
```

---

## Logo Assets

All logo files are hosted at: **https://images.jointheleague.org/logos/**

Use these URLs directly. Do not host copies elsewhere unless specifically required.

### Available Logo Files

| File | Description | Use For |
|------|-------------|---------|
| `logo4.png` | Primary logo (female flag carrier with text) | **Default logo** for headers, hero sections |
| `logo_girl_flag.png` | Female flag carrier with wordmark | Alternative primary logo |
| `figures_text_boy.png` | Male flag carrier with wordmark | Alternative primary logo |
| `figures_girl.png` | Female figures silhouette only (no text) | Icon/favicon use when wordmark appears nearby |
| `logo_JTL_horiz.png` | Horizontal layout logo | Narrow spaces, navigation bars, footers |
| `logo_black.png` | 1-color black logo | Light backgrounds, limited color printing |
| `logo_white.png` | 1-color white logo | Dark or midtone backgrounds |
| `logo_w_orangebg.png` | White logo on orange background | Orange branded sections, banners |
| `logo_blackbg.jpg` | Logo on black background (reverse) | Dark-themed pages, dark mode |
| `logo_square_1000.png` | Square format, 1000px | Social media profiles, app icons, thumbnails |
| `wordmark.png` | Wordmark only (no figures) | Text-heavy layouts where figures appear elsewhere |
| `flag.png` | Flag element only | Decorative accent, small icon |
| `bolt.png` | Lightning bolt element | Decorative accent, favicon variant |
| `flag-sunburst.png` | Flag with sunburst effect | Feature graphics, splash screens |

### Logo Usage Rules

- The logo must always be surrounded by **clear space** equal to at least the height of the wordmark text. No other design elements may appear within this space.
- Two versions exist (male and female flag carrier). They can be used interchangeably.
- The **horizontal logo** should only be used when the primary (stacked) logo does not fit the layout.
- The **symbol** (figures silhouette) may be used alone only when the League's name or wordmark appears nearby in context.
- The silhouette should always remain a **group of people** (a League). Do not isolate a single figure.

### Do Not

- Add drop shadows or other special effects to the logo.
- Use a single figure from the logo in isolation.
- Place the orange logo over any colored background (**only on black or white**).
- Use colors other than Pantone 165 orange, black, or white for the logo.
- Alter the proportions of the logo.
- Substitute the wordmark with typed text. Always use the official logo image files.

### Reverse / Dark Backgrounds

- **On black background:** Use orange silhouette with white wordmark (`logo_blackbg.jpg`).
- **On other dark or colored backgrounds:** Use white silhouette with black wordmark (`logo_white.png`). The orange silhouette should never appear on any background other than black or white.

---

## Typography

### Brand Fonts

The official League fonts are **Trade Gothic Bold No. 2** (headings) and **Trade Gothic Light** (body). Since these are not freely available web fonts, use the approved alternatives:

| Role | Official Font | Web Alternative | CSS Stack |
|------|--------------|-----------------|-----------|
| Headings | Trade Gothic Bold 2 | Arial Bold | `'Arial', 'Helvetica Neue', sans-serif` |
| Body text | Trade Gothic Light | Arial / Arial Light | `'Arial', 'Helvetica Neue', sans-serif` |
| Code / monospace | — | System monospace | `'Courier New', 'Consolas', monospace` |

**The wordmark in the logo must never be replaced with typed text.** Always use the official logo image. Do not recreate it in HTML/CSS.

---

## Web Implementation Patterns

### Buttons

The League website uses rounded buttons with the primary orange:

- **Primary button:** background `#F37121`, text white, `border-radius: 8px`, `padding: 12px 24px`
- **Secondary button:** background white, `border: 2px solid #F37121`, text `#F37121`, same radius/padding
- **Hover state:** slightly darker orange (`~#E06010`) for primary; light orange fill for secondary

### Page Layout

The current website follows these patterns:

- Warm cream hero section (`#FEF7F0`) at the top of the page
- Alternating white and light gray (`#F9FAFB`) sections for content grouping
- Card-based layouts with subtle borders (`#E5E7EB`) for program/class listings
- Dark charcoal footer (`#1A1A2E`) with white text and orange link accents
- Orange pill-shaped tags for class/category labels
- Rounded corners on cards and buttons (~8px)

---

## Key URLs and Resources

| Resource | URL |
|----------|-----|
| Main website | https://www.jointheleague.org |
| Curriculum site | https://curriculum.jointheleague.org |
| Logo files | https://images.jointheleague.org/logos/ |
| All curriculum images | https://images.jointheleague.org |
| Class images | https://images.jointheleague.org/classes/ |
| Marketing images | https://images.jointheleague.org/mkt/ |
| Python images | https://images.jointheleague.org/python/ |
| Module navigation icons | https://images.jointheleague.org/module-navigation/ |
| Robot images | https://images.jointheleague.org/robots/ |
| Image repo (GitHub) | https://github.com/league-curriculum/images |

---

## Quick Reference for Agents

When generating web content for the League:

1. **Always use `#F37121` as the primary accent color.** This is the League's orange. Use it for buttons, links, highlights, and interactive elements.
2. **Use Arial as the web font.** Bold for headings, regular/light for body text. Fall back to Helvetica Neue or system sans-serif.
3. **Reference logos from `images.jointheleague.org`.** Use `logo4.png` as the default. Use `logo_JTL_horiz.png` for navigation bars.
4. **Warm backgrounds, not sterile white.** Use `#FEF7F0` (cream) for hero areas and `#F9FAFB` for alternating sections.
5. **Dark footer with `#1A1A2E` background.** White text, orange accent links.
6. **Never place the orange logo on colored backgrounds.** Orange logo is only valid on black or white. On other backgrounds, use the white logo.
7. **Never type the wordmark.** Always use the official logo image. Do not recreate it in HTML/CSS text.
8. **Maintain clear space around the logo.** At minimum, leave padding equal to the wordmark height on all sides.
