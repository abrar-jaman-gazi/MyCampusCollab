# Form crash fix

Fixed the following pages:

- `/projects/create/`
- `/projects/<id>/join/`
- `/gigs/create/`
- `/gigs/<id>/apply/`

## Cause

The shared form initializer accessed `field.widget.input_type` directly. Django
widgets such as `Textarea`, `Select`, and `CheckboxSelectMultiple` do not all
provide that attribute, so form construction raised `AttributeError`.

## Resolution

The form styling logic in these files now uses safe widget class checks:

- `apps/marketplace/forms.py`
- `apps/collaboration/forms.py`

Regression tests were also added to:

- `apps/marketplace/tests.py`
- `apps/collaboration/tests.py`

No database migration is required for this fix.
