
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
s="www"

message = Mail(
    from_email = 'abcd@gmail.com',
    to_emails = str("prashantgoyal494@gmail.com"),
    subject = "Welcome to medParliament",
    html_content="ww")
sg = SendGridAPIClient('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')
response = sg.send(message)