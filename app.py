
"""
This file is the framework for generating multiple Streamlit applications 
through an object oriented framework. 
"""

# Import necessary libraries
import streamlit as st
import analyze
import screen

# Define the multipage class to manage the multiple apps in our program


class MultiPage:
    """Framework for combining multiple streamlit applications."""

    def __init__(self) -> None:
        """Constructor class to generate a list which will store all our applications as an instance variable."""
        self.pages = []
        st.sidebar.markdown(
            """
            **About**
            - App source code <a href='https://github.com/jeanmariepm/strlit.git'>here </a>
            - Built in `Python` using `streamlit`,`yfinance`, `plotly`, `pandas` and more
            """,
            unsafe_allow_html=True,
        )

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

        # run the app function
        page['function']()


# Create an instance of the app
pages = MultiPage()

# Title of the main page
st.header("VIP Applications")


# Add all your applications (pages) here
pages.add_page("Analyze Stock", analyze.run)
pages.add_page("Screen Stocks", screen.run)

# The main app
pages.run()
