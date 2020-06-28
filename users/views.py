from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from . import models
# Create your views here.

class checkUser(APIView):
    """ Login check for the user """
    serializer_class = serializers.checkUser

    def post(self, request):
        serializer = serializers.checkUser(data = request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            try:
                user = models.User.objects.get(email = email)
                actualPassword = user.password
                cardNumber = user.cardNumber
                if actualPassword == password:
                    return Response({
                        'result': True,
                        'cardEnding':  int(cardNumber[-4:]),
                        'email': email,
                        'error': 'login successfull'
                    })
                else:
                    return Response({
                        'result': False,
                        'cardEnding':  1234,
                        'email': email,
                        'error': 'Incorrect password'
                    })
            except Exception as e:
                return Response({
                    'result': False,
                    'cardEnding':  1234,
                    'email': email,
                    'error': 'email doesnt exist please register to use our service'
                })
        else:
            return Response({
                'result': False,
                'cardEnding':  1234,
                'email': 'any email',
                'error': serializer.errors['email'][0]
            })


class registerUser(APIView):
    """ To register the user into the database """

    serializer_class = serializers.AddUser

    def post(self, request):
        serializer = serializers.AddUser(data = request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            name = serializer.data.get('name')
            cardNumber = serializer.data.get('cardNumber')
            password = serializer.data.get('password')
            address = serializer.data.get('address')
            # creating a new user
            user = models.User(email = email, name = name, cardNumber = cardNumber, password = password, address = address)
            # a boolean variable to know if the query got executed or not
            var = True
            try:
                user.save()
            except Exception as e:
                var = False
            if var:
                return Response({'result': True,
                                'error': 'no error user got successfully registered'
                                })
            else:
                return Response({'result': False,
                                'error': 'User already exist in the database'
                                })

        else:
            return Response({'result': False,
                            'error': serializer.errors
                            })
 
class fetchInvoice(APIView):
    """ This function returns all the items"""
    def get(self, request):
        try:
            invoiceList = models.Invoice.objects.all()
            jsonList = []
            for item in invoiceList:
                itemDict = {}
                itemDict['itemName'] = item.itemName
                itemDict['quantity'] = item.quantity
                itemDict['itemPrice'] = item.itemPrice
                itemDict['cost'] = item.cost
                jsonList.append(itemDict)
            return Response({
                'invoiceList':jsonList,
                'result': True
            })
        except Exception as e:
            return Response({
                'result': False
            })

