# ✈️ Agentic AI-Based Travel Planning Assistant

## Project Overview
The Agentic AI-Based Travel Planning Assistant is a Python-based web application designed to simplify travel planning. It helps users select destinations, explore flights and hotels, discover tourist attractions, check weather conditions, and estimate their travel budget.

The application uses a Streamlit interface and travel datasets in JSON format to generate personalized travel plans based on user preferences.

## Problem Statement
Planning a trip requires travelers to compare flights, hotels, tourist attractions, weather conditions, and expenses across multiple platforms. This process is time-consuming and often results in inefficient travel plans.

This project simplifies the process by providing travel recommendations and a structured itinerary through a single application.

## Objectives
- Recommend flights based on source and destination.
- Suggest suitable hotels based on travel preferences.
- Discover tourist attractions based on user interests.
- Retrieve weather information using a free weather API.
- Generate day-wise travel itineraries.
- Estimate total trip expenses.
- Provide a simple and interactive travel-planning interface.

## Features
- Flight recommendation system.
- Hotel recommendation system.
- Tourist places discovery.
- Live weather integration.
- Day-wise itinerary generation.
- Travel budget estimation.
- Budget, travel duration, destination and interest-based inputs.
- Interactive Streamlit dashboard.

## Technologies Used
- Python
- Streamlit
- JSON
- Requests
- Open-Meteo Weather API
- VS Code

## Project Structure
```text
Agentic-AI-Travel-Planning-Assistant/
│
├── app.py
├── data/
│   ├── flights.json
│   ├── hotels.json
│   └── places.json
│
├── requirements.txt
└── README.md
```

## Weather API
Weather forecasts are retrieved using the free Open-Meteo API.

Website: https://open-meteo.com/

No API key is required for the weather API.

## Installation & Setup

### 1. Clone the repository
```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Agentic-AI-Travel-Planning-Assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
streamlit run app.py
```

The application will open in your browser.

## How to Use
1. Enter your starting city.
2. Select your destination.
3. Choose the number of travel days.
4. Set your estimated budget.
5. Select your travel style.
6. Choose your preferred interests.
7. Click Generate My Trip.
8. View flights, hotel recommendations, weather, itinerary, and budget breakdown.

## Business Use Cases
- Travel agencies
- Tourism companies
- Online travel platforms
- Hotel recommendation systems
- Personalized travel services

## Future Enhancements
- Integrate an LLM-powered LangChain agent.
- Add real-time flight and hotel APIs.
- Implement route and distance optimization.
- Add downloadable PDF itineraries.
- Support additional destinations and advanced personalization.

## Disclaimer
This project is developed for educational and demonstration purposes. Flight, hotel and attraction information may contain sample data and estimated prices. It is not a live booking platform.

## Author
Developed as a Python and AI travel-planning project.
