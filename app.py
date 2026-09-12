
import streamlit as st
import requests
from gtts import gTTS

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍",
    layout="centered"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown("""
<style>

.main {
    padding-top: 2rem;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 30px;
}

.translation-box {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #dddddd;
    margin-top: 20px;
}

.footer {
    text-align: center;
    margin-top: 40px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------

st.markdown(
    '<div class="title">🌍 AI Language Translator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Translate • Listen • Learn</div>',
    unsafe_allow_html=True
)

# -----------------------------
# LANGUAGES
# -----------------------------

languages = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Japanese": "ja"
}

language_names = list(languages.keys())

# -----------------------------
# SESSION STATE
# -----------------------------

if "source" not in st.session_state:
    st.session_state.source = "English"

if "target" not in st.session_state:
    st.session_state.target = "Hindi"

if "translation" not in st.session_state:
    st.session_state.translation = ""

# -----------------------------
# LANGUAGE SELECTION
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    source_language = st.selectbox(
        "Source Language",
        language_names,
        index=language_names.index(
            st.session_state.source
        )
    )

with col2:
    target_language = st.selectbox(
        "Target Language",
        language_names,
        index=language_names.index(
            st.session_state.target
        )
    )

# -----------------------------
# SWAP
# -----------------------------

if st.button(
    "🔄 Swap Languages",
    use_container_width=True
):

    st.session_state.source = target_language
    st.session_state.target = source_language

    st.rerun()

# -----------------------------
# TEXT INPUT
# -----------------------------

text = st.text_area(
    "✍️ Enter your text",
    placeholder="Type or paste your text here...",
    height=160
)

# -----------------------------
# TRANSLATION FUNCTION
# -----------------------------

def translate_text(text, source, target):

    url = "https://api.mymemory.translated.net/get"

    params = {
        "q": text,
        "langpair": f"{source}|{target}"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    if response.status_code == 200:

        data = response.json()

        return data["responseData"]["translatedText"]

    return None

# -----------------------------
# SPEECH FUNCTION
# -----------------------------

def create_speech(text, language):

    speech = gTTS(
        text=text,
        lang=language,
        slow=False
    )

    speech.save("translation.mp3")

    return "translation.mp3"

# -----------------------------
# TRANSLATE
# -----------------------------

if st.button(
    "🚀 Translate",
    use_container_width=True
):

    if not text.strip():

        st.warning(
            "⚠️ Please enter some text first."
        )

    elif source_language == target_language:

        st.info(
            "ℹ️ Please select different languages."
        )

    else:

        with st.spinner("Translating..."):

            try:

                translation = translate_text(
                    text,
                    languages[source_language],
                    languages[target_language]
                )

                if translation:

                    st.session_state.translation = translation

                    st.success(
                        "✅ Translation completed!"
                    )

                else:

                    st.error(
                        "❌ Translation failed."
                    )

            except Exception:

                st.error(
                    "❌ Unable to connect to "
                    "the translation service."
                )

# -----------------------------
# DISPLAY RESULT
# -----------------------------

if st.session_state.translation:

    st.markdown(
        '<div class="translation-box">',
        unsafe_allow_html=True
    )

    st.subheader("📝 Translation")

    st.write(
        st.session_state.translation
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Speech
    try:

        audio_file = create_speech(
            st.session_state.translation,
            languages[target_language]
        )

        st.subheader("🔊 Listen")

        with open(
            audio_file,
            "rb"
        ) as audio:

            st.audio(
                audio.read(),
                format="audio/mp3"
            )

    except Exception:

        st.warning(
            "⚠️ Text-to-speech is unavailable "
            "for this language."
        )

# -----------------------------
# FOOTER
# -----------------------------

st.markdown(
    '<div class="footer">'
    'Built as part of CodeAlpha AI Internship'
    '</div>',
    unsafe_allow_html=True
)
