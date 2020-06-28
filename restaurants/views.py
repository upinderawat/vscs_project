"""
APIs called:
    1) Visa Merchant Locator API
    2) Visa Queue Insights API

"""
import requests
import json
import random
import os

from django.http import HttpResponse

from .models import Restaurant, Reservation
from .serializers import ReservationSerialzier

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
def index(request):
    return HttpResponse("<h1>Server is working</h1>")

class reserveTable(APIView):
    serializer_class = ReservationSerialzier

    def post(self, request, format=None):
        serializer = ReservationSerialzier(data = request.data)
        if serializer.is_valid():
            if not Reservation.objects.filter(email=serializer.validated_data['email']).exists():
                serializer.save()
                return Response({
                    'result': 'true',
                    'message': 'Booking has been made for {0} under {1}'.format(
                        serializer.validated_data['numberOfPeople'], serializer.validated_data['email'])
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'result': 'false',
                    'message': 'Booking already exists for {}'.format(serializer.validated_data['email'])
                }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_merchant_data(request):
    #### Synthesized data ####
    offers = ["10% off on total bill", "1+1 on drinks", "10% off on visa card payments", "20% off on buffet"]
    cuisines = ["CHINESE", "CONTINENTAL", "ITALIAN", "INDIAN"]
    expenses = ["LOW", "AVERAGE", "HIGH"]

    #### Input ####
    zipcode = "94404"
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cert_file_path = os.path.join(BASE_DIR, "restaurants/cert.pem")
    key_file_path = os.path.join(BASE_DIR,"restaurants/key.pem")
    url = "https://sandbox.api.visa.com/merchantlocator/v1/locator"

    finalResponse = {"restaurants": []}

    #### Visa Merchant Locator API call ####
    i = 1
    while i < 3:
        payload = {
            "header": {
                "messageDateTime": "2020-06-20T16:51:51.903",
                "requestMessageId": "Request_001",
                "startIndex": str(i)
            },
            "searchAttrList": {
                "merchantCategoryCode": ["5812"],
                "merchantCountryCode": "840",
                "merchantPostalCode": zipcode,
                "distance": "20",
                "distanceUnit": "M"
            },
            "responseAttrList": ["GNLOCATOR"],
            "searchOptions": {
                "maxRecords": "10",
                "matchIndicators": "true",
                "matchScore": "true"
            }
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic UTlON1pTTVdZQzIxTFRXRjJHQVEyMUl6b0Fzb1lSNTBnOS1RZ2MwbTlieW81eXV2bzpCdjBqeThwM1ZyNDl5aUk0OTZCeXd6MXBNYzBUeFF3eUZ2M3lFUVc='
        }

        cert = (cert_file_path, key_file_path)
        try:
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload), cert=cert)
            responseText = response.text.encode('utf8')
            responseJSON = json.loads(responseText)

            SynthesizedResponse = {
                "id": responseJSON['merchantLocatorServiceResponse']['response'][0]['responseValues']['visaMerchantId'],
                "name": responseJSON['merchantLocatorServiceResponse']['response'][0]['responseValues']['visaMerchantName'],
                "address": responseJSON['merchantLocatorServiceResponse']['response'][0]['responseValues'][
                    'merchantStreetAddress'],
                "cuisine": random.choice(cuisines),
                "expense": random.choice(expenses),
                "offers": random.choice(offers),
                "waitTime": random.randrange(1, 30)
            }
            try:
                restaurant = Restaurant(id=responseJSON['merchantLocatorServiceResponse']['response'][0]['responseValues']['visaMerchantId'],
                                        name=responseJSON['merchantLocatorServiceResponse']['response'][0]['responseValues']['visaMerchantName'],
                                        address=responseJSON['merchantLocatorServiceResponse']['response'][0]['responseValues']['merchantStreetAddress'], 
                                        cuisine=random.choice(cuisines),
                                        expense=random.choice(expenses),
                                        offers=random.choice(offers),
                                        waitTime=random.randrange(1, 30)
                                        )
                restaurant.save()
            except Exception as e:
                return HttpResponse("Error inserting into restaurant table: "+str(e))

            finalResponse["restaurants"].append(SynthesizedResponse)
            
        except Exception as e:
            return HttpResponse("API request error: "+str(e))
        i += 1

    formattedfinalResponse = json.dumps(finalResponse, indent=4, sort_keys=True)
    return HttpResponse(formattedfinalResponse, 'application/json')

def fetchWaitingTime(zipcode,cert_file_path,key_file_path):
    """
    Visa Queue Insights API call
    Returns waiting time for merchants in an area
    """
    payload = {
        "requestHeader": {
            "messageDateTime": "2020-06-28T08:42:33.327",
            "requestMessageId": "6da60e1b8b024532a2e0eacb1af58581"
        },
        "requestData": {
            "kind": "predict"
        }
    }
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic UTlON1pTTVdZQzIxTFRXRjJHQVEyMUl6b0Fzb1lSNTBnOS1RZ2MwbTlieW81eXV2bzpCdjBqeThwM1ZyNDl5aUk0OTZCeXd6MXBNYzBUeFF3eUZ2M3lFUVc='
    }
    cert = (cert_file_path, key_file_path)
    url = "https://sandbox.api.visa.com/visaqueueinsights/v1/queueinsights"

    try:
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload), cert=cert)
    except Exception as e:
            return HttpResponse("Queue insights API request error: "+str(e))

    responseJSON = json.loads(response.text.encode('utf8'))
    formattedResponse = json.dumps(responseJSON, indent=4, sort_keys=True)
    return HttpResponse(formattedResponse, 'application/json')