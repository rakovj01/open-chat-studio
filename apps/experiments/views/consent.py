from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView
from django_tables2 import SingleTableView

from apps.experiments.models import ConsentForm
from apps.experiments.tables import ConsentFormTable
from apps.teams.mixins import LoginAndTeamRequiredMixin


class ConsentFormHome(LoginAndTeamRequiredMixin, TemplateView):
    template_name = "generic/object_home.html"

    def get_context_data(self, team_slug: str, **kwargs):
        return {
            "active_tab": "consent_forms",
            "title": "Consent Forms",
            "new_object_url": reverse("experiments:consent_new", args=[team_slug]),
            "table_url": reverse("experiments:consent_table", args=[team_slug]),
        }


class ConsentFormTableView(SingleTableView):
    model = ConsentForm
    paginate_by = 25
    table_class = ConsentFormTable
    template_name = "table/single_table.html"

    def get_queryset(self):
        return ConsentForm.objects.filter(team=self.request.team)


class CreateConsentForm(CreateView):
    model = ConsentForm
    fields = ["name", "consent_text", "capture_identifier", "identifier_label", "identifier_type", "confirmation_text"]
    template_name = "generic/object_form.html"
    extra_context = {
        "title": "Create Consent Form",
        "button_text": "Create",
        "active_tab": "consent_forms",
    }

    def get_success_url(self):
        return reverse("experiments:consent_home", args=[self.request.team.slug])

    def form_valid(self, form):
        form.instance.team = self.request.team
        form.instance.owner = self.request.user
        return super().form_valid(form)


class EditConsentForm(UpdateView):
    model = ConsentForm
    fields = ["name", "consent_text", "capture_identifier", "identifier_label", "identifier_type", "confirmation_text"]
    template_name = "generic/object_form.html"
    extra_context = {
        "title": "Update Consent Form",
        "button_text": "Update",
        "active_tab": "consent_forms",
    }

    def get_queryset(self):
        return ConsentForm.objects.filter(team=self.request.team)

    def get_success_url(self):
        return reverse("experiments:consent_home", args=[self.request.team.slug])


class DeleteConsentForm(LoginAndTeamRequiredMixin, View):
    def delete(self, request, team_slug: str, pk: int):
        consent_form = get_object_or_404(ConsentForm, id=pk, team=request.team)
        if consent_form.is_default:
            return HttpResponse("Cannot delete default consent form.", status=400)
        consent_form.delete()
        messages.success(request, "Consent Form Deleted")
        return HttpResponse()
