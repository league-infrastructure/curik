---
title: "Responsive Design"
uid: "webdev-les-005"
---

{{< instructor-guide >}}
**Objectives:** Students will use media queries and mobile-first design
to make pages that work on phones, tablets, and desktops.

**Time:** 35 minutes

**Materials:** Text editor, browser DevTools (device toolbar)

**Tips:** Have students use Chrome DevTools' device toolbar (`Ctrl+Shift+M`)
to simulate different screen sizes. Show them how their layouts break at
small sizes — then fix it with media queries.

**Common mistake:** Students often write desktop-first CSS and then
struggle to "undo" all the complex layout for mobile. Emphasize
mobile-first: start simple, add complexity for larger screens.
{{< /instructor-guide >}}

## Why Responsive?

Over 60% of web traffic comes from mobile devices[^1]. A page that only
looks good on a desktop monitor is unusable for most of your audience.

[^1]: As of 2024, mobile devices account for approximately 60% of global web traffic, according to Statcounter. This number has been steadily rising since 2017 when mobile first surpassed desktop.

{{< callout type="danger" >}}
A non-responsive website in 2024 is like a store with no front door —
most people will just leave. Google also ranks mobile-friendly sites
higher in search results!
{{< /callout >}}

## The Viewport Meta Tag

First, add this to every page's `<head>`:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

Without it, mobile browsers render your page at ~980px wide and zoom
out, making everything tiny and unreadable.

## Media Queries

Media queries let you apply CSS rules only at certain screen sizes:

```css
/* Mobile-first: base styles for small screens */
.card-grid {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

/* Tablet and up (768px+) */
@media (min-width: 768px) {
    .card-grid {
        flex-direction: row;
        flex-wrap: wrap;
    }
    .card {
        flex: 1 1 45%;
    }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
    .card {
        flex: 1 1 30%;
    }
}
```

{{< callout type="tip" >}}
:bulb: **Mobile-first means `min-width`!** Start with styles for the
smallest screen, then use `@media (min-width: ...)` to add complexity
for larger screens. This is easier than trying to "undo" desktop layout
for mobile.
{{< /callout >}}

## Common Breakpoints

| Breakpoint | Device | `min-width` |
|-----------|--------|-------------|
| Small | Phones | Default (no query) |
| Medium | Tablets | `768px` |
| Large | Laptops | `1024px` |
| Extra Large | Desktops | `1280px` |

## Responsive Typography

```css
/* Base size for mobile */
html { font-size: 16px; }

/* Slightly larger on tablets */
@media (min-width: 768px) {
    html { font-size: 17px; }
}

/* Full size on desktop */
@media (min-width: 1024px) {
    html { font-size: 18px; }
}
```

{{< callout type="info" >}}
Use `rem` units instead of `px` for spacing and font sizes. `1rem` equals
the root font size (usually 16px). When you change the root size with a
media query, everything scales proportionally!
{{< /callout >}}

## Responsive Images

```css
img {
    max-width: 100%;
    height: auto;
}
```

These two lines ensure images never overflow their container. They'll
shrink to fit small screens but won't stretch beyond their natural size
on large screens.

## Responsive Navigation

A common pattern: horizontal nav on desktop, hamburger menu on mobile.

```css
/* Mobile: stack vertically, hide by default */
.nav-links {
    display: none;
    flex-direction: column;
}

.nav-links.active {
    display: flex;
}

/* Desktop: show horizontally */
@media (min-width: 768px) {
    .nav-links {
        display: flex;
        flex-direction: row;
    }
    .hamburger {
        display: none;  /* Hide menu button on desktop */
    }
}
```

{{< callout type="warning" >}}
The hamburger menu toggle requires **JavaScript** — something we'll
cover in a future course. For now, focus on the CSS layout and test
with `.active` added manually to the HTML.
{{< /callout >}}

{{< readme-shared >}}
## Exercise: Responsive Portfolio

Build a responsive portfolio page with:

1. A **navigation bar** that's horizontal on desktop, vertical on mobile
2. A **hero section** with a large heading that scales with screen size
3. A **project grid** showing 1 column on mobile, 2 on tablet, 3 on desktop
4. A **footer** that stacks vertically on mobile

Test your page at 375px (phone), 768px (tablet), and 1024px (laptop)
using the browser's device toolbar.
{{< /readme-shared >}}

{{< readme-only >}}
## Checklist

Before submitting, verify:

- [ ] Viewport meta tag is present
- [ ] No horizontal scrolling at any screen size
- [ ] Text is readable (not too small) on mobile
- [ ] Cards/grid items don't overflow on narrow screens
- [ ] Navigation is usable on both mobile and desktop
{{< /readme-only >}}

---

:tada: **Congratulations!** You've completed the Web Development course.
You now have the skills to build real, responsive web pages from scratch.

> "The web is for everyone, and collectively we hold the power to change
> it for the better." — Tim Berners-Lee[^2]

[^2]: Tim Berners-Lee invented the World Wide Web in 1989 while working at CERN. He made it free and open — never patenting or charging for it.
