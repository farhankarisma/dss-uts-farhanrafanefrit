import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Welcome to My DSS App",
    page_icon="🌟",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom CSS for artistic design
st.markdown("""
    <style>
    /* Main page styling */
    .main {
        background: linear-gradient(to right, #ece9e6, #ffffff);
        color: #333333;
        font-family: 'Verdana', sans-serif;
    }
    h1 {
        color: #2E8B57;
        text-align: center;
        font-family: 'Helvetica', sans-serif;
        font-size: 3rem;
        margin-top: 30px;
        animation: fadeIn 2s ease-in-out;
    }
    h3 {
        color: #4169E1;
        font-size: 1.8rem;
        text-align: center;
        margin-bottom: 20px;
    }
    p {
        text-align: center;
        font-size: 1.2rem;
    }
    .content-block {
        text-align: center;
        margin-top: 50px;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
    }
    /* Add subtle animation */
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    .btn-primary {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
    }
    .btn-primary:hover {
        background-color: white;
        color: black;
        border: 2px solid #4CAF50;
    }
    hr {
        border: 1px solid #CCCCCC;
        width: 80%;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("<h1>Decision Support System 🌟</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Explore, Interact, and Enjoy the Experience!</p>", unsafe_allow_html=True)

# Main Content Section
st.markdown("<div class='content-block'><h3>Welcome to the DSS Application!</h3></div>", unsafe_allow_html=True)
st.write("""
    Use the sidebar to navigate through different decision support system methods, including **AHP**, **WP**, and **SAW**.
    Enhance your decision-making process with these powerful tools!
""")


# Sidebar styling
st.sidebar.markdown("""
    <style>
    .sidebar-content {
        font-family: 'Verdana', sans-serif;
        color: #333333;
        font-size: 1.1rem;
        padding: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Success message to show the app is working fine
st.success("App Loaded Successfully!")


