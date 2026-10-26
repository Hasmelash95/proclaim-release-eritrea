from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.contrib import messages
from .models import Profile, Location
from .forms import ContactForm


class Info(generic.ListView):
    """
    Generic view for the info page which includes
    profile list views and location list views.
    """
    model = Profile
    template_name = 'info/info.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super(Info, self).get_context_data(**kwargs)
        context['location'] = Location.objects.all()
        return context


def contact(request):
    """
    Renders the contact form and saves sent messages for staff to
    read in the admin.
    """
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            # Spam is not saved, but looks sent so bots don't retry
            if not contact_form.is_spam():
                contact_form.save()
            messages.success(request, 'Thank you for your message. '
                                      'We will get back to you as soon as we can.')
            return redirect('contact')
    else:
        contact_form = ContactForm()
    return render(request, 'info/contact.html',
                  {'contact_form': contact_form})
