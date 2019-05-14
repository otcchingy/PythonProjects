from twilio.rest import Client

account_sid = 'AC378b9b00b555767b02857c9e90cab1f9'
auth_token = '9836c83a2dd8e534e770715be3373033'
twilio_number = '+12528811375'

client = Client(account_sid, auth_token)


def twilio_send(phone, message):
    send_message = client.messages.create(to=phone, from_=twilio_number, body=message)
