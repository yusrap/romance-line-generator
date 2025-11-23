import streamlit as st
from openai import OpenAI

# Page config
st.set_page_config(
    page_title="Romance Line Generator",
    page_icon="💕",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #fff5f7;
    }
    .stTextInput > div > div > input {
        background-color: white;
        border: 2px solid #ffb6c1;
        border-radius: 10px;
        padding: 10px;
    }
    .stButton > button {
        background-color: #ff69b4;
        color: white;
        border-radius: 10px;
        padding: 10px 30px;
        font-size: 16px;
        border: none;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #ff1493;
    }
    .output-box {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    h1 {
        color: #d1477a;
        text-align: center;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 14px;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI client with API key from secrets
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

# System prompt
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

# Header
st.title("💕 Bring Romance to Dating Apps")
st.markdown('<p class="subtitle">Transform casual messages into elegant 18th-century romantic language</p>', 
            unsafe_allow_html=True)

st.markdown("---")

# Input section
user_input = st.text_input("", placeholder="Type your casual message here... (e.g., 'hey what's up?')", 
                          label_visibility="collapsed")

# Generate button
if st.button("✨ Give me a romantic line!"):
    if user_input:
        with st.spinner("Crafting your romantic message..."):
            try:
                # Create the prompt
                history = [
                    {'role': 'user', 'content': get_system_prompt()},
                    {'role': 'user', 'content': user_input}
                ]
                
                # Get response
                response = client.chat.completions.create(
                    model='gpt-3.5-turbo',
                    messages=[
                        {'role': 'system', 'content': get_system_prompt()},
                        {'role': 'user', 'content': user_input}
                    ],
                    temperature=0.8
                )
                
                output_text = response.choices[0].message.content
                
                # Display output
                st.markdown('<div class="output-box">', unsafe_allow_html=True)
                st.markdown(f'### 💌 Romantic Version:')
                st.markdown(f'*"{output_text}"*')
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Check word usage
                words_used = [word for word in top_words[:50] if word in output_text.lower()]
                
                # Stats
                with st.expander("📊 See details"):
                    st.write(f"**Words from source text used:** {len(words_used)}")
                    if words_used:
                        st.write(f"**Words:** {', '.join(words_used[:10])}")
                    st.write(f"**Output length:** {len(output_text.split())} words")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a message to transform!")

# Footer
st.markdown("---")
st.markdown('<p style="text-align: center; color: #999; font-size: 12px;">Powered by "Dangerous Connections" by De Laclos</p>', 
            unsafe_allow_html=True)