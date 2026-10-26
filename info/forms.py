from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """
    Creates the contact form anyone can fill out to send a
    message to the team.
    """
    # Hidden from people with CSS. Spam bots fill in every field,
    # so a message with this filled in is thrown away
    website = forms.CharField(required=False, label='Leave this empty',
                              widget=forms.TextInput(attrs={
                                  'autocomplete': 'off',
                                  'tabindex': '-1',
                              }))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 6}))

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

    def is_spam(self):
        return bool(self.cleaned_data.get('website'))
