import streamlit as st
import streamlit.components.v1 as components

# Set page config
st.set_page_config(page_title="Gem Cards", layout="wide")

def main():
    st.title("Hidden Gems Finder")

    # Add a new section for the College Cards
    st.header("College Cards")
    st.write("Explore our curated list of hidden gem colleges:")

    # Load the HTML file
    with open("college_cards.html", "r") as f:
        html_content = f.read()

    # Render the React component
    components.html(html_content, height=600)

if __name__ == "__main__":
    main()