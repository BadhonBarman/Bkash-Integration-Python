# payments/views.py
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import requests
from .forms import PaymentForm
from .models import *
from django.conf import settings
from sslcommerz_lib import SSLCOMMERZ 
from django.urls import reverse 
from django.contrib import messages
from django.http import HttpResponse
import uuid
import random
import time
import os
from urllib.parse import quote
from dotenv import load_dotenv
load_dotenv()

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests



@csrf_exempt
def b_pay(request):
    if request.method == 'GET':
        app_key = os.getenv('app_key'),
        app_secret =os.getenv('app_secret'),
        username =os.getenv('b_username'),
        password =os.getenv('b_pass'),
        base_url = os.getenv('b_base_url')

        # Start Grant Token
        response = requests.post(base_url+'/tokenized/checkout/token/grant', 
                                json={'app_key': app_key, 'app_secret': app_secret},
                                headers={'accept': 'application/json',
                                        'content-type': 'application/json',
                                        'password': password,
                                        'username': username})
        response_data = response.json()
        print(f'response data : {response_data}')
        id_token = response_data['id_token']
        
        request.session['bbbbbt_iddddd'] = id_token
        
        
        # refresh
        refresh_token = response_data['refresh_token']
        print('========================================')
        print(refresh_token)
    
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'username': 'sandboxTokenizedUser02',
            'password': password
        }

        request_data = {
            'app_key': app_key,
            'app_secret': app_secret,
            'refresh_token': refresh_token
        }

        url = os.getenv('b_base_url')+'/tokenized/checkout/token/refresh'

        response_r = requests.post(url, json=request_data, headers=headers)
        response_data_r = response_r.json()

        print(f'refresh token response : {response_data_r}')
        
        
        # create payment
        print('================== CREATE PAYMENT  ======================')
        url = os.getenv('b_base_url')+'/tokenized/checkout/create'
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': id_token,
            'X-APP-Key': app_key
        }
        
        data = {
        "mode": "0011",
        "payerReference": "01619777283",
        "merchantAssociationInfo": "MI05MID54RF09123456One",
        "amount": "500",
        "currency": "BDT",
        "intent": "sale",
        "merchantInvoiceNumber": "Inv0124",
        "callbackURL":"http://127.0.0.1:8000/b_confirmation/",
        "successCallbackURL":"http://127.0.0.1:8000/b_confirmation/",
        "cancelledCallbackURL":"http://127.0.0.1:8000/b_confirmation/"
        }

        response_c = requests.post(url, json=data, headers=headers)
        print(response_c.json())

        # checkout
        
        return redirect(response_c.json()['bkashURL'])
        
    return JsonResponse({'error': 'Payment execution failed'})
        



def b_confirmation(request):
    
    headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': request.session.get('bbbbbt_iddddd'),
            'X-APP-Key': os.getenv('app_key')
        }
    
    data = {
            'paymentID': request.GET.get('paymentID')
        }

    url = os.getenv('b_base_url')+'/tokenized/checkout/payment/status'

    response= requests.post(url, json=data, headers=headers)
    print(f'LAST RESPONSE :  {response.json()}')    

# def b_checkout(request):
#     if 'paymentID' in request.GET and 'status' in request.GET and request.GET['status'] == 'success':
#         paymentID = request.GET['paymentID']
#         base_url = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta'
#         auth = response_data['id_token']
#         post_token = {'paymentID': paymentID}
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': auth,
#             'X-APP-Key': '4f6o0cjiki2rfm34kfdadl1eqq'
#         }
#         response = requests.post(base_url + '/tokenized/checkout/execute', 
#                                  json=post_token, headers=headers)
#         response_data = response.json()

#         customerMsisdn = response_data['customerMsisdn']
#         paymentID = response_data['paymentID']
#         trxID = response_data['trxID']
#         merchantInvoiceNumber = response_data['merchantInvoiceNumber']
#         time = response_data['paymentExecuteTime']
#         transactionStatus = response_data['transactionStatus']
#         amount = response_data['amount']

#         return JsonResponse(response_data)

#     return JsonResponse({'message': 'Payment execution failed'})



