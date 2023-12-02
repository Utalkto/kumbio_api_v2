"""Mailjet API integration."""
import json
import logging
import requests
from slugify import slugify

# Django
from django.conf import settings