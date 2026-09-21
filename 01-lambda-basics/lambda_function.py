def lambda_handler(event,context):
  username=event["username"]
  action=event["action"]
  mfa_enabled=event["mfa_enabled"]


  if mfa_enabled==False:
    print(f"Security-alert ‼️ {username} logged in without MFA")
  else:
    print(f"Logged in Approved {username}")
