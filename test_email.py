"""
Test script to verify Gmail SMTP email configuration.
Run this to test if emails can be sent successfully.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apartment.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    """Test sending an email via Gmail SMTP"""
    print("=" * 50)
    print("Testing Gmail SMTP Configuration")
    print("=" * 50)
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
    print("=" * 50)
    
    # Test email (change to your own email for testing)
    test_email_address = settings.EMAIL_HOST_USER  # Send to yourself
    test_code = "123456"  # Test 6-digit code
    
    try:
        print(f"\n[SENDING] Sending test email to {test_email_address}...")
        
        subject = "Test Password Reset Code - Monterde Apartment"
        message = f"""Hello,

This is a test email to verify Gmail SMTP configuration.

Your test password reset code is: {test_code}

This code will expire in 15 minutes.

Best regards,
Monterde Apartment Team"""
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [test_email_address],
            fail_silently=False,
        )
        
        print("[SUCCESS] Test email sent successfully!")
        print(f"   Check your inbox at {test_email_address}")
        print(f"   Test code: {test_code}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to send email")
        print(f"   Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure python-dotenv is installed: pip install python-dotenv")
        print("2. Check that .env file exists with correct credentials")
        print("3. Verify Gmail App Password is correct (no spaces)")
        print("4. Ensure 2-Step Verification is enabled on Gmail")
        print("5. Check that 'Less secure app access' is enabled (if applicable)")
        return False

if __name__ == "__main__":
    test_email()

