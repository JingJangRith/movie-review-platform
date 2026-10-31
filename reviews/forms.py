from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(
                attrs={
                    "type": "range",
                    "min": 0,
                    "max": 100,
                    "step": 1,
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Write your review...",
                }
            ),
        }