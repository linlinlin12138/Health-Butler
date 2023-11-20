from django import forms

FOOD_SERVING_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddFoodForm(forms.Form):
    serving = forms.TypedChoiceField(
                choices=FOOD_SERVING_CHOICES,
                coerce=int)
    update = forms.BooleanField(required=False,
                initial=False,
                widget=forms.HiddenInput)