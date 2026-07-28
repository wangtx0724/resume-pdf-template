# Resume PDF Template

A reusable Codex skill for creating or reviewing Chinese two-page A4 resumes that follow a fixed visual template.

## What is included

- `SKILL.md`: the workflow and privacy rules.
- `references/layout-spec.md`: measurable layout, spacing, type, and divider guidance.
- `examples/sanitized-sample-resume.pdf`: a fully fictional resume that demonstrates the target layout.
- `examples/generate_sanitized_sample.py`: the vector-PDF generator for that sample.
- `examples/assets/synthetic-avatar.png`: an AI-generated, non-real-person avatar used only by the sample.

All visible resume facts in the sample are fictional. No original resume, personal photo, real contact information, employer, school, project, or client information is included in this repository.

## Generate the sample

```bash
python3 examples/generate_sanitized_sample.py
```

The script uses ReportLab and the macOS STHeiti font as a vector fallback. To reproduce a supplied template exactly, use the complete licensed font specified by that template.

The skill treats visual QA as a blocking gate: it extracts the source PDF's type and baseline measurements, then compares a same-resolution render of the output against the reference before delivery.

## Install as a Codex skill

Copy this repository directory to:

```text
~/.codex/skills/resume-pdf-template
```

Then invoke it whenever you need to generate, revise, or visually verify a resume using this template.

## License

MIT. See [LICENSE](LICENSE).
