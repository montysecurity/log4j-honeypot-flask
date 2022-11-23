from flask import Flask, redirect, url_for, request
from discord_webhook import DiscordWebhook
import json, os, requests

honeypot_name = "My log4j honeypot"
honeypot_port = 80
global discord_webhook
discord_webhook = ""

if "LOG4J_WEBHOOK" in os.environ and os.environ["LOG4J_WEBHOOK"].strip() != "":
    discord_webhook = os.environ["LOG4J_WEBHOOK"]

if "HONEYPOT_NAME" in os.environ and os.environ["HONEYPOT_NAME"].strip() != "":
    honeypot_name = os.environ["HONEYPOT_NAME"]

if "HONEYPOT_PORT" in os.environ and os.environ["HONEYPOT_PORT"].strip() != "":
    try:
        honeypot_port = int(os.environ["HONEYPOT_PORT"].strip())
    except:
        print("Invalid port: " + os.environ["HONEYPOT_PORT"])
        print("Reverting to port 80 default")
        honeypot_port = 80

app = Flask(__name__)

def reportHit(request):
    msg = ""
    msg += str("Log4J Honeypot Alert\n")
    msg += str("- Source IP: " + request.remote_addr + "\n")
    msg += str("- Headers:\n")
    for header in request.headers:
        msg += str("-- " + str(header) + "\n")
    for fieldname, value in request.form.items():
        msg += str("-- " + str((fieldname, value)) + "\n")
    log = open("log.txt", "a")
    log.write(msg)
    log.close()
    if "https" in discord_webhook:
        webhook = DiscordWebhook(url=discord_webhook, content=msg)
        response = webhook.execute()

login_form = """<html>
<head><title>Secure Area Login</title></head>
<body>
<h1>Log in to Secure Area</h1>
<form method='post' action='/'>
  <b>Username:</b> <input name='username' type='text'/><br/>
  <b>Password:</b> <input name='password' type='password'/><br/>
  <input type='submit' name='submit'/>
</form>
</body></html>"""

@app.route('/websso/SAML2/SSO/<path:hostname>') # vCenter websso login path
@app.route("/", methods=['POST','GET','HEAD','PUT','DELETE'])
def homepage(hostname="NA"):
    for header in request.headers:
        for field in header:
            if "${" in field:
                reportHit(request)
    if request.method == 'POST':
        for fieldname, value in request.form.items():
            if "${" in value:
                reportHit(request)
        return("<html><head><title>Login Failed</title></head><body><h1>Login Failed</h1><br/><a href='/'>Try again</a></body></html>")
    else:
        return(login_form)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=honeypot_port)
