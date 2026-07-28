---
name: resume-pdf-template
description: Generate, revise, or validate Chinese PDF resumes using the user's fixed two-page A4 resume template. Use when asked to turn resume content or JD-tailored text into a PDF, preserve this specific typography/layout, create a privacy-safe mock resume, or check a resume against the template.
---

# Resume PDF Template

Use this skill as the design authority for the user's Chinese resume PDFs. Read [layout-spec.md](references/layout-spec.md) before authoring or reviewing a PDF.

## Workflow

1. Confirm the resume content is truthful and tailored to the stated JD. Do not invent credentials, metrics, employers, awards, or technical skills.
2. Check the photo policy: use the provided photo only when the user authorizes it. If no photo is available, ask whether to use a new photo, an existing authorized photo, or omit it. For mock data, use a neutral placeholder, never the user's photo.
3. Before authoring, extract the reference PDF's text positions and font sizes with `pypdf` visitor callbacks. Use those measurements as the source of truth; do not estimate a similar layout from a screenshot.
4. Use the exact type scale, colors, margins, alignment, divider treatment, and two-page hierarchy in the layout spec. Treat the user's lighter divider preference as authoritative.
5. Use a complete Alibaba PuHuiTi font file for arbitrary new Chinese text. The reference PDF embeds character subsets only; never reuse those subsets to generate new text because missing glyphs can occur. If the complete font is unavailable, label the result as a named fallback and never claim exact typeface fidelity.
6. Render both the reference and output PDFs to PNG at the same resolution and compare them at 100% before delivery. Check Chinese glyphs, clipping, header alignment, section and entry baselines, divider weight, page breaks, image placement, and that no content is stranded by itself at a page boundary.
7. Treat visual QA as blocking. Do not deliver or publish when a header anchor differs by more than 1.5 pt, a section or entry anchor differs by more than 2 pt, the body font size differs by more than 0.5 pt, or the output adds unrequested sections to fill whitespace.
8. For a mock/sanitized resume, replace every identifiable field: name, phone, email, photo, employer, school, dates, client names, and project facts. Do not leave user data in visible text or PDF metadata.

## Delivery

Deliver only a PDF that passed the visual QA gate in the requested output location. State any intentional deviation from the template, especially a fallback font, missing photo, or page-count change.
