import requests
import json


def payTalk(transactionDetails):
    transactionHeaders = {
            'Content-Type': 'application/json',
        }
    choice = input("Press 1 for user login, 2 for guest, other to cancel")
    if ("1" == choice):
        while True:
            login = dict()
            login["email"] = input("Enter email")
            login["password"] = input("Enter password")
            response = requests.get('http://127.0.0.1:8000/api/getUserDetails', headers=transactionHeaders, data=json.dumps(login))
            if(response.status_code == 200):
                userResponse = json.loads(response.text)

                transactionDetails["deliveryEmail"] = login["email"]
                transactionDetails["deliveryName"] = userResponse["name"]
                transactionDetails["userId"] = userResponse["user_id"]
                response = requests.post('http://127.0.0.1:8000/api/createTransaction/', headers=transactionHeaders, data=json.dumps(transactionDetails))
                if(response.status_code == 200):
                    data = dict()
                    ctResponse = json.loads(response.text)
                    data["transaction_id"] = ctResponse["transaction_id"]
                    data["billingAddress"] = userResponse["card_details"]["billingAddress"]
                    data["cardDetails"] = userResponse["card_details"]
 
                    if(input("Submit(y) or Cancel(n)") == "n"):
                        cancelData = dict()
                        cancelData["transaction_id"] = ctResponse["transaction_id"]
                        response = requests.post('http://127.0.0.1:8000/api/cancelTransaction', headers=transactionHeaders, data=json.dumps(cancelData))
                        print(response.text)
                        return "Transaction Cancelled"
                    response = requests.post('http://127.0.0.1:8000/api/makePayment', headers=transactionHeaders, data=json.dumps(data))
                    if(response.status_code == 200):
                        return "Success",response.text
                    else: # Shouldn't reach this under any circumstance
                        print("Error: ",response.text)
                else:
                    print("Error: ",response.text)
            else:
                print("Error: ",response.text)

    elif ("2" == choice):
        transactionDetails["deliveryEmail"] = input("Enter email")
        transactionDetails["deliveryName"] = input("Enter name")
        transactionDetails["userId"] = -1
        print(transactionDetails, type(transactionDetails))
        response = requests.post('http://127.0.0.1:8000/api/createTransaction/', headers=transactionHeaders, data=json.dumps(transactionDetails))
        if(response.status_code == 200):
            while True:
                ctResponse = json.loads(response.text)
                print("Enter Card details:")
                print("")
                cardDetails = dict()
                cardDetails["number"] = input("Card number")
                cardDetails["securityCode"] = input("securityCode")
                cardDetails["expiryDate"] = input("expiryDate")

                print("Enter Billing details:")
                print("")
                billingAddress = dict()
                billingAddress["name"] = input("name of occupant: ")
                billingAddress["addressLine1"] = input("addressLine1: ")
                billingAddress["addressLine2"] = input("addressLine2 (Optional, press enter to skip): ")
                billingAddress["city"] = input("city: ")
                billingAddress["postcode"] = input("postcode: ")
                billingAddress["region"] = input("region (Optional, press enter to skip): ")
                billingAddress["countryCode"] = input("countryCode: ")

                data = dict()
                data["transaction_id"] = ctResponse["transaction_id"]
                data["billingAddress"] = billingAddress
                data["cardDetails"] = cardDetails

                if(input("Submit(y) or Cancel(n)") == "n"):
                    cancelData = dict()
                    cancelData["transaction_id"] = ctResponse["transaction_id"]
                    response = requests.post('http://127.0.0.1:8000/api/cancelTransaction', headers=transactionHeaders, data=json.dumps(cancelData))
                    print(response.text)
                    return "Transaction Cancelled"

                response = requests.post('http://127.0.0.1:8000/api/makePayment', headers=transactionHeaders, data=json.dumps(data))
                if(response.status_code == 200):
                    return response.text
                else:
                    print("Error: ",response.text)
        else:
            print("Error: ",response.text)

    else:

        return"Transaction Cancelled"




data = '{ "userId": "3a2", "orderId": "23ddew4", "merchantId": "usvd8g78", "currencyCode": "US", "transactionAmount": "60.35"}'
data = json.loads(data)
print(data)
print(payTalk(data))