from django.conf import settings
from django_tables2 import columns, tables

from apps.analysis.models import Analysis, AnalysisRun, RunGroup
from apps.generics import table_actions


class AnalysisTable(tables.Table):
    name = columns.Column(
        linkify=True,
        attrs={
            "a": {"class": "link"},
        },
        orderable=True,
    )
    actions = columns.TemplateColumn(
        template_name="generic/crud_actions_column.html",
        extra_context={
            "actions": [
                table_actions.Action("analysis:create_run", "fa-solid fa-play"),
                table_actions.EditAction("analysis:edit"),
                table_actions.DeleteAction("analysis:delete"),
            ]
        },
    )

    class Meta:
        model = Analysis
        fields = ("name",)
        row_attrs = settings.DJANGO_TABLES2_ROW_ATTRS
        orderable = False
        empty_text = "No pipelines found."


class RunGroupTable(tables.Table):
    id = columns.Column(
        linkify=True,
        attrs={
            "a": {"class": "link"},
        },
        orderable=True,
    )
    actions = columns.TemplateColumn(
        template_name="generic/crud_actions_column.html",
        extra_context={
            "actions": [
                table_actions.Action("analysis:replay_run", "fa-solid fa-play"),
            ]
        },
    )

    class Meta:
        model = RunGroup
        fields = ("id", "status", "start_time", "end_time")
        row_attrs = settings.DJANGO_TABLES2_ROW_ATTRS
        orderable = False
        empty_text = "No runs found."
