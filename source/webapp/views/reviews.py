from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView
from part.models import Part
from webapp.forms.review_form import ReviewForm


class CreateReviewView(LoginRequiredMixin, CreateView):
    template_name = "review/create_review.html"
    form_class = ReviewForm

    def form_valid(self, form):
        part = get_object_or_404(Part, pk=self.kwargs["pk"])
        review = form.save(commit=False)
        review.part = part
        review.author = self.request.user
        review.save()
        return redirect(part.get_absolute_url())
