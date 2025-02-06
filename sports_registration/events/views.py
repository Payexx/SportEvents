from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil został zaktualizowany!")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'events/profile.html', {'form': form})