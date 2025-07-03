import os
import resend

def send_reset_email(user_email, reset_url):
    # Securely read the secret from the mounted file path
    if "RESEND_KEY_FILE" in os.environ:
        with open(os.environ["RESEND_KEY_FILE"]) as f:
            resend.api_key = f.read().strip()
    else:
        raise RuntimeError("Missing RESEND_KEY_FILE environment variable")

    return resend.Emails.send({
        "from": os.getenv("EMAIL_SENDER", "support@market.devmode.art"),
        "to": user_email,
        "subject": "Reset your password",
        "html": f"<p>Click below to reset your password:</p><a href='{reset_url}'>{reset_url}</a>"
    })
