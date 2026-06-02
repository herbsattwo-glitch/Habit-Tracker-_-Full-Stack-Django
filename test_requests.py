import requests

# Disable auto-redirects so we can see where Django is sending us
r = requests.get("http://127.0.0.1:8000", allow_redirects=False)

print("Status:", r.status_code)
print("Redirect target:", r.headers.get("Location"))
