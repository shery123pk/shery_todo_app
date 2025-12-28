# WhatsApp Task Reminders Setup Guide

## Overview
Get WhatsApp notifications when your tasks are due! This feature uses Twilio to send task reminders directly to your WhatsApp.

## Features
- ✅ Create tasks with due dates using natural language ("tomorrow 3pm", "next Monday 9am")
- ✅ Automatic WhatsApp reminders 30 minutes before task is due
- ✅ Works with simple task numbers (1, 2, 3) instead of complex IDs
- ✅ Natural language commands via AI chatbot

## Setup Steps

### 1. Get Twilio Account (Free Trial Available)

1. Go to [Twilio](https://www.twilio.com/try-twilio)
2. Sign up for a free account
3. You'll get **$15 in free credit** - enough for testing!

### 2. Get Your Twilio Credentials

1. After signing up, go to [Twilio Console](https://console.twilio.com)
2. Copy your **Account SID** and **Auth Token**
3. Save these for step 4

### 3. Set Up WhatsApp Sandbox (For Testing)

**Option A: Twilio Sandbox (Easiest - No Business Account Needed)**

1. Go to [Twilio WhatsApp Sandbox](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn)
2. You'll see a number like `+1 415 523 8886`
3. **Join the sandbox**: Send a WhatsApp message from your phone to that number with the code shown (e.g., "join <your-code>")
4. You should receive a confirmation message

**Option B: WhatsApp Business API (For Production)**
- Requires WhatsApp Business Account approval
- Takes 1-3 days for approval
- Follow [Twilio WhatsApp Business Setup](https://www.twilio.com/docs/whatsapp/tutorial/connect-number-business-profile)

### 4. Configure Backend

Edit `backend/.env` file and add:

```bash
# Twilio WhatsApp Notifications
TWILIO_ACCOUNT_SID=your-account-sid-here
TWILIO_AUTH_TOKEN=your-auth-token-here
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
USER_WHATSAPP_NUMBER=whatsapp:+YOUR_PHONE_NUMBER
```

**Important**:
- Replace `your-account-sid-here` with your actual Account SID
- Replace `your-auth-token-here` with your actual Auth Token
- Replace `+YOUR_PHONE_NUMBER` with your phone number (format: +1234567890)
- Keep the `whatsapp:` prefix!

### 5. Restart Backend

```bash
cd backend
# Backend will automatically detect Twilio credentials and enable WhatsApp
```

## How to Use

### Creating Tasks with Due Dates

Open the chatbot (purple button) and use natural language:

**Examples:**
```
"Add call dentist tomorrow at 3pm"
"Create buy groceries task for next Monday 9am"
"Add finish report due in 2 hours"
"Remind me to workout tomorrow morning"
```

The AI will automatically parse the date/time and set reminders!

### Deleting Tasks by Number

No need for complex IDs! Just use task numbers:

```
"Delete task 1"
"Remove the first task"
"Delete the third task"
```

The chatbot shows tasks with numbers (1, 2, 3...) and remembers which task is which.

### Viewing Tasks with Due Dates

```
"Show me all my tasks"
"What tasks are due soon?"
"Show my incomplete tasks"
```

## How Reminders Work

1. **You create a task** with a due date via chatbot
2. **Background service checks** every 10 minutes for upcoming tasks
3. **30 minutes before due time**, you get a WhatsApp message like:

```
🔔 Task Reminder

📌 Call dentist

⏰ Due: 2025-12-30 15:00

Don't forget to complete this task!

---
TaskFlow AI Assistant
```

## Testing

Try this in the chatbot:

```
"Add test reminder task for 5 minutes from now"
```

Wait 5 minutes and you should get a WhatsApp reminder!

## Troubleshooting

### Not Receiving Messages?

1. **Check Sandbox Join**: Make sure you joined the Twilio sandbox by sending the join code
2. **Check Phone Number**: Ensure it includes country code (+1234567890)
3. **Check Credentials**: Verify Account SID and Auth Token are correct
4. **Check Backend Logs**: Look for "[SUCCESS] Twilio WhatsApp client initialized"

### "WhatsApp notifications disabled"

- Twilio credentials are missing or incorrect
- Check your `.env` file has all required fields uncommented

### Free Trial Limits

- Twilio free trial: $15 credit (~1000 messages)
- Sandbox: Only works with numbers that joined the sandbox
- Production: Requires WhatsApp Business approval

## Cost

**Free Tier:**
- Twilio gives $15 free credit
- WhatsApp messages cost ~$0.005 each
- That's about 3000 free messages!

**After Free Tier:**
- WhatsApp: $0.005 per message
- Very affordable for personal use

## Need Help?

Check Twilio docs:
- [Twilio WhatsApp Quickstart](https://www.twilio.com/docs/whatsapp/quickstart)
- [Twilio Console](https://console.twilio.com)
- [Get Help](https://support.twilio.com)

---

Enjoy your WhatsApp task reminders! 🎉
