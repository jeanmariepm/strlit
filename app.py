
"""
This file is the framework for generating multiple Streamlit applications 
through an object oriented framework. 
"""

# Import necessary libraries
import streamlit as st
import analyze
import screen
import auth

# Define the multipage class to manage the multiple apps in our program


class MultiPage:

    def __init__(self) -> None:
        self.pages = []

    def add_page(self, title, func) -> None:
        """Class Method to Add pages to the project
        Args:
            title ([str]): The title of page which we are adding to the list of apps 

            func: Python function to render this page in Streamlit
        """

        self.pages.append({

            "title": title,
            "function": func
        })

    def run(self):
        # Drodown to select the page to run
        page = st.sidebar.selectbox(
            'App Navigation',
            self.pages,
            format_func=lambda page: page['title']
        )
        st.sidebar.markdown(
            """
            **About**
            - App source code <a href='https://github.com/jeanmariepm/strlit.git'>here </a>
            - Built in `Python` using `streamlit`,`yfinance`, `apitrader`, `postgres` and more
            """,
            unsafe_allow_html=True,
        )

        # run the app function
        if page['function'].__module__ == 'auth':
            st.session_state['user'] = page['function']()
        else:
            page['function'](st.session_state['user'])


# Title of the main page
st.header("VIP Applications")


# Create an instance of the app
if 'pages' not in st.session_state:
    pages = MultiPage()
    pages.add_page("Login", auth.run)
    pages.add_page("Analyze Stock", analyze.run)
    pages.add_page("Screen Stocks", screen.run)
    st.session_state['pages'] = pages

if 'user' not in st.session_state:
    st.session_state['user'] = None

# The main app
st.session_state['pages'].run()
