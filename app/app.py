from flask import Flask, redirect, url_for, request
import json
import os

#### Set the name of this honeypot instance here, or in environment variable HONEYPOT_NAME ####
# (use a descriptive name so you know when alerts come in where they were triggered)
honeypot_name = "My log4j honeypot"

#### Set the port you want this honeypot to listen on. Recommend 8080 or 80
#### you can also use environment variable HONEYPOT_PORT
honeypot_port = 80

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
    log = open("log.txt", "a")
    log.write("Alert from log4j honeypot " + honeypot_name + "\n")
    log.write("Suspicious request received from IP: "+ request.remote_addr + "\n")
    log.write("Review HTTP headers for payloads:\n")
    for header in request.headers:
        log.write(str(header) + "\n")
    for fieldname, value in request.form.items():
        log.write(str((fieldname, value)) + "\n")
    log.write("\n----------------------------------------\n")
    log.close()

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
        print(header)
        for field in header:
            if "${" in field:
                reportHit(request)
    if request.method == 'POST':
        for fieldname, value in request.form.items():
            print(value)
            if "${" in value:
                reportHit(request)
        return("<html><head><title>Login Failed</title></head><body><h1>Login Failed</h1><br/><a href='/'>Try again</a></body></html>")
    else:
        return(login_form)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=honeypot_port)
