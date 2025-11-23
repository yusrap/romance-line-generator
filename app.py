import streamlit as st
from openai import OpenAI

# Page config
st.set_page_config(
    page_title="Romance Line Generator",
    page_icon="💕",
    layout="centered"
)

# Custom CSS to match the design exactly
st.markdown("""
<style>
    /* White background */
    .main {
        background-color: white;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Container styling */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1000px;
    }
    
    /* Input box styling - wider and cleaner */
    .stTextInput > div > div > input {
        background-color: #f5f5f5;
        border: 1px solid #e8e8e8;
        border-radius: 25px;
        padding: 18px 25px;
        font-size: 16px;
        width: 100%;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #ffb4c8;
        color: white;
        border-radius: 25px;
        padding: 15px 50px;
        font-size: 16px;
        border: none;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background-color: #ff9bb3;
    }
    
    /* Label styling - small pink pills */
    .label-pill {
        background-color: #ffb4c8;
        color: white;
        padding: 6px 18px;
        border-radius: 20px;
        display: inline-block;
        font-size: 13px;
        margin-bottom: 15px;
        font-weight: 400;
    }
    
    /* Message boxes - speech bubble style with shadow */
    .message-bubble {
        background-color: white;
        border-radius: 25px;
        padding: 25px 30px;
        margin: 10px 0 40px 0;
        font-size: 19px;
        line-height: 1.6;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        color: #333;
    }
    
    /* Title styling */
    h1 {
        color: #2d2d2d;
        font-size: 2.8rem;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .subtitle {
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
        line-height: 1.6;
    }
    
    /* Portrait styling */
    .portrait-container {
        text-align: center;
        margin: 2rem 0;
    }
    
    /* Image styling - circular with pink border */
    img {
        border-radius: 50% !important;
        border: 6px solid #ffb4c8;
        object-fit: cover;
    }
    
    /* Spacing adjustments */
    .stMarkdown {
        margin-bottom: 0;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
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

# Main layout
col1, col2 = st.columns([1, 2.5])

with col1:
    # Portrait image
    st.markdown('<div class="portrait-container">', unsafe_allow_html=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/05/Juliette_Récamier_%281777-1849%29.jpg", width=200)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.title("Bring Romance to Dating Apps")
    st.markdown('<p class="subtitle">This one line generator leverages hundreds of pages of letters from "Dangerous Connections" to help you seduce with a romantic touch.</p>', unsafe_allow_html=True)

st.markdown("---")

# Initialize session state for messages
if 'input_message' not in st.session_state:
    st.session_state.input_message = ""
if 'output_message' not in st.session_state:
    st.session_state.output_message = ""

# Input section
user_input = st.text_input("Your message", placeholder="Type your casual message here...", 
                          label_visibility="collapsed", key="user_input")

# Button
if st.button("Give me a line!"):
    if user_input:
        st.session_state.input_message = user_input
        with st.spinner("Crafting your romantic message..."):
            try:
                response = client.chat.completions.create(
                    model='gpt-3.5-turbo',
                    messages=[
                        {'role': 'system', 'content': get_system_prompt()},
                        {'role': 'user', 'content': user_input}
                    ],
                    temperature=0.8
                )
                
                st.session_state.output_message = response.choices[0].message.content
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a message!")

# Display messages if they exist
if st.session_state.input_message:
    st.markdown('<div class="label-pill">input</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="message-bubble">{st.session_state.input_message}</div>', unsafe_allow_html=True)

if st.session_state.output_message:
    st.markdown('<div class="label-pill">romantic version</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="message-bubble">{st.session_state.output_message}</div>', unsafe_allow_html=True)
