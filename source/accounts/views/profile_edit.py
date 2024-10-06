from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms.user_update_form import UserUpdateForm


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile_view')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'profile_edit.html', {'form': form})
