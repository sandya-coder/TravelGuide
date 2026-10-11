
import streamlit as st
import requests
from google import genai
import html

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="TravelMate AI | Your Audio Tour Guide",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');

/* GLOBAL COLORS */
.stApp {
    background: #f5f7fb !important;
    color: #172033 !important;
    font-family: 'DM Sans', sans-serif;
}

.stApp p,
.stApp li,
.stApp label,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp span,
.stApp div[data-testid="stMarkdownContainer"] {
    color: #172033;
}

/* Keep icons and emoji visible */
.stApp [data-testid="stMarkdownContainer"] {
    color: #172033 !important;
}

/* PAGE LAYOUT */
header[data-testid="stHeader"] {
    background: transparent;
}

.main .block-container {
    max-width: 1180px;
    padding: 1.5rem 2rem 3rem 2rem;
}

/* BRAND HEADER */
.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 25px;
}

.brand-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 15px;
    background: linear-gradient(135deg, #2563eb, #06b6d4);
    color: #ffffff !important;
    font-size: 25px;
}

.brand-name {
    font-size: 23px;
    font-weight: 800;
    color: #14213d !important;
    letter-spacing: -0.8px;
}

.brand-subtitle {
    font-size: 12px;
    color: #64748b !important;
}

/* HERO BANNER */
.hero {
    overflow: hidden;
    border-radius: 28px;
    padding: 60px 45px;
    margin-bottom: 28px;
    background:
        linear-gradient(
            90deg,
            rgba(8, 22, 46, 0.94) 0%,
            rgba(8, 22, 46, 0.75) 55%,
            rgba(8, 22, 46, 0.18) 100%
        ),
        url("https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=1800&q=85");
    background-size: cover;
    background-position: center;
    box-shadow: 0 18px 45px rgba(22, 43, 75, 0.13);
}

.hero .hero-tag {
    display: inline-block;
    padding: 8px 13px;
    border: 1px solid rgba(255,255,255,0.4);
    border-radius: 30px;
    background: rgba(255,255,255,0.12);
    color: #ffffff !important;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}

.hero h1 {
    color: #ffffff !important;
    font-family: 'Manrope', sans-serif;
    font-size: clamp(34px, 5vw, 54px);
    font-weight: 800;
    line-height: 1.14;
    letter-spacing: -1.5px;
    margin-top: 23px;
    margin-bottom: 15px;
}

.hero p {
    color: #f1f5f9 !important;
    max-width: 570px;
    font-size: 16px;
    line-height: 1.8;
}

.hero .hero-highlight {
    color: #67e8f9 !important;
}

/* SECTION HEADINGS */
.section-kicker {
    color: #2563eb !important;
    text-transform: uppercase;
    letter-spacing: 1.6px;
    font-weight: 800;
    font-size: 11px;
    margin-bottom: 7px;
}

.section-heading {
    font-family: 'Manrope', sans-serif;
    font-size: 28px;
    color: #172033 !important;
    font-weight: 800;
    letter-spacing: -0.7px;
    margin-bottom: 7px;
}

.section-description {
    font-size: 14px;
    color: #526176 !important;
    line-height: 1.7;
    margin-bottom: 23px;
}

/* FEATURE CARDS */
.feature-card {
    height: 100%;
    padding: 21px;
    background: #ffffff;
    border: 1px solid #e3e9f2;
    border-radius: 19px;
    box-shadow: 0 5px 18px rgba(22, 43, 75, 0.04);
}

.feature-card .feature-icon {
    width: 43px;
    height: 43px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #eaf2ff;
    border-radius: 13px;
    font-size: 22px;
    margin-bottom: 13px;
}

.feature-card h4 {
    font-size: 16px;
    color: #172033 !important;
    margin: 0 0 8px 0;
}

.feature-card p {
    color: #526176 !important;
    font-size: 13px;
    line-height: 1.7;
    margin: 0;
}

/* DESTINATION CARDS */
.destination-card {
    background: #ffffff;
    border: 1px solid #e3e9f2;
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 10px;
}

.destination-card img {
    width: 100%;
    height: 125px;
    object-fit: cover;
    display: block;
}

.destination-card .destination-info {
    padding: 12px 13px 14px;
}

.destination-card .destination-name {
    font-weight: 800;
    color: #172033 !important;
    font-size: 15px;
}

.destination-card .destination-location {
    color: #526176 !important;
    font-size: 12px;
    margin-top: 4px;
}

/* FORM CONTAINER */
.form-card {
    background: #ffffff;
    border: 1px solid #e3e9f2;
    border-radius: 22px;
    padding: 25px;
    box-shadow: 0 8px 30px rgba(22, 43, 75, 0.045);
}

/* FORM LABELS */
.stApp [data-testid="stWidgetLabel"] p,
.stApp [data-testid="stWidgetLabel"] label,
.stApp .stTextInput label,
.stApp .stSelectbox label,
.stApp .stRadio label {
    color: #243247 !important;
    font-weight: 600;
}

/* TEXT INPUTS */
.stApp input,
.stApp textarea {
    color: #172033 !important;
    background-color: #ffffff !important;
    -webkit-text-fill-color: #172033 !important;
    border-color: #d6e0ed !important;
    border-radius: 12px !important;
}

.stApp input::placeholder,
.stApp textarea::placeholder {
    color: #7b8798 !important;
    -webkit-text-fill-color: #7b8798 !important;
    opacity: 1 !important;
}

/* DROPDOWNS */
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: #ffffff !important;
}

.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] * {
    color: #172033 !important;
}

/* RADIO BUTTON LABELS */
.stApp [data-testid="stRadio"] label,
.stApp [data-testid="stRadio"] p {
    color: #243247 !important;
}

/* CAPTIONS */
.stApp [data-testid="stCaptionContainer"] p {
    color: #526176 !important;
    font-size: 13px;
}

/* BUTTONS */
.stApp .stButton button,
.stApp .stDownloadButton button {
    min-height: 49px;
    width: 100%;
    border: none !important;
    border-radius: 13px;
    background: linear-gradient(105deg, #2563eb, #0891b2) !important;
    color: #ffffff !important;
    font-weight: 800;
    transition: all 0.2s ease;
}

.stApp .stButton button *,
.stApp .stDownloadButton button * {
    color: #ffffff !important;
}

.stApp .stButton button:hover,
.stApp .stDownloadButton button:hover {
    background: linear-gradient(105deg, #1d4ed8, #0e7490) !important;
    box-shadow: 0 7px 20px rgba(37, 99, 235, 0.22);
    transform: translateY(-1px);
}

/* GENERATED STORY */
.story-card {
    padding: 27px;
    border: 1px solid #e3e9f2;
    border-radius: 20px;
    background: #ffffff;
    margin-top: 12px;
    margin-bottom: 18px;
}

.story-label {
    font-size: 11px;
    font-weight: 800;
    color: #2563eb !important;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.story-title {
    font-family: 'Manrope', sans-serif;
    color: #172033 !important;
    font-size: 25px;
    font-weight: 800;
    margin-bottom: 12px;
}

/* GENERATED STORY TEXT */
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] li {
    color: #263449;
    line-height: 1.8;
}

.stApp h2,
.stApp h3,
.stApp h4 {
    color: #172033 !important;
}

/* ALERTS */
.stApp [data-testid="stAlert"] p {
    color: inherit !important;
}

/* AUDIO PLAYER */
.stApp audio {
    width: 100%;
    border-radius: 12px;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #edf3ff;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label {
    color: #172033 !important;
}

/* FOOTER */
.footer {
    text-align: center;
    padding: 24px 10px;
    color: #526176 !important;
    font-size: 13px;
    line-height: 1.8;
}

.footer strong {
    color: #2563eb !important;
}

/* MOBILE */
@media (max-width: 700px) {
    .main .block-container {
        padding: 1rem 1rem 2rem 1rem;
    }

    .hero {
        padding: 35px 23px;
        border-radius: 21px;
        background-position: center;
    }

    .hero h1 {
        font-size: 35px;
    }

    .hero p {
        font-size: 14px;
    }

    .section-heading {
        font-size: 24px;
    }

    .form-card {
        padding: 17px;
    }
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# API KEYS
# ==================================================

try:
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
    MURF_AI_API_KEY = st.secrets.get("MURF_AI_API_KEY", "")
except Exception:
    GEMINI_API_KEY = ""
    MURF_AI_API_KEY = ""


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:
    st.markdown("## ✈️ TravelMate AI")
    st.caption("Your personal AI travel companion")
    st.divider()

    st.markdown("### 🌍 Explore with AI")
    st.write(
        "Generate narrated travel stories for destinations around the world."
    )

    st.markdown("### ✨ What you can do")
    st.write("📍 Discover destinations")
    st.write("📖 Learn history and culture")
    st.write("🎙️ Listen to AI narration")
    st.write("🌐 Choose your language")
    st.write("📥 Download your audio guide")

    st.divider()
    st.markdown("### 🔐 API connection")

    if GEMINI_API_KEY and MURF_AI_API_KEY:
        st.success("API keys detected")
    else:
        st.warning(
            "Configure GEMINI_API_KEY and MURF_AI_API_KEY "
            "in Streamlit app settings → Secrets."
        )

    st.caption("Your API keys are read from Streamlit Secrets.")


# ==================================================
# BRAND HEADER
# ==================================================

st.markdown("""
<div class="brand">
    <div class="brand-icon">✈️</div>
    <div>
        <div class="brand-name">TravelMate AI</div>
        <div class="brand-subtitle">Your world, your story</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==================================================
# HERO SECTION
# ==================================================

st.markdown("""
<div class="hero">
    <span class="hero-tag">✦ YOUR PERSONAL AI TOUR GUIDE</span>
    <h1>Every destination<br>has a <span class="hero-highlight">story.</span></h1>
    <p>
        Travel beyond the ordinary. Discover the history, culture,
        hidden gems and fascinating stories behind the places you love
        through your own AI-generated audio tour.
    </p>
</div>
""", unsafe_allow_html=True)


# ==================================================
# FEATURE CARDS
# ==================================================

st.markdown(
    '<div class="section-kicker">MADE FOR CURIOUS TRAVELLERS</div>'
    '<div class="section-heading">Explore your way</div>'
    '<div class="section-description">'
    'Everything you need to turn a destination into a memorable experience.'
    '</div>',
    unsafe_allow_html=True
)

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🗺️</div>
        <h4>Discover Places</h4>
        <p>Explore famous landmarks, local culture, history and interesting facts.</p>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎧</div>
        <h4>Listen Anywhere</h4>
        <p>Turn your personalised travel story into audio narration.</p>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🌏</div>
        <h4>Your Language</h4>
        <p>Create your guide in English, Hindi, Tamil or Telugu.</p>
    </div>
    """, unsafe_allow_html=True)


# ==================================================
# DESTINATION SUGGESTIONS
# ==================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-kicker">GET INSPIRED</div>'
    '<div class="section-heading">Where will you go next?</div>'
    '<div class="section-description">'
    'Start with a favourite or enter any destination below.'
    '</div>',
    unsafe_allow_html=True
)

destinations = [
    {
        "name": "Taj Mahal",
        "location": "Agra, India",
        "image": "photo-1564507592333-c60657eea523"
    },
    {
        "name": "Bali",
        "location": "Indonesia",
        "image": "photo-1537996194471-e657df975ab4"
    },
    {
        "name": "Paris",
        "location": "France",
        "image": "photo-1502602898657-3e91760cbb34"
    },
    {
        "name": "Grand Canyon",
        "location": "United States",
        "image": "photo-1474044159687-1ee9f3a51722"
    }
]

destination_columns = st.columns(4)

for index, item in enumerate(destinations):
    with destination_columns[index]:
        st.markdown(
            f"""
            <div class="destination-card">
                <img
                    src="https://images.unsplash.com/{item['image']}?auto=format&fit=crop&w=500&q=80"
                    alt="{html.escape(item['name'])}"
                >
                <div class="destination-info">
                    <div class="destination-name">
                        {html.escape(item['name'])}
                    </div>
                    <div class="destination-location">
                        {html.escape(item['location'])}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            f"Explore {item['name']}",
            key=f"destination_{index}",
            use_container_width=True
        ):
            st.session_state["destination_input"] = (
                f"{item['name']}, {item['location']}"
            )


# ==================================================
# GUIDE CREATION FORM
# ==================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-kicker">CREATE YOUR EXPERIENCE</div>'
    '<div class="section-heading">Build your audio travel guide</div>'
    '<div class="section-description">'
    'Choose your destination and preferences. We will create a story just for you.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="form-card">', unsafe_allow_html=True)

destination = st.text_input(
    "📍 Where do you want to explore?",
    key="destination_input",
    placeholder="For example: Taj Mahal, Agra"
)

col1, col2 = st.columns(2)

with col1:
    language = st.selectbox(
        "🌐 Choose your language",
        ["English", "Hindi", "Tamil", "Telugu"]
    )

with col2:
    guide_type = st.selectbox(
        "📖 Choose your guide style",
        ["Quick Summary", "Detailed Story"]
    )

voice_id = st.text_input(
    "🎙️ Murf Voice ID",
    placeholder="Enter a voice ID supported by your Murf account"
)

st.caption(
    "Use a voice ID supported by your Murf API account "
    "and compatible with your selected language."
)

generate_button = st.button(
    "✨ Generate My Audio Guide",
    use_container_width=True
)

st.markdown('</div>', unsafe_allow_html=True)


# ==================================================
# LANGUAGE SETTINGS
# ==================================================

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


# ==================================================
# GENERATE TRAVEL STORY AND AUDIO
# ==================================================

if generate_button:

    if not destination.strip():
        st.error("Please enter a destination.")

    elif not GEMINI_API_KEY:
        st.error(
            "Gemini API key is missing. Add GEMINI_API_KEY "
            "in Streamlit app settings → Secrets."
        )

    elif not MURF_AI_API_KEY:
        st.error(
            "Murf API key is missing. Add MURF_AI_API_KEY "
            "in Streamlit app settings → Secrets."
        )

    elif not voice_id.strip():
        st.error("Please enter your Murf Voice ID.")

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
                "culture, important attractions, local experiences "
                "and useful visitor tips."
            )

        prompt = f"""
You are a friendly, knowledgeable and engaging travel guide.

Create a travel guide about: {destination}

Write the entire guide in {settings["name"]}.

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
            with st.spinner("🌍 Discovering your destination..."):
                client = genai.Client(api_key=GEMINI_API_KEY)

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

            st.markdown("""
            <div class="story-card">
                <div class="story-label">YOUR PERSONAL TRAVEL GUIDE</div>
                <div class="story-title">📖 Your destination story</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(story)

            st.divider()

            st.markdown(
                '<div class="section-kicker">LISTEN AND EXPLORE</div>'
                '<div class="section-heading">🎧 Your audio tour</div>'
                '<div class="section-description">'
                'Listen to your guide or download it for your journey.'
                '</div>',
                unsafe_allow_html=True
            )

            with st.spinner("🎙️ Creating your audio guide with Murf AI..."):

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
                label="📥 Download Your Audio Guide",
                data=audio_bytes,
                file_name="travelmate_audio_guide.mp3",
                mime="audio/mpeg",
                use_container_width=True
            )

            st.success(
                "Your audio guide is ready. Enjoy your journey! ✈️"
            )

        except Exception as e:
            st.error(
                "Something went wrong while generating your guide."
            )
            st.code(str(e))


# ==================================================
# FOOTER
# ==================================================

st.markdown("""
<div class="footer">
    <strong>✈️ TravelMate AI</strong><br>
    Discover more. Travel deeper. Listen to every story.<br>
    Made with ❤️ for curious travellers.
</div>
""", unsafe_allow_html=True)
