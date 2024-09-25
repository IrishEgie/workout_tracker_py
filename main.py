import requests
from datetime import datetime
from config import *

# Replace these placeholders with actual values or environment variables
GENDER = "male"  # Example: "female"
WEIGHT_KG = 55.6  # Example: 55.6
HEIGHT_CM = 160  # Example: 160
AGE = 22  # Example: 22

# Nutritionix and Sheety API endpoints
exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = f"https://api.sheety.co/{SHEET_ID}/exerciseTrackerPySheet/sheet1"

# Ask for input regarding the exercises
exercise_text = input("Tell me which exercises you did: ")

# Nutritionix API headers
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "Content-Type": "application/json"
}

# Parameters for the Nutritionix API
parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

# Make the request to Nutritionix API
response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(result)
# Get the current date and time
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# Sheety API Bearer token from config file
bearer_headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Iterate through each exercise and send it to Google Sheets via Sheety API
for workout in result['exercises']:
    sheet_inputs = {
        "sheet1": {  # Ensure that 'workout' matches the structure expected by your Sheety setup
            "date": today_date,
            "time": now_time,
            "exercise": workout["name"].title(),
            "duration": workout["duration_min"],
            "calories": workout["nf_calories"]
        }
    }

    # Send each exercise as a new row in the Google Sheet
    sheet_response = requests.post(url=sheet_endpoint, json=sheet_inputs, headers=bearer_headers)

    # Print the response from Sheety to verify it was logged successfully
    print(sheet_response.text)
