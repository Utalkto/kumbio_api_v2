from unittest.mock import patch
from communications.notifications import send_whatsapp
from communications.notifications import send_email


@patch('communications.notifications.requests.request')
def test_send_whatsapp(mock_request):
    mock_request.return_value.status_code = 200
    assert send_whatsapp("+584124781318", "Hello, World!") == True
    mock_request.return_value.status_code = 400
    assert send_whatsapp("+584124781318", "Hello, World!") == False


@patch('communications.notifications.Client')
def test_send_email(mock_client):
    mock_send = mock_client.return_value.send.create
    mock_send.return_value.status_code = 200

    assert send_email("emiliojgerdezd@gmail.com", "Test Subject", "<p>Test Body</p>") == True

    mock_send.return_value.status_code = 400
    assert send_email("emiliojgerdezd@gmail.com", "Test Subject", "<p>Test Body</p>") == False