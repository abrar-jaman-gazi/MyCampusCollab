from django import forms

from .models import CollaborationProject, JoinRequest, ProjectUpdate


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


class ProjectForm(StyledModelForm):
    class Meta:
        model = CollaborationProject
        fields = [
            "title",
            "project_type",
            "category",
            "description",
            "objectives",
            "skills",
            "roles_needed",
            "team_size",
            "start_date",
            "end_date",
            "work_mode",
            "preference",
            "attachment",
            "status",
            "progress",
        ]

        widgets = {
            "description": forms.Textarea(attrs={"rows": 6}),
            "objectives": forms.Textarea(attrs={"rows": 4}),
            "skills": forms.CheckboxSelectMultiple(),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "progress": forms.NumberInput(
                attrs={
                    "min": 0,
                    "max": 100,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["skills"].widget.attrs["class"] = "skill-checkboxes"

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:
            self.add_error(
                "end_date",
                "End date must be after the start date.",
            )

        return cleaned_data


class JoinRequestForm(StyledModelForm):
    class Meta:
        model = JoinRequest
        fields = [
            "role",
            "message",
        ]

        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }


class ProjectUpdateForm(StyledModelForm):
    class Meta:
        model = ProjectUpdate
        fields = [
            "title",
            "content",
        ]

        widgets = {
            "content": forms.Textarea(attrs={"rows": 5}),
        }