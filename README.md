# Resume PDF Template

A reusable Codex skill for creating or reviewing Chinese two-page A4 resumes that follow a fixed visual template.

## What is included

- `SKILL.md`: the workflow and privacy rules.
- `references/layout-spec.md`: measurable layout, spacing, type, and divider guidance.
- `examples/sanitized-sample-resume.pdf`: a fully fictional resume that demonstrates the target layout.
- `examples/generate_sanitized_sample.py`: the vector-PDF generator for that sample.
- `examples/assets/synthetic-avatar.png`: an AI-generated, non-real-person avatar used only by the sample.
- `scripts/install_alibaba_puhuiti.py`: one-time installer for the official default font.

All visible resume facts in the sample are fictional. No original resume, personal photo, real contact information, employer, school, project, or client information is included in this repository.

## Generate the sample

```bash
python3 scripts/install_alibaba_puhuiti.py
python3 examples/generate_sanitized_sample.py
```

The installer downloads Alibaba PuHuiTi 3.0 from the official [Alibaba Fonts download page](https://www.alibabafonts.com/#/font) into a local ignored cache. The font files are intentionally not committed: the full package is about 266 MB, above GitHub's normal file limit, and the repository's MIT license applies only to this skill's code and documents, not the font. After the one-time install, the generator uses this font by default with no environment variable or system-font fallback.

The skill treats visual QA as a blocking gate: it extracts the source PDF's type and baseline measurements, then compares a same-resolution render of the output against the reference before delivery.

## Install as a Codex skill

Copy this repository directory to:

```text
~/.codex/skills/resume-pdf-template
```

Then invoke it whenever you need to generate, revise, or visually verify a resume using this template.

## License

MIT. See [LICENSE](LICENSE).
