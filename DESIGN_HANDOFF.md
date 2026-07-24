# Figma design handoff

The application uses a centralized design system in `static/css/app.css`. The first `:root` block contains the colors, radii, shadows, font stack and container width used throughout the interface.

Because the supplied Figma Make URL could not be inspected from the build environment, this package implements the approved CampusCollab product brief and visual direction rather than claiming a pixel-perfect extraction.

To apply exact Dev Mode values without changing application structure:

1. Export the approved logo, illustrations and profile placeholders into `static/images/`.
2. Replace the `:root` values in `static/css/app.css` with the Figma color, spacing, radius and shadow values.
3. Replace mock hero artwork in the `.dashboard-mock` block with an exported image if the approved design uses one.
4. Confirm breakpoints at 1440 px, 768 px and 390 px.
5. Keep template component names and backend form fields unchanged so design adjustments do not break functionality.

Reusable UI templates are in `templates/components/`:

- `navbar.html`
- `footer.html`
- `mobile_nav.html`
- `gig_card.html`
- `project_card.html`
- `user_card.html`
- `admin_sidebar.html`
