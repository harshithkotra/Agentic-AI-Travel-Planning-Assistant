
# ✈️ Agentic AI-Based Travel Planning Assistant

## Project Overview
The AI-Based Travel Planning Assistant is a Python-based web application designed to simplify travel planning. It helps users explore flights, hotels, tourist attractions, weather conditions, and estimated travel expenses in one place.

The application uses Streamlit for its interactive interface and JSON datasets to provide travel recommendations based on user preferences.

## Problem Statement
Planning a trip involves comparing flights, accommodation, tourist destinations, weather conditions, and expenses across multiple platforms. This can be time-consuming and difficult for travelers.

This project aims to simplify the process by providing travel recommendations, estimated budgets, and a structured itinerary through a single application.

## Objectives
- Recommend flights based on source and destination.
- Suggest hotels based on location and travel preferences.
- Discover tourist attractions based on user interests.
- Retrieve weather forecasts using a weather API.
- Generate a day-wise travel itinerary.
- Estimate total travel expenses.
- Provide an interactive and user-friendly interface.

## Features
- Flight search and recommendations
- Hotel recommendations
- Tourist places discovery
- Weather forecast integration
- Day-wise itinerary generation
- Travel budget estimation
- Destination and travel preference selection
- Interactive Streamlit dashboard

## Technologies Used
- Python
- Streamlit
- JSON
- Requests
- Open-Meteo API
- Visual Studio Code

## Project Structure
```text
Travel-Planning-Agent/
│
├── app.py
├── requirements.txt
├── data/
│   ├── flights.json
│   ├── hotels.json
│   └── places.json
├── tools/
│   └── travel_tools.py
├── agent/
│   └── travel_agent.py
└── README.md
```

## Weather API
Weather information is retrieved through the Open-Meteo API.

Website: https://open-meteo.com/

Open-Meteo provides weather data without requiring an API key for this project's usage.

## Installation and Setup

### 1. Clone the repository
```bash
git clone https://github.com/harshithkotra/Agentic-AI-Travel-Planning-Assistant.git
cd Agentic-AI-Travel-Planning-Assistant
```

### 2. Create a virtual environment
```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows:
```bash
.venv\Scripts\activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the application
```bash
streamlit run app.py
```

The application will open in your default browser.

## How to Use
1. Enter your starting city.
2. Select your destination.
3. Choose the number of travel days.
4. Set your travel budget.
5. Select your preferred travel style.
6. Choose your travel interests.
7. Click **Generate My Trip**.
8. Explore your recommended flights, hotels, attractions, weather, itinerary, and budget breakdown.

## Use Cases
- Travel planning
- Tourism recommendation systems
- Travel agencies
- Hotel discovery
- Personalized trip planning

## Future Enhancements
- Integrate an LLM-powered LangChain agent for autonomous tool selection.
- Connect real-time flight and hotel APIs.
- Add distance and route optimization.
- Provide downloadable travel itineraries.
- Expand destinations and recommendation capabilities.

## Disclaimer
This project is developed for educational and demonstration purposes. Flight, hotel, and attraction information may use sample datasets and estimated prices. The application is not a live booking platform.

## Author
Developed as a Python-based travel planning and AI application project.
