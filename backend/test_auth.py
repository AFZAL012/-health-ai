import urllib.request
import json
import urllib.error

url = 'http://127.0.0.1:5000/api/v1/auth/register'
data = json.dumps({'email':'patient@example.com', 'password':'SecurePass123!', 'role':'patient'}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

try:
    response = urllib.request.urlopen(req)
    print(response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
    print(e.read().decode('utf-8'))
except Exception as e:
    print(e)
