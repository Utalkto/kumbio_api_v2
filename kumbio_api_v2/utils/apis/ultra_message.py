"""Mailjet API integration."""
import json
import logging
import requests
from slugify import slugify

# Django
from django.conf import settings


class UltraMessage:
    url = settings.ULTRAMSG_URL
    token = settings.ULTRAMSG_TOKEN

    def _get_resource(self, uri, **kwargs):
        """Get resource method."""
        url = "{}/{}".format(self.url, uri)
        # Headers
        headers = {"Content-Type": "application/json"}
        request_api = requests.get(url, timeout=10, headers=headers)
        # Save response

        return request_api

    def _post_resource(self, uri, **kwargs):
        """Post resource method."""
        url = "{}/{}".format(self.url, uri)
        # Headers
        headers = {"Content-Type": "application/json"}
        request_api = requests.post(url, data=json.dumps(kwargs), timeout=10, headers=headers)
        # Save response

        return request_api

    def _get_response(self, uri, **kwargs):
        response = None
        try:
            response_json = {}
            data = kwargs.get("data")
            method = kwargs.pop("method")
            send_to = data.get("send_to")
            message = data.get("message")
            data = {
                "token": settings.ULTRAMSG_TOKEN,
                "to": send_to,
                "body": message,
                "priority": 10,
                "referenceId": "",
                "msgid": "",
                "mentions": "",
            }
            if method == "get":
                response = self._get_resource(uri, **data)
            else:
                response = self._post_resource(uri, **data)
            response.raise_for_status()
            if response.status_code in [requests.codes.ok, requests.codes.created]:
                response_json = {
                    "status_code": response.status_code,
                    "response": response.json(),
                }
        except Exception as e:
            if response:
                status_code = response.status_code
                reason = response.json() if hasattr(response, "json") else response.text
            else:
                status_code = 500
                reason = str(e) or "Timeout"
            response_json = {"status_code": status_code, "response": reason}
        return response_json

    def send_whatsapp_message(self, send_to, message):
        uri = f"{settings.ULTRAMSG_INSTANCE}/messages/chat"
        method = "post"
        data = {"send_to": send_to, "message": message}
        return self._get_response(uri, method=method, data=data)
