
import os
import requests
import streamlit as st
from google import genai

st.set_page_config(
    page_title="TravelMate AI",
    page_icon="✈️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5f3ff, #ecfeff);
}
h1 { color: #6d28d9; }
h2, h3 { color: #0f766e; }
.stButton > button {
    background: linear-gradient(90deg, #7c3aed, #0891b2);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("✈️ TravelMate AI")
st.subheader("Your personal AI-powered audio tour guide")
st.write("Discover famous destinations through engaging stories and AI narration.")

with st.sidebar:
    st.header("⚙️ API Configuration")
    st.info("Add your API keys in Streamlit → App settings → Secrets.")
    st.markdown("Required secrets: `GEMINI_API_KEY` and `MURF_AI_API_KEY`")

place = st.text_input("🌍 Destination", placeholder="Taj Mahal, Agra")

language = st.selectbox(
    "🗣️ Story language",
    ["English", "Hindi", "Tamil", "Telugu"]
)

length = st.selectbox(
    "📖 Guide length",
    ["Quick summary", "Detailed story"]
)

voice_id = st.text_input(
    "🎙️ Murf voice ID",
    placeholder="Enter a voice ID supported by your Murf account"
)

locale_options = {
    "English": ["en-US", "en-IN"],
    "Hindi": ["hi-IN"],
    "Tamil": ["ta-IN"],
    "Telugu": ["te-IN"]
}

locale = st.selectbox(
    "Voice locale",
    locale_options[language]
)

if st.button("✨ Generate my audio guide", use_container_width=True):
    if not place.strip() or not voice_id.strip():
        st.warning("Please enter a destination and Murf voice ID.")
    else:
        try:
            gemini_key = st.secrets["GEMINI_API_KEY"]
            murf_key = st.secrets["MURF_AI_API_KEY"]

            client = genai.Client(api_key=gemini_key)

            word_count = 150 if length == "Quick summary" else 300

            prompt = f"""
            Act as a professional tourist guide. Explain the history,
            importance, attractions, and interesting facts about {place}.
            Write approximately {word_count} words in {language}.
            Use engaging language and avoid inventing facts.
            """

            with st.spinner("🌍 Creating your travel story..."):
                response = client.models.generate_content(
                    model="gemini-3.1-flash-lite",
                    contents=prompt
                )

            description = (response.text or "").strip()

            if not description:
                st.error("Gemini returned an empty description.")
                st.stop()

            st.subheader("📖 Your Travel Story")
            st.write(description)

            with st.spinner("🎧 Creating your audio narration..."):
                audio_response = requests.post(
                    "https://global.api.murf.ai/v1/speech/stream",
                    headers={
                        "api-key": murf_key,
                        "Content-Type": "application/json"
                    },
                    json={
                        "voice_id": voice_id.strip(),
                        "text": description,
                        "locale": locale,
                        "model": "FALCON",
                        "format": "MP3",
                        "sampleRate": 24000,
                        "channelType": "MONO"
                    },
                    timeout=120
                )

            if audio_response.status_code != 200:
                st.error(
                    f"Murf returned HTTP {audio_response.status_code}. "
                    "Check your voice ID, locale, API access, and credits."
                )
                st.stop()

            audio_bytes = audio_response.content

            if not audio_bytes:
                st.error("Murf returned no audio.")
                st.stop()

            st.subheader("🎧 Listen to Your Travel Guide")
            st.audio(audio_bytes, format="audio/mpeg")

            st.download_button(
                "⬇️ Download MP3",
                data=audio_bytes,
                file_name="travel-guide.mp3",
                mime="audio/mpeg",
                use_container_width=True
            )

            st.success("Your travel guide is ready!")

        except KeyError:
            st.error(
                "API keys are missing. Add both keys under "
                "Streamlit App settings → Secrets."
            )
        except Exception as error:
            st.error(f"Generation failed: {error}")
