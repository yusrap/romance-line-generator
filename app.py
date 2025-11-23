import streamlit as st
from openai import OpenAI

# Page config
st.set_page_config(
    page_title="Romance Line Generator",
    page_icon="💕",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS - FORCE same height
st.markdown("""
<style>
    /* Force light mode */
    [data-testid="stAppViewContainer"] {
        background-color: white;
    }
    
    .main {
        background-color: white !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }
    
    /* Title */
    h1 {
        color: #2d2d2d;
        font-size: 2.8rem;
        margin-bottom: 1rem;
        font-weight: 700;
        text-align: center !important;
    }
    
    .subtitle {
        color: #666;
        font-size: 1.1rem;
        line-height: 1.6;
        text-align: center !important;
        display: block;
        width: 100%;
    }

    /* Text input wrapper */
    .stTextInput > div {
        padding: 0 !important;
        border-radius: 25px !important;
        overflow: visible !important;  /* Prevent curve clipping */
        height: 56px !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* Actual input element */
    .stTextInput input {
        background-color: #f5f5f5 !important;
        border: 1px solid #e8e8e8 !important;
        border-radius: 25px !important;
        font-size: 16px !important;
        height: 56px !important;
        padding: 0 20px !important;
        line-height: 56px !important;
        box-sizing: border-box !important;
    }

    /* FORCE BUTTON HEIGHT */
    .stButton button {
        background-color: #ffb4c8 !important;
        color: white !important;
        border-radius: 25px !important;
        font-size: 14px !important;
        border: none !important;
        font-weight: 500 !important;
        width: 100% !important;
        height: 56px !important;
        min-height: 56px !important;
        max-height: 56px !important;
        padding: 0 30px !important;
        line-height: 56px !important;
        box-sizing: border-box !important;
        margin: 0 !important;
    }
    
    .stButton button:hover {
        background-color: #ff9bb3 !important;
    }
    
    /* Portrait */
    .stImage img {
        border-radius: 50% !important;
        border: 6px solid #ffb4c8 !important;
        object-fit: cover !important;
        width: 180px !important;
        height: 320px !important;
    }
    
    /* Label pill */
    .label-pill {
        background-color: #ffb4c8;
        color: white;
        padding: 6px 18px;
        border-radius: 20px;
        display: inline-block;
        font-size: 13px;
        margin-bottom: 12px;
        font-weight: 400;
    }
    
    /* Speech bubble */
    .speech-bubble {
        background-color: white;
        border-radius: 25px;
        padding: 25px 30px;
        margin-bottom: 30px;
        font-size: 19px;
        line-height: 1.6;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        color: #333;
    }
    
    hr {
        margin: 2.5rem 0;
        border: none;
        border-top: 1px solid #e8e8e8;
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["API_KEY"])

# Top words list
top_words = ['love', 'think', 'know', 'time', 'friend', 'thing', 'letter', 'little', 'day', 'woman',
    'heart', 'dear', 'great', 'happiness', 'pleasure', 'tell', 'wish', 'believe', 'hope',
    'friendship', 'good', 'thought', 'return', 'happy', 'word', 'write', 'let', 'moment',
    'find', 'answer', 'said', 'letters', 'night', 'tender', 'come', 'honour', 'man', 'leave',
    'taken', 'women', 'morning', 'reason', 'cause', 'opportunity', 'left', 'way', 'confidence',
    'idea', 'necessary', 'means', 'gave', 'received', 'obliged', 'opinion', 'sentiments', 'told',
    'yesterday', 'found', 'mind', 'lovely', 'days', 'able', 'right', 'eyes', 'speak', 'given',
    'passion', 'feel', 'virtue', 'life', 'sufficient', 'manner', 'dread', 'certain', 'wrote',
    'receive', 'daughter', 'hand', 'read', 'use', 'mother', 'charming', 'true', 'place', 'went',
    'came', 'young', 'business', 'forget', 'power', 'bed', 'object', 'new', 'giving', 'resolution',
    'unhappy', 'girl', 'uneasiness', 'took']

word_list_string = ', '.join(top_words[:50])

def get_system_prompt():
    return f'''You are a world-famous romance writer creating elegant, charming pick-up lines inspired by 18th-century letters.

Your goal: Transform modern casual messages into beautiful, romantic language that would make someone's heart flutter.

RULES:
1. Be ROMANTIC and creative - paint a picture, create a mood
2. Use 3-5 words from this list: {word_list_string}
3. Keep it relatively concise (10-20 words) but prioritize beauty over brevity
4. You can be poetic, thoughtful, or gently flirtatious
5. Don't just translate word-for-word - add romantic flair

Examples:

Input: "what's up girl?"
Output: "Have you ever thought about the little moments that turn into great love stories?"

Input: "you look cute"
Output: "Your lovely eyes and charming presence have quite captured my heart."

Input: "wanna hang out?"
Output: "Would you grant me the pleasure of your tender company this lovely evening?"

Now, transform this with beauty and romance:'''

# Title
st.markdown('<h1 style="text-align: center;">Bring Romance to Dating Apps</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">This one line generator leverages hundreds of pages of letters from "Dangerous Connections" to help you seduce with a romantic touch.</p>', unsafe_allow_html=True)

st.markdown("---")

# Initialize session state
if 'output_message' not in st.session_state:
    st.session_state.output_message = ""
if 'user_input_saved' not in st.session_state:
    st.session_state.user_input_saved = ""

# Chat layout
chat_col1, chat_col2 = st.columns([1, 4])

with chat_col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Juliette_Récamier_%281777-1849%29.jpg/500px-Juliette_Récamier_%281777-1849%29.jpg", width=180)

with chat_col2:
    if not st.session_state.output_message:
        st.markdown('<div class="label-pill">input</div>', unsafe_allow_html=True)
    
    col_input, col_button = st.columns([5, 1.5])
    with col_input:
        user_input = st.text_input("Your message", placeholder="Type your casual message here...", 
                                  label_visibility="collapsed", key="input_field", on_change=_noop)
    with col_button:
        generate_button = st.button("Give me a line!")
    
    def generate_response(input_text):
        if input_text:
            st.session_state.user_input_saved = input_text
            with st.spinner("Crafting your romantic message..."):
                try:
                    response = client.chat.completions.create(
                        model='gpt-3.5-turbo',
                        messages=[
                            {'role': 'system', 'content': get_system_prompt()},
                            {'role': 'user', 'content': input_text}
                        ],
                        temperature=0.8
                    )
                    st.session_state.output_message = response.choices[0].message.content
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a message!")
    
    if generate_button and user_input:
        generate_response(user_input)
    
    if st.session_state.user_input_saved and st.session_state.output_message:
        st.markdown('<div class="label-pill">input</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="speech-bubble">{st.session_state.user_input_saved}</div>', unsafe_allow_html=True)
    
    if st.session_state.output_message:
        st.markdown('<div class="label-pill">romantic version</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="speech-bubble">{st.session_state.output_message}</div>', unsafe_allow_html=True)
