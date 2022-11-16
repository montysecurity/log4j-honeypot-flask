# log4j-honeypot-flask

## Changes Made to this Fork

Here is a list of changes made compared to the repo managed by BinaryDefense.

- Removed webhook functionality
- Removed docker functionality
- Added local logging functionality
- Changed defalt port to 80
- Created `setup.sh` to instal dependencies and launch the app
- Removed *requests* from `requirements.txt`

## Why the Changes?

I wanted to make a version that could be stood up with one command and not require Slack/Teams as a notification platform

## Setup

`sudo bash setup.sh`

## Use Case

This is a CVE-2021-44228 (Log4J) honeypot

Important Note: This is a LOW-INTERACTION honeypot meant for internal active defense. It is not supposed to be vulnerable or let attackers get into anything.

All it does is watch for suspicious string patterns in the requests (form fields and HTTP headers) and log them to `log.txt`

## Credit

Of course thank you to BinaryDefense for the original code. 
