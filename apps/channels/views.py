import json
import uuid

from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from apps.channels import tasks
from apps.channels.models import ChannelPlatform, ExperimentChannel


@csrf_exempt
def new_telegram_message(request, channel_external_id: uuid):
    token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if token != settings.TELEGRAM_SECRET_TOKEN:
        return HttpResponseBadRequest("Invalid request.")

    data = json.loads(request.body)
    tasks.handle_telegram_message.delay(message_data=data, channel_external_id=channel_external_id)
    return HttpResponse()


@csrf_exempt
def new_whatsapp_message(request):
    message_data = json.dumps(request.POST.dict())
    tasks.handle_whatsapp_message.delay(message_data)
    return HttpResponse()


@csrf_exempt
def new_facebook_message(request: HttpRequest, team: str):
    # https://developers.facebook.com/docs/messenger-platform/webhooks#:~:text=Validating%20Verification%20Requests
    if request.method == "GET":
        challenge = request.GET["hub.challenge"]
        verify_token_exists = ExperimentChannel.objects.filter(
            experiment__team__slug=team,
            platform=ChannelPlatform.FACEBOOK,
            extra_data__verify_token=request.GET["hub.verify_token"],
        ).exists()
        if not verify_token_exists:
            return HttpResponseForbidden()
        return HttpResponse(challenge, content_type="text/plain")
    elif request.method == "POST":
        body_json = request.body.decode("utf-8")
        tasks.handle_facebook_message.delay(body_json)
        return HttpResponse()
    return HttpResponseForbidden()
