import random
import http.client
import json
from django.conf import settings

from users.models import User, OTPVerifier


conn = http.client.HTTPSConnection("api.msg91.com")
class UserService:

    def generate_otp(self, user):

        otp = random.randrange(100000, 999999)
        otp_verifier = OTPVerifier.objects.create(user=user, otp=otp)
        return otp_verifier

    def send_otp(self, otp_verifier):
        headers = {
          'authkey': settings.MSG91_AUTH_KEY,
          'content-type': "application/json"
        }
        otp = otp_verifier.otp
        customer_phone = otp_verifier.user.phone_number
        payload = {
          "sender": settings.MSG91_SENDER_ID,
          "route": "4",
          "sms": [ { "message": f"Welcome to CFRESH , Your OTP verification code is: {otp}", "to": [ customer_phone ] } ],
          "DLT_TE_ID": settings.MSG91_DLT_TE_ID
        }
        payload = json.dumps(payload)
        conn.request("POST", "/api/v2/sendsms", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data