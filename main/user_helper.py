import requests
import json

#search for disposable emails
def validate_email(email):
  r = requests.get(
    "https://api.mailgun.net/v3/address/validate",
    auth=("api", "pubkey-779be17989ae8e3d4b53ad9c5a57e4f3"),
    params={"address": email})
  return json.loads(r.content)
