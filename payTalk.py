import requests
import json


def payTalk(transactionDetails):
    webAddress = 'sc20soj.pythonanywhere.com'
    #'http://127.0.0.1:8000/'
    transactionHeaders = {
            'Content-Type': 'application/json',
        }
    choice = input("Press 1 for user login, 2 for guest, other to cancel")
    if ("1" == choice):
        while True:
            login = dict()
            login["email"] = input("Enter email")
            login["password"] = input("Enter password")
            response = requests.get('http://127.0.0.1:8000/getUserDetails', headers=transactionHeaders, data=json.dumps(login))
            if(response.status_code == 200):
                userResponse = json.loads(response.text)

                transactionDetails["deliveryEmail"] = login["email"]
                transactionDetails["deliveryName"] = userResponse["name"]
                transactionDetails["userId"] = userResponse["user_id"]
                response = requests.post('http://127.0.0.1:8000/createTransaction/', headers=transactionHeaders, data=json.dumps(transactionDetails))
                if(response.status_code == 200):
                    data = dict()
                    ctResponse = json.loads(response.text)
                    data["transaction_id"] = ctResponse["transaction_id"]
                    #data["billingAddress"] = userResponse["card_details"]["billingAddress"]
                    data["cardDetails"] = userResponse["card_details"]
                    print("")
                    for i in range(len(data["cardDetails"])):
                        print(str(i),data["cardDetails"][str(i)])
                        print("")
                    cardChosen = input("Select card of corresponding value: ")
                    data["billingAddress"] = userResponse["card_details"][str(cardChosen)]["billingAddress"]
                    data["cardDetails"] = userResponse["card_details"][str(cardChosen)]

                    if(input("Submit(y) or Cancel(n)") == "n"):
                        cancelData = dict()
                        cancelData["transaction_id"] = ctResponse["transaction_id"]
                        response = requests.post('http://127.0.0.1:8000/cancelTransaction', headers=transactionHeaders, data=json.dumps(cancelData))
                        print(response.text)
                        return "Transaction Cancelled"
                    response = requests.post('http://127.0.0.1:8000/makePayment', headers=transactionHeaders, data=json.dumps(data))
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
        response = requests.post('http://127.0.0.1:8000/createTransaction/', headers=transactionHeaders, data=json.dumps(transactionDetails))
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
                    response = requests.post('http://127.0.0.1:8000/cancelTransaction', headers=transactionHeaders, data=json.dumps(cancelData))
                    print(response.text)
                    return "Transaction Cancelled"

                response = requests.post('http://127.0.0.1:8000/makePayment', headers=transactionHeaders, data=json.dumps(data))
                if(response.status_code == 200):
                    return response.text
                else:
                    print("Error: ",response.text)
        else:
            print("Error: ",response.text)

    else:

        return"Transaction Cancelled"



transactionHeaders = {
            'Content-Type': 'application/json',
        }
choice = input("Press 1 to make payment, 2 to view data, 3 to refund: ")
if choice == "1":
	#data = '{"orderId": "23ddew4", "merchantId": "usvd8g78", "currencyCode": "US", "transactionAmount": 60.35}'
    data = dict()
    data["orderId"] = input("orderId: ")
    data["merchantId"] = input("merchantId: ")
    data["currencyCode"] = "US"
    data["transactionAmount"] = float(input("transactionAmount: "))
	#data = json.loads(data)
    print(payTalk(data))
elif choice == "2":
    choice = input("Press 1 to view by user, 2 to view by email: ")
    if choice == "1":
        data = dict()
        data["userId"] = input("Enter User ID: ")
        response = requests.get('http://127.0.0.1:8000/getUserTransactions', headers=transactionHeaders, data=json.dumps(data))
        print(response.text)
    if choice == "2":
        data = dict()
        data["deliveryEmail"] = input("Enter Email: ")
        response = requests.get('http://127.0.0.1:8000/getEmailTransactions', headers=transactionHeaders, data=json.dumps(data))
        print(response.text)
elif choice == "3":
    data = dict()
    data["transaction_id"] = input("Transaction ID: ")
    data["refundAmount"] = float(input("refundAmount: "))
    response = requests.post('http://127.0.0.1:8000/refundTransaction', headers=transactionHeaders, data=json.dumps(data))
    if(response.status_code == 200):
        print("Successful Refund")
    else:
        print("error:  ",response.text)





