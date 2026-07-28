# Fixed Resume PDF Layout

Use this as the fixed style system unless the user explicitly changes a value.

## Page and Font

- Page: A4 portrait, `595.92 x 841.92 pt`.
- Main content width: `24 pt` left/right margins.
- Typeface: Alibaba PuHuiTi. Use Regular and Bold only.
- Base text: `#333333`. Secondary metadata/date: `#666666`.

## Measured Reference Grid

The reference template was authored on a `793.7 x 1122.5 px` A4 grid at 96dpi.
Render from this grid rather than approximating each page by eye. At 160dpi, use a
`1324 x 1872 px` canvas and a scale of `160 / 96`.

- Main left/right inset: `32 px` on the reference grid.
- Name baseline: `x=284.2, y=63`; photo: top-right, about `100 x 100 px`.
- Header metadata baselines: `y=99` and `y=123`.
- Page 1 section title baselines: personal strengths `175`, work history `464`, project history `687`.
- Page 1 entry baselines: employer `506`, first project `729`, second project `927`.
- Page 2 begins as the continuation of the same grid: project entry `1163`, education title `1370`, education entry `1412`.

The source coordinate system uses 96dpi CSS-like units. Its effective point sizes are
the grid values multiplied by `0.75`: name `30 px`, section title `20 px`, entry name
`16 px`, role/date/body `13 px`, and content labels `14 px`.

## Type Scale

| Role | Font | Size | Alignment |
| --- | --- | --- | --- |
| Name | Bold | 22.5 pt | centered |
| Contact and intent line | Regular | 9.7 pt | centered |
| Section title | Bold | 15 pt | left |
| Employer/project name | Bold | 12 pt | left |
| Role and date | Regular | 10.5 pt | role left, date right |
| `内容：` / `业绩：` label | Bold | 10.5 pt | left |
| Body and bullets | Regular | 9.7 pt | left |

## Header

- Place the name centered at the top.
- Put contact details below it, then the experience/target-role/salary/city line.
- Place one square photo at top-right. Preserve the original visual size and rounded corners.
- Do not use an image, icon, or logo in place of a missing personal photo without confirmation. A mock resume may use a neutral placeholder labeled `示例照片`.

## Sections and Entries

- Use plain white background and black typography; do not introduce cards, colored bands, gradients, or decorative shapes.
- Place a section title above one light divider.
- Divider: `0.35 pt`, `#D9D9D9`; keep roughly `6 pt` from title to line and `7 pt` from line to content. This is the user's approved lighter variant.
- Keep generous but compact vertical rhythm between blocks. Avoid extra paragraph spacing inside body copy.
- Each employer/project header is one line: name at left, role beside it, date aligned to the far right.
- Use simple round bullets. Wrapped bullet lines align with the text, not the marker.
- Continue an entry naturally on page 2. Do not repeat the section heading solely because a paragraph flowed across pages.

## Page Budget

- Keep the first page: header, personal strengths, work history, and first project(s).
- Begin page 2 with the continued project content, then remaining projects, skills, education, and certificates.
- Preserve readable density. Shorten wording before shrinking type or violating margins.

## Dynamic Layout Rules

- This is a reusable layout system, not a PDF background to be edited. Rebuild each resume from structured data and the grid above.
- Keep the original information rhythm: four short strengths on page 1, work history, two projects on page 1, then the final project and education on page 2.
- Flow wrapped text at a 24px reference-grid leading (40px at 160dpi). Preserve English tokens such as `Figma`, `POC`, `Design Token`, and dates as unbroken words where possible.
- Measure each project header before drawing. Leave clear separation between project name, role, and right-aligned date; move the role column right when a title is long rather than allowing overlap.
- Do not add skill or certificate sections merely to fill page 2. Preserve the source template's deliberate lower-page whitespace when the supplied content is short.

## Verification Checklist

- Render every page to PNG at a stable resolution and visually inspect at 100%.
- Verify no missing glyphs, clipped lines, overlapping elements, or incorrect font substitution.
- Verify the photo is authorized and all visible metadata is correct.
- Verify dates align right, section dividers are light and thin, and project headers retain their three-part hierarchy.
