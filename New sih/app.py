from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
import google.generativeai as genai
import os
import aiResponse
import random
import uuid
import requests
import csv
import time


import pandas as pd


app = Flask(__name__)

genai.configure(api_key='Api_Key')

csv_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vROnMBbf_ZIX1Q2VaaXV4t_M0M86mQsJmxGWbeZhJfMXT7vcTOd8pnNbT5rOa4W9QqHPJGhLSWPWzaS/pub?output=csv'

app.config["SECRET_KEY"] = "LOL420"
csv_File = 'C://Users//abhin//Desktop//abhinav//New sih//Cleaned_Book1.csv'

def generate_unique_id():
    return str(uuid.uuid4())

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['GET','POST'])
def chat():
    data = session.get('data', [])

    if request.method == "POST":
        input_text = request.json.get("text")  # Get the text from the JSON request
        if input_text:
            message_id = generate_unique_id()
            model = genai.GenerativeModel(model_name="gemini-pro")
            
            # Generate responses based on input
            user_greet = model.generate_content(f"{input_text} is related to greeting, only answer in one word yes or no")
            user_greet = user_greet.text.strip().lower()

            if user_greet == "yes":
                # Return a random greeting
                response = random.choice(aiResponse.greetingL)
                text_result = response
            else:
                # Generate a response based on the input
                response = model.generate_content(input_text)
                text_result = response.text.strip() if response else "I am not able to help you with this. Sorry"
            
            # Save the user's message and the response
            data.append({'id': message_id, 'text': input_text, 'response': text_result})
            session['data'] = data
            
            return jsonify({'response': text_result})  # Return the AI response as JSON
        else:
            return jsonify({'error': 'Please provide a valid input!'}), 400

    return render_template("chat.html", data=data[::-1])




# Replace with your actual CSV URL
csv_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vROnMBbf_ZIX1Q2VaaXV4t_M0M86mQsJmxGWbeZhJfMXT7vcTOd8pnNbT5rOa4W9QqHPJGhLSWPWzaS/pub?output=csv'

def fetch_csv_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors
    return response.text.splitlines()

# Function to read and store the last row of CSV data
def get_last_sensor_data(url):
    lines = fetch_csv_data(url)
    csv_reader = csv.DictReader(lines)

    # Store the last row of the CSV
    last_row = None
    for row in csv_reader:
        last_row = row

    return last_row


@app.route('/sensor')

def sensor():
    # Fetch the latest sensor data
    while True:
        last_sensor_data = get_last_sensor_data(url=csv_url)

        try:
            if last_sensor_data:
                sensor_data = {
                    'timestamp' : last_sensor_data["timestamp"], #
                    'ph_mv': last_sensor_data["ph_mv"], #
                    'water_temp_c' : last_sensor_data["water_temp_c"],#
                    'water_flow_l_min' : last_sensor_data["water_flow_l_min"],
                    'turbidity_v' : last_sensor_data["turbidity_v"],#
                    'tds_mv' : last_sensor_data["tds_mv"],#
                    'humidity_percent' : last_sensor_data["humidity_percent"],#
                }

                return render_template('sensor.html', sensor_data=sensor_data)
            else:
                return render_template('sensor.html', error='No data found')
        except requests.exceptions.RequestException as e:
            return render_template('sensor.html', error=f'Error fetching data: {e}')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9693)