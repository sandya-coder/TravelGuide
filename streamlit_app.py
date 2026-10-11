
import streamlit as st
import requests
from google import genai

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="TravelMate AI",
    page_icon="✈️",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5f3ff 0%, #ecfeff 100%);
}
.main .block-container {
    max-width: 1000px;
    padding-top: 2rem;
}
.hero {
    background: linear-gradient(120deg, #6d28d9, #0891b2);
    padding: 30px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 25px;
}
.hero h1 {
    color: white;
    font-size: 42px;
}
.hero p {
    color: white;
    font-size: 17px;
}
.stButton button {
    background: linear-gradient(90deg, #7c3aed, #0891b2);
    color: white;
    border: none;
    border-radius: 10px;
    min-height: 45px;
    font-weight: bold;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# API KEYS
# Read keys from Streamlit Secrets
# --------------------------------------------------
try:
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
    MURF_AI_API_KEY = st.secrets.get("MURF_AI_API_KEY", "")
except Exception:
    GEMINI_API_KEY = ""
    MURF_AI_API_KEY = ""

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.header("⚙️ API Configuration")
    st.write("API keys are read securely from Streamlit Secrets.")

    if GEMINI_API_KEY and MURF_AI_API_KEY:
        st.success("API keys detected.")
    else:
        st.warning(
            "Add GEMINI_API_KEY and MURF_AI_API_KEY "
            "in your Streamlit app's Secrets settings."
        )

    st.divider()
    st.subheader("🌍 About TravelMate")
    st.write(
        "Explore destinations through AI-generated stories "
        "and narrated audio guides."
    )
    st.write("✨ AI-powered travel stories")
    st.write("🎙️ Voice narration")
    st.write("🌐 Multiple languages")
    st.write("📥 Downloadable audio")

# --------------------------------------------------
# MAIN PAGE
# --------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>✈️ TravelMate AI</h1>
    <p>Your personal AI-powered audio tour guide</p>
    <p>Discover famous destinations through engaging stories and AI narration.</p>
</div>
""", unsafe_allow_html=True)

st.subheader("🗺️ Create Your Travel Guide")

destination = st.text_input(
    "📍 Enter a destination",
    placeholder="Example: Taj Mahal, Agra"
)

language = st.selectbox(
    "🌐 Choose your language",
    ["English", "Hindi", "Tamil", "Telugu"]
)

guide_type = st.radio(
    "📖 Choose your guide style",
    ["Quick Summary", "Detailed Story"],
    horizontal=True
)

voice_id = st.text_input(
    "🎙️ Murf Voice ID",
    placeholder="Enter a valid voice ID from your Murf account"
)

st.caption(
    "Use a voice ID supported by your Murf API account "
    "and compatible with your selected language."
)


# --------------------------------------------------
# LANGUAGE SETTINGS
# --------------------------------------------------
language_settings = {
    "English": {
        "name": "English",
        "locale": "en-US"
    },
    "Hindi": {
        "name": "Hindi",
        "locale": "hi-IN"
    },
    "Tamil": {
        "name": "Tamil",
        "locale": "ta-IN"
    },
    "Telugu": {
        "name": "Telugu",
        "locale": "te-IN"
    }
}

# --------------------------------------------------
# GENERATE GUIDE
# --------------------------------------------------
if st.button("✨ Generate Audio Guide", use_container_width=True):

    if not destination.strip():
        st.error("Please enter a destination.")

    elif not GEMINI_API_KEY:
        st.error(
            "Gemini API key is missing. "
            "Add GEMINI_API_KEY in Streamlit Secrets."
        )

    elif not MURF_AI_API_KEY:
        st.error(
            "Murf API key is missing. "
            "Add MURF_AI_API_KEY in Streamlit Secrets."
        )

    elif not voice_id.strip():
        st.error(
            "Please enter a valid Murf Voice ID."
        )

    else:
        settings = language_settings[language]

        if guide_type == "Quick Summary":
            length_instruction = (
                "Write a concise travel guide of approximately "
                "150 to 200 words."
            )
        else:
            length_instruction = (
                "Write an engaging, detailed travel guide of "
                "approximately 400 to 600 words. Include history, "
                "culture, important attractions, local experiences, "
                "and useful visitor tips."
            )

        prompt = f"""
        You are an experienced and friendly travel guide.

        Create a travel guide about: {destination}

        Write the guide entirely in {settings["name"]}.

        {length_instruction}

        Include:
        1. An engaging introduction.
        2. Historical and cultural significance.
        3. Important attractions.
        4. Interesting facts.
        5. Practical visitor tips.
        6. A friendly conclusion.

        Use natural language suitable for speaking aloud.
        Avoid Markdown tables and excessive special characters.
        Do not invent facts when information is uncertain.
        """

        try:
            with st.spinner("🌍 Creating your travel story..."):

                client = genai.Client(
                    api_key=GEMINI_API_KEY
                )

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                story = response.text

                if not story or not story.strip():
                    st.error(
                        "The AI did not return a travel story. "
                        "Please try again."
                    )
                    st.stop()

            st.success("Your travel story is ready!")

            st.subheader("📖 Your Travel Story")
            st.write(story)

            st.divider()
            st.subheader("🎧 Audio Tour Guide")

            with st.spinner("🎙️ Generating audio with Murf AI..."):

                murf_url = (
                    "https://global.api.murf.ai/v1/speech/stream"
                )

                headers = {
                    "api-key": MURF_AI_API_KEY,
                    "Content-Type": "application/json"
                }

                payload = {
                    "voice_id": voice_id.strip(),
                    "text": story,
                    "locale": settings["locale"],
                    "model": "FALCON",
                    "format": "MP3",
                    "sampleRate": 24000,
                    "channelType": "MONO"
                }

                audio_response = requests.post(
                    murf_url,
                    headers=headers,
                    json=payload,
                    timeout=120
                )

                if not audio_response.ok:
                    st.error(
                        f"Murf API error: HTTP "
                        f"{audio_response.status_code}"
                    )
                    st.code(audio_response.text[:1500])
                    st.stop()

                content_type = audio_response.headers.get(
                    "Content-Type", ""
                ).lower()

                if "json" in content_type:
                    st.error(
                        "Murf returned JSON instead of audio. "
                        "Check the API response below."
                    )
                    st.code(audio_response.text[:1500])
                    st.stop()

                audio_bytes = audio_response.content

                if not audio_bytes:
                    st.error("Murf returned an empty audio response.")
                    st.stop()

            st.audio(audio_bytes, format="audio/mpeg")

            st.download_button(
                label="📥 Download Audio Guide",
                data=audio_bytes,
                file_name="travelmate_audio_guide.mp3",
                mime="audio/mpeg",
                use_container_width=True
            )

            st.success("Your audio guide is ready!")

        except Exception as e:
            st.error("Something went wrong while generating your guide.")
            st.write("Error details:")
            st.code(str(e))

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.markdown(
    "<center>✈️ TravelMate AI | Explore the world, "
    "one story at a time.</center>",
    unsafe_allow_html=True
)
