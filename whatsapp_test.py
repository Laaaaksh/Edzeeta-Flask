from twilio.rest import Client


account_sid = "AC06c07055c9b9f47d458c0f79e57656d4"
# Your Auth Token from twilio.com/console
auth_token  = "020b64904d5cf268e7712037e255b352"

client = Client(account_sid, auth_token)


# this is the Twilio sandbox testing number
from_whatsapp_number='whatsapp:+917483444860'
# replace this number with your own WhatsApp Messaging number
to_whatsapp_number='whatsapp:+919716841208'

client.messages.create(body='Ahoy, world!',
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)