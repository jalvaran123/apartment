# Password Reset Email System - Setup Complete ✅

## Overview
The password reset email system has been fully configured with Gmail SMTP integration.

## What Was Set Up

### 1. **Database Model**
- ✅ `PasswordResetCode` model created with:
  - 6-digit code generation
  - 15-minute expiry
  - Rate limiting (IP tracking)
  - Security indexes

### 2. **Email Configuration**
- ✅ Gmail SMTP configured in `settings.py`
- ✅ Uses `cmookie@gmail.com` as sender
- ✅ App Password configured: `xqmlgqcybgphcmjz` (spaces removed)
- ✅ Environment variables loaded from `.env` file

### 3. **Backend Endpoint**
- ✅ `/auth/request-reset/` endpoint created
- ✅ Generates 6-digit codes
- ✅ Sends emails via Gmail SMTP
- ✅ Rate limiting: 3 requests per hour per IP
- ✅ Security: Doesn't reveal if email exists

### 4. **Frontend Integration**
- ✅ Forgot password page updated
- ✅ Uses `fetch()` to send POST requests
- ✅ Displays success/error messages
- ✅ Loading states and validation

### 5. **.env File**
- ✅ Automatically created at project root
- ✅ Contains Gmail credentials
- ✅ Loaded automatically on Django startup

## Files Modified/Created

1. `accounts/models.py` - Added PasswordResetCode model
2. `accounts/views.py` - Added password reset endpoint
3. `accounts/templates/accounts/forgot_password.html` - Updated frontend
4. `apartment/settings.py` - Email configuration
5. `apartment/urls.py` - URL routing
6. `.env` - Gmail credentials (auto-created)
7. `requirements.txt` - Added python-dotenv
8. `test_email.py` - Test script created

## Email Configuration Details

```
EMAIL_BACKEND = django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST = smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = cmookie@gmail.com
EMAIL_HOST_PASSWORD = xqmlgqcybgphcmjz (App Password)
DEFAULT_FROM_EMAIL = cmookie@gmail.com
```

## Testing the Setup

### Option 1: Use the Test Script
```bash
python test_email.py
```

### Option 2: Test via Web Interface
1. Start Django server: `python manage.py runserver`
2. Visit: `http://localhost:8000/forgot-password/`
3. Enter an email address
4. Click "Send Reset Link"
5. Check the inbox for the 6-digit code

## Troubleshooting Email Issues

If you see "Username and Password not accepted" error:

1. **Verify Gmail App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - Make sure 2-Step Verification is enabled
   - Generate a new App Password if needed
   - Update `.env` file with the new password (no spaces)

2. **Check .env File**:
   - Location: Project root (same directory as manage.py)
   - Should contain:
     ```
     EMAIL_HOST_USER=cmookie@gmail.com
     EMAIL_HOST_PASSWORD=xqmlgqcybgphcmjz
     DEFAULT_FROM_EMAIL=cmookie@gmail.com
     ```

3. **Verify App Password Format**:
   - App passwords are 16 characters
   - Should have NO spaces: `xqmlgqcybgphcmjz`
   - Not the regular Gmail password

4. **Check Gmail Settings**:
   - 2-Step Verification MUST be enabled
   - App Password must be generated specifically for "Mail"
   - Regular password will NOT work

## Security Features

- ✅ Rate limiting (3 requests/hour per IP)
- ✅ Code expiry (15 minutes)
- ✅ No email enumeration (always returns success)
- ✅ CSRF protection
- ✅ IP address tracking
- ✅ Secure code storage

## Next Steps

1. **Run Migrations** (if not done):
   ```bash
   python manage.py migrate
   ```

2. **Test Email Sending**:
   ```bash
   python test_email.py
   ```

3. **Verify Email Receives**:
   - Check `cmookie@gmail.com` inbox
   - Check Spam folder if not in inbox
   - Verify code format: 6 digits

4. **Production Deployment**:
   - Keep `.env` file secure (don't commit to git)
   - Add `.env` to `.gitignore`
   - Use environment variables on production server

## URL Endpoints

- `/forgot-password/` - Forgot password page
- `/auth/request-reset/` - API endpoint for sending reset codes

## Code Flow

1. User enters email → Frontend sends POST to `/auth/request-reset/`
2. Backend generates 6-digit code → Stores in database
3. Backend sends email via Gmail SMTP → User receives code
4. Success message displayed → User can verify code later

The system is ready to use! 🚀

