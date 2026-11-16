# Matthew Chung — Engineering Portfolio

**[Visit the website](https://4sy8zwp9hz-netizen.github.io/matthew-chung-portfolio/)**

A one-page introduction to quality engineering, manufacturing investigations, and two flagship software platforms. GitHub case studies and interactive public demos are linked throughout the page.

- [Full engineering portfolio](https://github.com/4sy8zwp9hz-netizen/manufacturing-software-portfolio)
- [Manufacturing Yield Platform](https://github.com/4sy8zwp9hz-netizen/manufacturing-analytics-platform)
- [Interactive investigations](https://4sy8zwp9hz-netizen.github.io/webpage_presentation_example/)

This is a separate website repository. It does not replace or modify the linked repositories, investigations, or demos.

## Development

The website is plain HTML, CSS, and local images, with no JavaScript, dependency installation, or build step. Python 3.11+ is sufficient for validation and local preview.

```sh
python tools/validate_site.py
python -m http.server 8765 --bind 127.0.0.1 --directory dist
```

Open `http://127.0.0.1:8765/`. For a project-path preview, serve the repository's parent directory and open `/matthew-chung-portfolio/dist/`.

## Deployment

GitHub Pages uses the **GitHub Actions** publishing source. Pushes to `main` run validation, upload only `dist/`, and publish it to the project URL. Pull requests run validation without deploying. The workflow pins its GitHub-maintained actions to reviewed commit versions, and only the deployment job has Pages write permission.

Relative stylesheet, image, and section links work under the `/matthew-chung-portfolio/` project path. Absolute canonical and social-preview URLs identify this website. No custom domain or account-level Pages settings are required.

## Public boundaries

Software screenshots and demos use fictional data and independent implementations. Separately linked investigations use anonymized observed data, as described on those reports. Scale and activity figures are dated aggregate snapshots—not demo data or unique-user counts.

No proprietary source, credentials, internal endpoints, production records, or private screenshots are included. The small-group demo is separate from the live personal application and its backend.

## Structure

```text
dist/                   Published HTML, CSS, and assets
tools/validate_site.py  Dependency-free validation
.github/workflows/     Validation and Pages deployment
```

## Contact

[Email](mailto:matthewvchung@gmail.com) · [LinkedIn](https://www.linkedin.com/in/matthew-chung-292a0446/)

Released under the [MIT License](LICENSE).
