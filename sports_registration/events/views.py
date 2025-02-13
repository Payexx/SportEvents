from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Event, EventRegistration
def home(request):
    return render(request, 'events/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Zapisujemy dodatkowe pola
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'Konto zostało utworzone! Możesz się teraz zalogować.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil został zaktualizowany!")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'events/profile.html', {'form': form})

def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    already_registered = EventRegistration.objects.filter(user=request.user, event=event).exists() if request.user.is_authenticated else False
    return render(request, 'events/event_detail.html', {'event': event, 'already_registered': already_registered})

@login_required
def event_register(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if EventRegistration.objects.filter(user=request.user, event=event).exists():
        messages.warning(request, "Już jesteś zapisany na to wydarzenie.")
        return redirect('event_detail', event_id=event.id)

    if event.available_spots() <= 0:
        messages.error(request, "Brak wolnych miejsc na to wydarzenie.")
        return redirect('event_detail', event_id=event.id)

    EventRegistration.objects.create(user=request.user, event=event)
    messages.success(request, "Zapisano na wydarzenie!")
    return redirect('my_events')

@login_required
def my_events(request):
    registrations = EventRegistration.objects.filter(user=request.user)
    return render(request, 'events/my_events.html', {'registrations': registrations})


@login_required
def event_unregister(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Sprawdź, czy użytkownik jest zapisany
    registration = EventRegistration.objects.filter(user=request.user, event=event).first()

    if registration:
        registration.delete()
        messages.success(request, "Wypisano się z wydarzenia!")
    else:
        messages.warning(request, "Nie jesteś zapisany na to wydarzenie.")

    return redirect('my_events')