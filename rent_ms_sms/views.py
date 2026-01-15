from django.http import JsonResponse
import requests
from dotenv import dotenv_values
from rent_ms_dto.Enum import SystemTypeInum
from rent_ms_sms.models import RentMsSms
import json
from django.views.decorators.csrf import csrf_exempt


config = dotenv_values(".env")

class SendSms:
    # Function to send sms
    def send_bulk_sms(request_data):
        url = config['HUDUMA_SMS_URL']
        api_token = config['HUDUMA_SMS_TOKEN_JWT']

        headers = {
            "X-Huduma": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            response = requests.post(url, headers=headers, json=request_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print("Error sending bulk SMS:", e)
            if e.response:
                print("Response:", e.response.text)
            raise


    # function to update the information of user if they well receive sms
@csrf_exempt
def update_sms_status_from_huduma(request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)

                smsId = data.get('smsId')
                senderId = data.get('senderId')
                message = data.get('message')
                recipient = data.get('recipient')
                status = data.get('status')
                smscId = data.get('smscId')
                thirdPartyRef = data.get('thirdPartyRef')


                if thirdPartyRef and status is not None:
                    sms = RentMsSms.objects.filter(third_party_ref=thirdPartyRef).first()

                    if sms:
                        sms.status = status
                        sms.smscId = smscId
                        sms.save()

                        return JsonResponse({'status': 'Success', 'message': 'SMS status updated'})
                    else:
                        return JsonResponse({'status': 'Error', 'message': 'SMS with the given reference not found'}, status=404)

                return JsonResponse({'status': 'Error', 'message': 'Invalid or missing data'}, status=400)

            except json.JSONDecodeError:
                return JsonResponse({'status': 'Error', 'message': 'Invalid JSON payload'}, status=400)
        else:
            return JsonResponse({'status': 'Error', 'message': 'Only POST method allowed'}, status=405)

        # call back end point
@csrf_exempt
def rent_ms_sms_callback(request):
            return JsonResponse({'status':'Success','message': 'Rent Ms callback point','code':'200'})












