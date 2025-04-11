import streamlit as st
import re
from collections import Counter
from streamlit_lottie import st_lottie
import requests

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Text Analyzer Pro 2.0", layout="centered", page_icon="🧠")

# ---------------- LOTTIE LOADER ----------------
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

animation = load_lottie_url("https://assets7.lottiefiles.com/packages/lf20_touohxv0.json")

# ---------------- STYLING ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Nunito', sans-serif;
}

h1, h2, h3 {
    font-weight: 700;
}

.main-box {
    background: #f8f9fa;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    transition: 0.3s ease;
}

.main-box:hover {
    transform: scale(1.01);
}

.result-section {
    margin-top: 1.5rem;
    padding: 1.2rem;
    border-radius: 12px;
    background: #ffffff;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.footer {
    margin-top: 3rem;
    text-align: center;
    font-size: 0.9rem;
    color: #999;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("## 🧠 Text Analyzer Pro 2.0")
st.caption("Smart. Stylish. Supercharged.")

if animation:
    st_lottie(animation, height=180, key="intro")

st.divider()

# ---------------- USER INPUT ----------------
st.markdown("### 📝 Input Your Text")
text_input = st.text_area("Write or paste your text below 👇", height=180)

# ---------------- OPTIONS ----------------
st.markdown("### 🛠️ Text Transform Options")
option = st.selectbox("Select transformation:", [
    "Original", "UPPERCASE", "lowercase", "Title Case", "Remove Extra Spaces"
])

def transform_text(text, mode):
    if mode == "UPPERCASE":
        return text.upper()
    elif mode == "lowercase":
        return text.lower()
    elif mode == "Title Case":
        return text.title()
    elif mode == "Remove Extra Spaces":
        return " ".join(text.split())
    return text

transformed_text = transform_text(text_input, option)

# ---------------- ANALYZE BUTTON ----------------
if st.button("🚀 Analyze Text"):
    if not transformed_text.strip():
        st.warning("Please enter some text first.")
    else:
        text = transformed_text.strip()

        total_chars = len(text)
        total_words = len(text.split())
        total_sentences = len(re.split(r'[.!?]+', text)) - 1

        words = re.findall(r'\w+', text.lower())
        word_freq = Counter(words).most_common(5)

        char_freq = Counter(c.lower() for c in text if c.isalnum())
        top_chars = char_freq.most_common(5)

        # ---------------- DISPLAY RESULTS ----------------
        st.markdown("## 📊 Results")
        with st.container():
            st.markdown("<div class='main-box'>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            col1.metric("🔡 Characters", total_chars)
            col2.metric("🧾 Words", total_words)
            col3.metric("📚 Sentences", total_sentences)

            st.markdown("#### 🔠 Most Common Words")
            for word, count in word_freq:
                st.write(f"• **{word}**: {count} times")

            st.markdown("#### 🔡 Most Common Characters")
            for char, count in top_chars:
                st.write(f"• **{char}**: {count} times")

            st.markdown("#### 🧾 Transformed Text")
            st.code(transformed_text, language="text")

            st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("<div class='footer'>✨ Built with ❤️ using Streamlit | © 2025 Text Analyzer Pro</div>", unsafe_allow_html=True)
