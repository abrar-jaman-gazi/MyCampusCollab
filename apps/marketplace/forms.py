from django import forms

from .models import Gig, Proposal


class StyledModelForm(forms.ModelForm):
    """Apply CampusCollab styles safely to every widget type."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        choice_group_widgets = (
            forms.CheckboxSelectMultiple,
            forms.RadioSelect,
        )

        placeholder_unsupported_widgets = (
            forms.CheckboxInput,
            forms.CheckboxSelectMultiple,
            forms.RadioSelect,
            forms.Select,
            forms.SelectMultiple,
            forms.FileInput,
        )

        for field in self.fields.values():
            widget = field.widget

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", "form-check-input")

            elif not isinstance(widget, choice_group_widgets):
                widget.attrs.setdefault("class", "form-control")

            if not isinstance(widget, placeholder_unsupported_widgets):
                widget.attrs.setdefault("placeholder", field.label)


class GigForm(StyledModelForm):
    class Meta:
        model = Gig
        fields = [
            "title",
            "category",
            "description",
            "skills",
            "budget_type",
            "budget",
            "deadline",
            "experience_level",
            "attachment",
            "status",
        ]

        widgets = {
            "description": forms.Textarea(attrs={"rows": 7}),
            "deadline": forms.DateInput(attrs={"type": "date"}),
            "skills": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["skills"].widget.attrs["class"] = "skill-checkboxes"


class ProposalForm(StyledModelForm):
    class Meta:
        model = Proposal
        fields = [
            "cover_letter",
            "proposed_cost",
            "delivery_days",
            "milestones",
            "attachment",
        ]

        widgets = {
            "cover_letter": forms.Textarea(attrs={"rows": 7}),
            "milestones": forms.Textarea(attrs={"rows": 4}),
        }