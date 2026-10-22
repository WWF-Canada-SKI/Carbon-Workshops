# Maintaining the workshop website

## Structure

- `index.html`: workshop library homepage.
- `_config.yml`: shared Jekyll configuration.
- `_layouts/default.html`: shared header, navigation, and page layout.
- `_data/workshops.yml`: sidebar links for all workshops.
- `assets/css/site.css`: responsive site styles.
- `.github/workflows/workshop-pages.yml`: build, link checks, and deployment.
- `scripts/check_site.py`: checks generated internal links and images.

## Edit an existing component

Edit its Markdown guide and keep downloads and images beside it. The folder's
README becomes that component's homepage. Use relative links, e.g. `../README.md`,
`../03_Field_Methods/`, and `images/photo.png`. The website rewrites links to
existing Markdown guides into their corresponding web addresses.

Changes pushed to `main` automatically rebuild and republish. The build runs
internal-link checks before deployment; external services are not checked by CI.

## Add a workshop or component

1. Create its folder and add a populated `README.md`.
2. Add images and downloads inside that folder.
3. Add a link in the parent guide and in `_data/workshops.yml`.
4. For a new workshop collection, add a card to `index.html`.
5. Commit to `main` and check the publishing workflow.

Use consistent letter case in filenames. In particular, do not keep both
`README.md` and `Readme.md` in one folder: that creates conflicts on macOS.

## Missing resources

`Blue Carbon Workshops/resources.md` lists available and pending materials.
When a pending resource is added, replace the availability links in the guides
with its real path and update that list. Do not substitute the archived Tsawwassen
workbook for the current Cowichan example; their teaching contexts differ.

The Blue Carbon Data Interpretation component currently contains an overview and field-to-lab
preparation. Its later sections remain in development.

Green Carbon includes Forests, Grasslands, and Wetlands, each with four core
components, an ecosystem-specific supplement, and a worked example.
Shared PDFs live in `Green Carbon Workshops/_Shared/`; the configuration explicitly
includes linked underscore-prefixed resource folders in the published site.

## Personal preview and work publishing

The personal fork is the preview; the work repository can remain the authoritative
copy of workshop materials. After previewing a change, open a pull request from
the personal fork to `WWF-Canada-SKI/Carbon-Workshops`, review, and merge it there.
Pages settings are separate for each repository and are not copied by a pull request.

In each repository set **Settings → Pages → Source → GitHub Actions**. Keep the
repository name `Carbon-Workshops` in both accounts so the same `/Carbon-Workshops`
base path works. If the name changes, update `baseurl` in `_config.yml`.

Use the work site's component links when sharing with participants. Before starting
new preview work, use GitHub's **Sync fork** to bring in work-repository updates.
Resolve conflicts through the normal GitHub flow; forks do not sync automatically.

## Terrestrial content import

The Green Carbon materials were copied from
`CathalD/Terrestrial_Carbon_Workshops_V1` at commit `6e13888ba789f2db8385880e198206d1ad2e1ed3`.
The original repository retains its commit history. Review future source updates
before importing them so changes made in this repository are preserved.
