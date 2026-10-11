# ✈️ TravelMate AI — Your Personal Audio Tour Guide

**TravelMate AI** is an AI-powered travel guide that transforms destinations into engaging travel stories and audio experiences. Explore famous landmarks, discover local history and culture, and listen to personalized guides in your preferred language.

🌐 **Live Demo:** [TravelMate AI](https://travelguide-dm3jk58bkrkocrqxalnamb.streamlit.app/)

💻 **GitHub Repository:** [TravelGuide](https://github.com/sandya-coder/TravelGuide)

---

## 🌍 Project Overview

Planning a trip often involves searching across multiple websites to learn about destinations, historical landmarks, cultural attractions, and interesting facts.

TravelMate AI simplifies this experience by generating personalized travel stories using Google Gemini and converting them into audio narration using Murf AI.

Users can enter a destination, select a language, choose a story length, and generate an audio travel guide that they can listen to or download.

## ✨ Features

- 🗺️ **AI-Powered Travel Stories:** Generate engaging information about destinations, landmarks, culture, history, and attractions.
- 🎧 **Audio Tour Generation:** Convert generated travel stories into speech using Murf AI.
- 🌐 **Multilingual Support:** Select English, Hindi, Tamil, or Telugu.
- 📖 **Customizable Guides:** Choose between Quick Summary and Detailed Story.
- 📍 **Destination Suggestions:** Explore suggestions such as the Taj Mahal, Bali, Paris, and the Grand Canyon.
- 📥 **Downloadable Audio:** Download the generated audio guide in MP3 format.
- 🎨 **Modern User Interface:** A responsive, travel-inspired interface with destination images, feature cards, and accessible text colors.
- 🔐 **Secure API Configuration:** Store API credentials in Streamlit Secrets rather than hardcoding them into the application.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application programming |
| Streamlit | Web application and user interface |
| Google Gemini API | AI-generated travel stories |
| Google Gen AI SDK | Connects the application to Gemini |
| Murf AI API | Text-to-speech audio generation |
| Requests | HTTP requests to the Murf API |
| HTML and CSS | Interface styling |
| Streamlit Community Cloud | Application hosting |
| Git and GitHub | Source control and deployment workflow |

## ⚙️ How It Works

1. **Choose a destination:** Enter a place you want to explore or select a suggested destination.
2. **Customize your guide:** Select your preferred language and guide style.
3. **Generate the story:** Google Gemini generates a destination-specific travel narrative.
4. **Create the audio:** Murf AI converts the story into speech.
5. **Listen and download:** Play the audio directly in the application or download the MP3 file.

## 🚀 Getting Started

### Prerequisites

Make sure you have:

- Python 3.10 or a compatible Python version.
- Git installed on your computer.
- A Google Gemini API key.
- A Murf AI API key.
- A Murf voice ID supported by your account and selected language.

### 1. Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/sandya-coder/TravelGuide.git
cd TravelGuide
```

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` file should include:

```text
streamlit
google-genai
requests
```

### 4. Configure API Keys

For local development, create a folder named `.streamlit` in the project root. Inside it, create a file named `secrets.toml`.

Add the following configuration, replacing the example values with your own API keys:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
MURF_AI_API_KEY = "your_murf_api_key"
```

**Security note:** Never commit real API keys to GitHub. Keep `secrets.toml` private and add it to `.gitignore`.

For the deployed application, configure the same secret names in your Streamlit Community Cloud app settings.

### 5. Run the Application

From the project root, run:

```bash
streamlit run streamlit_app.py
```

The application will open in your browser at the local address displayed in the terminal, usually:

`http://localhost:8501`

## 🔑 API Configuration

### Google Gemini API
Used to generate travel stories based on the user's destination, chosen language, and selected guide style.

### Murf AI API
Used to transform the generated story into audio narration. A compatible Murf voice ID is required.

API availability, supported voices, language compatibility, and usage limits depend on the respective providers and account configuration.

## 📂 Project Entry Points

- `streamlit_app.py` — Main Streamlit application, user interface, AI story generation, and audio generation.
- `requirements.txt` — Python dependencies.
- `README.md` — Project documentation.
- `Backend/` — Additional backend project files, if used in your repository.
- `Frontend/` — Additional frontend project files, if used in your repository.

## 🔒 Security and Limitations

- Store API credentials in Streamlit Secrets or local environment-specific configuration.
- Do not publish API keys, passwords, or private credentials.
- AI-generated travel information should be verified before relying on it for bookings, opening hours, safety guidance, or travel decisions.
- Audio generation requires a working Murf API connection and a compatible voice ID.
- Generated content and audio length may be limited by the API providers' current service and account limits.

## 🔮 Future Enhancements

- Interactive maps and route planning.
- Personalized itineraries based on budget, interests, and available time.
- Local food recommendations and hidden attractions.
- More regional languages and voice options.
- Save and revisit previously generated travel guides.
- Offline access to downloaded audio guides.
- Location-aware narration and nearby attraction suggestions.

## 🎯 Project Goal

The goal of TravelMate AI is to make discovering destinations more engaging, accessible, and convenient by combining artificial intelligence with personalized audio experiences.

**TravelMate AI — Discover more. Travel deeper. Listen to every story.** ✈️

---

*Built with Python, Streamlit, Google Gemini, and Murf AI.*
