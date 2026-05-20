from django import forms

from voyages.models import Option

from .models import Reservation


class ReservationForm(forms.ModelForm):
    options = forms.ModelMultipleChoiceField(
        queryset=Option.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Options et supplements",
    )

    class Meta:
        model = Reservation
        fields = ["date_arrivee", "date_retour", "personnes", "options"]
        widgets = {
            "date_arrivee": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "date_retour": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "personnes": forms.NumberInput(attrs={"min": 1, "class": "form-control"}),
        }

    def __init__(self, *args, voyage=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.voyage = voyage
        self.fields["options"].queryset = (
            voyage.options_list.filter(is_active=True) if voyage else Option.objects.none()
        )

    def clean(self):
        cleaned_data = super().clean()

        if not self.voyage:
            return cleaned_data

        date_arrivee = cleaned_data.get("date_arrivee")
        date_retour = cleaned_data.get("date_retour")
        personnes = cleaned_data.get("personnes")

        if date_arrivee and date_arrivee < self.voyage.start_date:
            self.add_error("date_arrivee", "La date d'arrivee est avant le debut du voyage.")

        if date_retour and date_retour > self.voyage.end_date:
            self.add_error("date_retour", "La date de retour depasse la fin du voyage.")

        if date_arrivee and date_retour and date_retour <= date_arrivee:
            self.add_error("date_retour", "La date de retour doit etre apres la date d'arrivee.")

        if personnes and personnes > self.voyage.places_restantes():
            self.add_error("personnes", f"Seulement {self.voyage.places_restantes()} place(s) disponible(s).")

        return cleaned_data

    def montant_total(self):
        date_arrivee = self.cleaned_data["date_arrivee"]
        date_retour = self.cleaned_data["date_retour"]
        personnes = self.cleaned_data["personnes"]
        options = self.cleaned_data.get("options", [])

        duree = (date_retour - date_arrivee).days or 1
        options_total = sum(option.price for option in options)

        return (self.voyage.price * personnes * duree) + options_total
