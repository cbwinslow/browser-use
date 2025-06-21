# Automated API Registration Workflow

This example demonstrates how to use **browser-use** to sign up for an account on a website, verify the registration through an email inbox, and generate an API key. The workflow relies on environment variables to provide the target URLs and email credentials.

## Environment Variables
- `SITE_SIGNUP_URL` – URL of the site's sign-up page.
- `API_SETTINGS_URL` – URL where a new API key can be generated after account verification.
- `REG_EMAIL` – Email address used for registration.
- `REG_EMAIL_PASSWORD` – Password for the email account (required if using IMAP to retrieve the verification link).

Ensure you comply with each website's terms of service before automating registrations.

Run the example with:
```bash
python auto_api_registration.py
```
