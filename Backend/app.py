
import os
import base64
import logging
import requests

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai

# Load API keys from Backend/.env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MURF_AI_API_KEY = os.getenv("MURF_AI_API_KEY")

app = Flask(__name__)
CORS(app)

# Limit incoming request size
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

logging.basicConfig(level=logging.INFO)

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

PROMPTS = {
    "Summary": (
        "Act as a professional tourist guide. Explain the history, "
        "importance, famous attractions, and interesting facts about "
        "{place}. Write approximately 150 words in {language}. "
        "Use simple, engaging language. Do not invent facts."
    ),
    "Detailed": (
        "Act as a professional tourist guide. Give an engaging, detailed "
        "account of {place}, including history, architecture, cultural "
        "importance, attractions, and visitor insights. Write approximately "
        "300 words in {language}. Use clear language and do not invent facts."
    )
}


@app.get("/")
def home():
    return jsonify({
        "message": "AI Travel Guide backend is running!"
    })


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "geminiConfigured": bool(GEMINI_API_KEY),
        "murfConfigured": bool(MURF_AI_API_KEY)
    })


@app.post("/generate-audio-guide")
def generate_audio_guide():
    try:
        data = request.get_json(silent=True) or {}

        place = str(data.get("place", "")).strip()
        answer_type = str(data.get("answerType", "Summary")).strip()
        language = str(data.get("language", "English")).strip()
        voice_id = str(data.get("voiceId", "")).strip()
        locale = str(data.get("locale", "")).strip()

        # Validate inputs
        if not place or len(place) > 200:
            return jsonify({
                "error": "Enter a destination (up to 200 characters)."
            }), 400

        if answer_type not in PROMPTS:
            return jsonify({
                "error": "Choose Summary or Detailed."
            }), 400

        if not language:
            return jsonify({
                "error": "Choose a language."
            }), 400

        if not voice_id or not locale:
            return jsonify({
                "error": "Enter a valid Murf voice ID and locale."
            }), 400

        if not client:
            return jsonify({
                "error": "Gemini API key missing in Backend/.env."
            }), 500

        if not MURF_AI_API_KEY:
            return jsonify({
                "error": "Murf API key missing in Backend/.env."
            }), 500

        # Step 1: Generate the travel description with Gemini
        prompt = PROMPTS[answer_type].format(
            place=place,
            language=language
        )

        gemini_response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        description = (gemini_response.text or "").strip()

        if not description:
            raise RuntimeError("Gemini returned no description.")

        # Step 2: Convert the description into speech using Murf
        murf_response = requests.post(
            "https://global.api.murf.ai/v1/speech/stream",
            headers={
                "api-key": MURF_AI_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "voice_id": voice_id,
                "text": description,
                "locale": locale,
                "model": "FALCON",
                "format": "MP3",
                "sampleRate": 24000,
                "channelType": "MONO"
            },
            timeout=120
        )

        if murf_response.status_code != 200:
            app.logger.error(
                "Murf returned HTTP %s: %s",
                murf_response.status_code,
                murf_response.text[:500]
            )

            return jsonify({
                "error": (
                    f"Murf API returned HTTP {murf_response.status_code}. "
                    "Check the API key, credits, voice ID, locale, "
                    "and request format."
                )
            }), 502

        audio_bytes = murf_response.content

        if not audio_bytes:
            raise RuntimeError("Murf returned empty audio.")

        # Step 3: Return the description and MP3 audio to the frontend
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

        return jsonify({
            "description": description,
            "audioBase64": audio_base64,
            "audioMimeType": "audio/mpeg",
            "fileName": "travel-guide.mp3"
        })

    except requests.Timeout:
        app.logger.warning("Murf request timed out")
        return jsonify({
            "error": "Murf took too long to respond. Please retry."
        }), 504

    except requests.RequestException:
        app.logger.exception("Murf connection error")
        return jsonify({
            "error": "Could not connect to Murf. Check your internet."
        }), 502

    except Exception:
        app.logger.exception("Travel guide generation failed")
        return jsonify({
            "error": "Generation failed. Check the backend terminal logs."
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )