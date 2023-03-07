from django.core.exceptions import ValidationError


def clean_email(self):
    data = self.cleaned_data['email']
    if 'test' in data:
        raise ValidationError("Votre email n'est pas une adresse email valide")
    return data


def clean_mdp(self):
    cleaned_data = super().clean()

    if len(cleaned_data) > 0:
        cleaned_mdp = self.cleaned_data['mdp']
        cleaned_conf_mdp = self.cleaned_data['conf_mdp']

        if cleaned_mdp != cleaned_conf_mdp:
            raise ValidationError("Les 2 mots de passe ne correspondent pas")

    return cleaned_data
