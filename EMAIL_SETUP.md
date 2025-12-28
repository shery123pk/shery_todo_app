# Email Task Reminders Setup Guide

## Overview
Get email notifications when your tasks are due! Receive beautiful reminder emails 30 minutes before your task deadline.

## Features
- ✅ Create tasks with due dates using natural language ("tomorrow 3pm", "next Monday 9am")
- ✅ Automatic email reminders 30 minutes before task is due
- ✅ Beautiful HTML email templates
- ✅ Works with Gmail, Outlook, or any SMTP provider
- ✅ Simple task numbers (1, 2, 3) for easy deletion

## Quick Setup (5 Minutes)

### Option 1: Gmail (Recommended - Free)

#### Step 1: Enable 2-Factor Authentication
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Click "2-Step Verification"
3. Follow the steps to enable it (required for App Passwords)

#### Step 2: Create App Password
1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select "Mail" and "Other (Custom name)"
3. Name it "TaskFlow"
4. Click "Generate"
5. **Copy the 16-character password** (you'll need it in Step 3)

#### Step 3: Configure Backend
Edit `backend/.env` file and add:

```bash
# Email Notifications
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
FROM_EMAIL=your-email@gmail.com
```

**Replace:**
- `your-email@gmail.com` - Your Gmail address
- `your-16-char-app-password` - The password from Step 2

#### Step 4: Restart Backend
```bash
cd backend
# Backend will automatically detect email credentials
```

That's it! You're done! 🎉

### Option 2: Outlook/Hotmail

```bash
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your-email@outlook.com
SMTP_PASSWORD=your-password
FROM_EMAIL=your-email@outlook.com
```

### Option 3: Other Email Providers

**Yahoo:**
```bash
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
```

**Custom SMTP:**
```bash
SMTP_HOST=smtp.yourprovider.com
SMTP_PORT=587  # or 465 for SSL
```

## How to Use

### Creating Tasks with Reminders

Open the chatbot (purple button) and use natural language:

**Examples:**
```
"Add call dentist tomorrow at 3pm"
"Create buy groceries task for next Monday 9am"
"Add finish report due in 2 hours"
"Remind me to workout tomorrow morning at 7am"
```

The AI will:
1. Parse the date and time
2. Create the task
3. Set up an email reminder for 30 minutes before

### Deleting Tasks by Number

No complex IDs needed! Just use numbers:

```
"Delete task 1"
"Remove the first task"
"Delete task 3"
```

### Viewing Tasks

```
"Show me all my tasks"
"What tasks are due soon?"
"Show my incomplete tasks"
```

## Email Examples

### Reminder Email (30 min before due)
```
Subject: 🔔 Task Reminder: Call dentist

You have a task due soon:

📌 Call dentist
⏰ Due: December 30, 2025 at 03:00 PM

Don't forget to complete this task!
```

### Confirmation Email (When task created)
```
Subject: ✅ Task Created: Call dentist

Your task has been created:

📌 Call dentist
⏰ Reminder: December 30, 2025 at 02:30 PM

You'll receive a reminder email 30 minutes before it's due.
```

## Testing

Try this in the chatbot:

```
"Add test reminder for 5 minutes from now"
```

Wait 5 minutes and check your email inbox! You should see a beautiful reminder email.

## Troubleshooting

### Not Receiving Emails?

1. **Check Spam/Junk folder** - First reminder might land there
2. **Verify credentials** - Double-check your email and app password
3. **Check backend logs** - Look for "[SUCCESS] Email notifications enabled"
4. **Gmail App Password** - Make sure 2FA is enabled first

### "Email notifications disabled"

- SMTP credentials are missing or commented out
- Check your `.env` file has all fields uncommented and filled

### Gmail "Less secure app" error

- Use App Password instead of regular password
- Enable 2-Factor Authentication first
- Don't use your regular Gmail password

### Emails going to spam

- Add FROM_EMAIL to your contacts
- Mark first email as "Not Spam"
- Future emails will go to inbox

## How It Works

1. **You create a task** with due date via chatbot
2. **Background service** checks every 10 minutes for upcoming tasks
3. **30 minutes before** due time, email is sent to your registered email
4. **Beautiful HTML email** arrives in your inbox
5. **Never miss a deadline** again!

## Email Templates

Emails include:
- 🔔 Attractive subject lines
- 📌 Task title prominently displayed
- ⏰ Due date/time in readable format
- 🎨 Beautiful HTML design with gradients
- 📱 Mobile-friendly responsive design

## Cost

**100% FREE**
- No subscriptions
- No API fees
- Just use your existing email account

## Security

- App Passwords are safer than using your main password
- Passwords stored only in your `.env` file (not committed to git)
- SMTP connection uses TLS encryption
- Your email provider handles all security

## Need Help?

**Gmail App Password issues:**
- [Google App Passwords Guide](https://support.google.com/accounts/answer/185833)
- Make sure 2FA is enabled first

**Other providers:**
- Check your email provider's SMTP settings
- Most use port 587 with STARTTLS

---

Enjoy your email task reminders! Never miss a deadline again! 📧🎉
