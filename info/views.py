from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import generic, View
from django.contrib import messages
from .models import Profile
from .forms import ContactForm


class Info(generic.ListView):
    """
    Generic view for the info page which includes the profile list
    and a contact form. Sent messages are saved for staff to read
    in the admin.
    """
    model = Profile
    template_name = 'info/info.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super(Info, self).get_context_data(**kwargs)
        context.setdefault('contact_form', ContactForm())
        return context

    def post(self, request, *args, **kwargs):
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            # Spam is not saved, but looks sent so bots don't retry
            if not contact_form.is_spam():
                contact_form.save()
            messages.success(request, 'Thank you for your message. '
                                      'We will get back to you as soon as we can.')
            return redirect(reverse('info') + '#contact')
        # Show the page again with the form errors
        self.object_list = self.get_queryset()
        return self.render_to_response(
            self.get_context_data(contact_form=contact_form))
