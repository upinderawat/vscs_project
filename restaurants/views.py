from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
import random
import os
from .models import Restaurant
# Create your views here.
def index(request):
    return HttpResponse("<h1>Server is working</h1>")
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
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload), cert=cert)

        responseText = response.text.encode('utf8')
        responseJSON = json.loads(responseText)

        # print(responseJSON['merchantLocatorServiceResponse']['response'][0]['responseValues']['visaMerchantName'])
        SynthesizedResponse = {
            "name": responseJSON['merchantLocatorServiceResponse']['response'][0]['responseValues']['visaMerchantName'],
            "address": responseJSON['merchantLocatorServiceResponse']['response'][0]['responseValues'][
                'merchantStreetAddress'],
            "cuisine": random.choice(cuisines),
            "expense": random.choice(expenses),
            "offers": random.choice(offers),
            "waitTime": str(random.randrange(1, 30))
        }
        # print(SynthesizedResponse)
        restaurant = Restaurant(name=responseJSON['merchantLocatorServiceResponse']['response'][0]['responseValues']['visaMerchantName'],
                                address=responseJSON['merchantLocatorServiceResponse']['response'][0]['responseValues']['merchantStreetAddress'], 
                                cuisine=random.choice(cuisines),
                                expense=random.choice(expenses),
                                offers=random.choice(offers),
                                waitTime=str(random.randrange(1, 30))
                                )
        restaurant.save()
        finalResponse["restaurants"].append(SynthesizedResponse)
        
        # restaurant = Restaurant(name=)
        i += 1

    formattedfinalResponse = json.dumps(finalResponse, indent=4, sort_keys=True)
    return HttpResponse(formattedfinalResponse, 'application/json')
