# utils.py

import os

def get_auth_headers():
    return {
        "Authorization": f"Bearer {os.getenv('LEMONSQUEEZY_API_KEY')}",
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json"
    }
