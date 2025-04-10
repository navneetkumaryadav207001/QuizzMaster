from tasks import send_daily_reminders

users = send_daily_reminders()
for user in users:
    print(user)