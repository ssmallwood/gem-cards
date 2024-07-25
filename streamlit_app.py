import streamlit as st
import json

# Load JSON data
def load_data():
    with open("full_college_data.json", "r") as file:
        data = json.load(file)
    return data

def display_college_card(college_name, details):
    # Define custom CSS with theme-aware colors
    st.markdown("""
    <style>
    .big-font {
        font-size: 18px;
        font-weight: bold;
    }
    .small-font {
        font-size: 14px;
    }
    .data-section {
        border: 1px solid var(--st-color-secondary-25);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .private-institution {
        background-color: var(--st-color-primary-10);
    }
    .public-institution {
        background-color: var(--st-color-success-10);
    }
    .unknown-institution {
        background-color: var(--st-color-secondary-10);
    }
    .metric-pill {
        display: inline-block;
        background-color: var(--st-color-secondary-25);
        border-radius: 15px;
        padding: 6px 12px;
        margin: 5px;
        font-size: 11px;
        white-space: nowrap;
    }
    ul {
        padding-left: 20px;
    }
    li {
        margin-bottom: 5px;
        font-size: 13px;
    }
    /* Ensure text is visible in both light and dark modes */
    .data-section, .data-section h3, .data-section h4, .data-section h5, .data-section p, .data-section li, .metric-pill {
        color: var(--st-color-text);
    }
    </style>
    """, unsafe_allow_html=True)

    # Handle missing "Institution Type" gracefully
    institution_type = details.get("Institution Type", "Unknown")
    if institution_type == "Private":
        institution_class = "private-institution"
    elif institution_type == "Public":
        institution_class = "public-institution"
    else:
        institution_class = "unknown-institution"

    # Handle potentially missing City and State
    location = f"{details.get('City', 'Unknown City')}, {details.get('State', 'Unknown State')}"

    with st.container():
        st.markdown(f"""
        <div class="data-section {institution_class}">
            <h3 class="big-font">{college_name}</h3>
            <p class="small-font">{location}</p>
            <p class="small-font">{institution_type} Institution</p>
            <h5 class="small-font">Why It's a Hidden Gem:</h5>
            <ul>
                {"".join(f"<li>{reason}</li>" for reason in details.get("hidden_gem_reasons", ["Information not available"]))}
            </ul>
            <h5 class="small-font">Potential Downsides:</h5>
            <ul>
                {"".join(f"<li>{downside}</li>" for downside in details.get("potential_drawbacks", ["Information not available"]))}
            </ul>
            <h4 class="small-font">Notable Metrics:</h4>
            <div>
                {"".join(f'<span class="metric-pill">{metric}</span>' for metric in details.get("notable_metrics", ["No metrics available"]))}
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_cards(data, filter_key="", institution_type_filter="All", state_filters=[]):
    colleges = [college for college in data if filter_key.lower() in college.lower()]
    
    if institution_type_filter != "All":
        colleges = [college for college in colleges if data[college].get("Institution Type", "Unknown") == institution_type_filter]
    
    if state_filters:
        colleges = [college for college in colleges if data[college].get("State") in state_filters]
    
    colleges.sort()  # Always sort alphabetically
    
    num_cols = 3
    cols = st.columns(num_cols)
    for index, college_name in enumerate(colleges):
        with cols[index % num_cols]:
            display_college_card(college_name, data[college_name])

def get_all_states(data):
    states = set()
    for college in data.values():
        state = college.get("State")
        if state:
            states.add(state)
    return sorted(list(states))

def main():
    st.set_page_config(layout="wide")
    
    # Set the theme to light mode
    st.markdown("""
        <style>
        :root {
            --st-color-primary-10: #e6f3ff;
            --st-color-success-10: #e6ffe6;
            --st-color-secondary-10: #f0f0f0;
            --st-color-secondary-25: #e0e0e0;
            --st-color-text: #000000;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("The Quiet Prestige List")
    college_data = load_data()
    
    # Filtering options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_key = st.text_input("Search for colleges:")
    
    with col2:
        institution_type_filter = st.selectbox(
            "Filter by Institution Type",
            ["All", "Private", "Public", "Unknown"]
        )
    
    with col3:
        all_states = get_all_states(college_data)
        state_filters = st.multiselect(
            "Filter by State(s)",
            options=all_states,
            default=[]
        )

    display_cards(college_data, filter_key, institution_type_filter, state_filters)

if __name__ == "__main__":
    main()