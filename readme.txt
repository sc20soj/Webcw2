PythonAnywhere:
https://sc20soj.pythonanywhere.com

Client code:
payTalkOnline.py
just run as python payTalkOnline.py

Admin page:
username=scott
password=james

User for system login:
email=sc20soj@leeds.ac.uk
password=James

API requests:
Submit all request data in format:
data = '{field: value, field: value}'
header Example:
transactionHeaders = {'Content-Type': 'application/json',} 
example request:
response = requests.post('https://sc20soj.pythonanywhere.com/api/createTransaction/', headers=transactionHeaders, data=data)


createTransaction
POST request
data = 
userId: int, (-1 for not a user) 
orderId: String, 
merchantId: String, 
currencyCode: String,(only accepts US or Pound) 
transactionAmount: float, 
deliveryEmail: String, 
deliveryName: String


getTransaction
GET request
transactionId: int


getUserTransactions
GET request
userId: int


getUserDetails
GET request
email: String, 
password: String


getEmailTransaction
GET request
email: String


makePayment
POST request
transaction_id: int, 
cardDetails :{number:String(16-19 chars, valid under luhens algorithm), 
securityCode:String(3-4 chars), 
expiryDate:XX/XX}

billingAddress : {name:String,
addressLine1:String,
addressLine2:String,
city:String,
postcode:String,
region:String,
countryCode:String}


refundTransaction
POST request
transaction_id: int,
refundAmount: float

cancelTransaction
Post request
transaction_id: int
