import streamlit as st
import json

# Load JSON data
def load_data():
    with open("full_college_data.json", "r") as file:
        return json.load(file)

def display_college_card(college_name, details):
    st.markdown(f"""
    <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px; background-color: white; height: 100%;">
        <h4 style="color: #1f618d; font-size: 1em; margin-top: 0;">{college_name}</h4>
        <p style="font-size: 0.8em; font-weight: bold; margin-bottom: 2px;">Why It's a Hidden Gem:</p>
        <ul style="font-size: 0.75em; margin-top: 0; padding-left: 15px;">
            {"".join(f"<li>{reason}</li>" for reason in details["hidden_gem_reasons"])}
        </ul>
        <p style="font-size: 0.8em; font-weight: bold; margin-bottom: 2px;">Potential Downsides:</p>
        <ul style="font-size: 0.75em; margin-top: 0; padding-left: 15px;">
            {"".join(f"<li>{downside}</li>" for downside in details["potential_drawbacks"])}
        </ul>
        <p style="font-size: 0.8em; font-weight: bold; margin-bottom: 2px;">Notable Metrics:</p>
        <div style="font-size: 0.7em;">
            {"".join(f'<span style="background-color: #f0f0f0; padding: 2px 4px; margin: 1px; border-radius: 5px; display: inline-block;">{metric}</span>' for metric in details["notable_metrics"])}
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_cards(data, filter_key=""):
    colleges = list(data.keys())
    filtered_colleges = [college for college in colleges if filter_key.lower() in college.lower()]
    
    screen_width = st.session_state.get("screen_width", 1200)
    num_cols = max(2, min(5, screen_width // 250))  # Adjust for more columns on wider screens
    
    for i in range(0, len(filtered_colleges), num_cols):
        cols = st.columns(num_cols)
        for j in range(num_cols):
            if i + j < len(filtered_colleges):
                with cols[j]:
                    display_college_card(filtered_colleges[i + j], data[filtered_colleges[i + j]])

def main():
    st.set_page_config(layout="wide")
    st.title("College Info Dashboard")
    
    # Custom CSS for more compact layout
    st.markdown("""
    <style>
    .stApp {
        max-width: 1400px;
        margin: 0 auto;
    }
    .stMarkdown {
        font-size: 0.9em;
    }
    h1 {
        font-size: 1.8em;
    }
    .stTextInput > label {
        font-size: 0.9em;
    }
    .stTextInput > div > div > input {
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)
    
    college_data = load_data()
    filter_key = st.text_input("Search for colleges:")
    
    # JavaScript to get screen width
    st.markdown("""
    <script>
    const updateScreenWidth = () => {
        const screenWidth = window.innerWidth;
        const event = new CustomEvent('streamlit:screenWidth', {detail: screenWidth});
        window.dispatchEvent(event);
    };
    updateScreenWidth();
    window.addEventListener('resize', updateScreenWidth);
    </script>
    """, unsafe_allow_html=True)
    
    # Handle the custom event in Streamlit
    screen_width = st.empty()
    st.session_state.screen_width = screen_width.number_input("Screen Width", value=1200, key="screen_width_input", label_visibility="hidden")
    
    display_cards(college_data, filter_key)

if __name__ == "__main__":
    main()