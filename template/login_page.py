from time import sleep

import streamlit as st
from streamlit_extras.row import row
from streamlit_extras.switch_page_button import switch_page

from utils import check_is_sign_up, password_entered, sign_up


# TODO: Google Login
def login_template():
    st.markdown(
        "<h3 style='text-align:center;padding: 0px 0px;color:grey;font-size:200%;'>NewsGPT Login</h3><br>",
        unsafe_allow_html=True,
    )
    submitted = False
    col1, col2, col3 = st.columns([0.3, 0.3, 0.3])
    with col2:
        with st.form("login_form", clear_on_submit=True):
            username = st.text_input(
                "Username 👇",
                label_visibility="visible",
                disabled=False,
                placeholder="username",
            )

            password = st.text_input(
                "Password 👇",
                label_visibility="visible",
                disabled=False,
                placeholder="password",
                type="password",
            )
            submitted = st.form_submit_button("LOGIN", use_container_width=True)
            if submitted and password and username:
                password_entered(username=username, password=password)
                if not st.session_state["password_correct"]:
                    st.error("😕 User not known or password incorrect")
                else:
                    st.success(
                        "Hi {} 👋, Welcome to NewsGPT".format(
                            st.session_state["realname"]
                        )
                    )
                    sleep(1)
                    st.session_state["page_name"] = "feed"
                    switch_page("home")
            elif submitted:
                st.warning("Please enter the username and password before you click login buttom")
                sleep(1.5)
                st.session_state["page_name"] = "login"
                switch_page("home")
        # google_signin = st.button("Sign In with Google", use_container_width=True)
        issignup = st.button("SIGN UP", type="secondary", use_container_width=True)
        if issignup:
            st.session_state["page_name"] = "signup"
            switch_page("home")
        guest_login = st.button("Guest Login", type="secondary", use_container_width=True)
        if guest_login:
            password_entered(username="", password="", guest=True)
            st.warning("Personlization and time saving monitor will be disabled with guest login")
            sleep(2)
            st.session_state["page_name"] = "feed"
            switch_page("home")


def signup_template():
    st.markdown(
        "<h3 style='text-align:center;padding: 0px 0px;color:grey;font-size:200%;'>NewsGPT Sign Up</h3><br>",
        unsafe_allow_html=True,
    )
    submitted = False
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col2:
        with st.form("login_form", clear_on_submit=True):
            username = st.text_input(
                "Username 👇",
                label_visibility="visible",
                disabled=False,
                placeholder="username",
            )
            password = st.text_input(
                "Password 👇",
                label_visibility="visible",
                disabled=False,
                placeholder="password",
                type="password",
            )
            firstname = st.text_input(
                "First Name 👇",
                label_visibility="visible",
                disabled=False,
                placeholder="first name",
            )
            lastname = st.text_input(
                "Last Name 👇",
                label_visibility="visible",
                disabled=False,
                placeholder="last name",
            )
            options = st.multiselect(
                "What are your favorite news categories",
                [
                    "technology",
                    "science",
                    "sport",
                    "entertainment",
                    "world",
                    "nation",
                    "business",
                ],
            )
            submitted = st.form_submit_button("SIGN UP")

            if submitted:
                st.session_state["page_name"] = "login"
                if not check_is_sign_up(username=username):
                    if not username or not password:
                        st.error("Please set up the username and password")
                        st.experimental_rerun()
                    if not firstname:
                        firstname = username
                    if not lastname:
                        lastname = ""
                    success, signup_info = sign_up(
                        username, password, lastname, firstname, options
                    )
                    if not success:
                        st.error(signup_info)
                        sleep(1)
                        st.experimental_rerun()
                    else:
                        st.success(signup_info)
                        sleep(1)
                        switch_page("home")
                else:
                    switch_page("home")
