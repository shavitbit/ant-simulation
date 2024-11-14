import requests
import json

## Define the URL of the Flask API
url = 'http://127.0.0.1:5000/api/v1/'

# Define the data you want to send in the POST request
data = {
    'id': '40.0-2.5-1.0-7.0',
    'sim_result': 150.4,
    'runs': 6
}

# Send the POST request to the Flask API
response = requests.post(url+"send_sim_result", json=data)

# Print the response from the server
if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.json())

#response = requests.get(url+"get_sim_summary")
## Print the response from the server
#if response.status_code == 200:
#    print("Success:", response.json())
#else:
#    print("Error:", response.json())

#sim_id = "20.0-1.5-1.0-5.0"
#response = requests.get(url+f"get_sim_result/{sim_id}")
#if response.status_code == 200:
#    print("Success:", response.json())
#else:
#    print("Error:", response.json())