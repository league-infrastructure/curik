---
title: "Your First Web Page"
uid: "webdev-les-001"
---

{{< instructor-guide >}}
**Objectives:** Students will create their first HTML file and view it
in a browser.

**Time:** 30 minutes

**Materials:** Text editor, web browser

**Tips:** Walk through creating the file step-by-step. Don't skip the
`<!DOCTYPE html>` — explain that it tells the browser "this is HTML5."
{{< /instructor-guide >}}

## What Is HTML?

Every web page you've ever visited is made of **HTML**[^1]. When you open
a website, your browser downloads an HTML file and turns it into the
page you see on screen.

[^1]: You can see the HTML of any web page by right-clicking and selecting "View Page Source" or pressing `Ctrl+U` (Windows) / `Cmd+Option+U` (Mac).

## Creating Your First Page

Create a new file called `index.html` and type this:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>My First Page</title>
  </head>
  <body>
    <h1>Hello, World!</h1>
    <p>This is my first web page.</p>
  </body>
</html>
```

Open the file in your browser — you should see a heading and a paragraph!

{{< callout type="tip" >}}
:bulb: **Save and refresh!** Every time you change your HTML file, save
it (`Ctrl+S`) and refresh your browser (`Ctrl+R`) to see the changes.
Or use VS Code's Live Server extension for automatic refresh.
{{< /callout >}}

## The Structure of an HTML Page

Every HTML page has the same basic structure:

| Part | Purpose |
|------|---------|
| `<!DOCTYPE html>` | Tells the browser this is HTML5 |
| `<html>` | The root element — everything goes inside |
| `<head>` | Metadata (title, styles, scripts) — not visible |
| `<title>` | Text shown in the browser tab |
| `<body>` | Everything the user actually sees |

{{< callout type="warning" >}}
:warning: **Tags must be closed!** Every opening tag like `<h1>` needs
a closing tag `</h1>`. Forgetting to close tags is the most common
HTML mistake.
{{< /callout >}}

## Adding More Content

Try adding these elements to your page:

```html
<body>
  <h1>About Me</h1>
  <p>My name is <strong>Alex</strong> and I'm learning web development.</p>

  <h2>My Favorite Things</h2>
  <ul>
    <li>Pizza</li>
    <li>Video games</li>
    <li>Coding</li>
  </ul>

  <h2>Useful Links</h2>
  <p>Check out <a href="https://developer.mozilla.org">MDN Web Docs</a>
     for more HTML tutorials.</p>
</body>
```

{{< callout type="info" >}}
`<strong>` makes text **bold** and `<em>` makes text *italic*. These
are called **inline elements** because they flow within a paragraph.
Block elements like `<h1>` and `<p>` start on a new line.
{{< /callout >}}

{{< readme-shared >}}
## Exercise: Your First Web Page

Create an `index.html` file with:

1. A heading with your name
2. A paragraph introducing yourself
3. An unordered list of your three favorite things
4. A link to your favorite website
{{< /readme-shared >}}

{{< readme-only >}}
## Starter Template

```html
<!DOCTYPE html>
<html>
  <head>
    <title>About Me</title>
  </head>
  <body>
    <!-- Your content here -->
  </body>
</html>
```

Save your file and open it in a browser to check your work.
{{< /readme-only >}}

---

*Next: [HTML Elements](/01-html-basics/02-elements/) — understanding
tags, attributes, and the elements that make up every web page.*
