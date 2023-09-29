import json
import time

import streamlit as st
from firebase_admin import firestore
from google.oauth2 import service_account
from streamlit_extras.buy_me_a_coffee import button as coffee_button
from streamlit_extras.switch_page_button import switch_page

from template.chat_page import chat_template
from template.feed_page import feed_template
from template.login_page import login_template, signup_template
from template.summary_page import summary_template
from utils import load_activities, second_to_text, signout

st.set_page_config(page_title="", page_icon="👋", layout="wide")

with st.sidebar:
    coffee_button(username="timho102003", floating=False, width=221)
    is_signout = st.button("Sign Out")
    if is_signout:
        if not st.session_state.get("is_auth_user", False):
            st.warning("Please login first to sign out")
        else:
            signout()
            st.success("Successfully sign out, Please sign in as different user")
        time.sleep(1)
        switch_page("home")
    st.divider()
    if st.session_state.get("is_auth_user", False) and not st.session_state.get("is_guest", False):
        user_meta = st.session_state["user_ref"].get()
        user_meta = user_meta.to_dict()
        tot_readtime = 0
        tot_savetime = 0
        readtime_last = 0
        savetime_last = 0
        col1, col2 = st.columns(2)
        if "save_time" in user_meta:
            savetime_last = user_meta["save_time"][-1]
            tot_savetime = sum(user_meta["save_time"])
            col1.metric(
                "Total Save Time",
                second_to_text(tot_savetime, True),
                second_to_text(savetime_last, True),
                help="Read time in total",
            )
        if "readtime" in user_meta:
            readtime_last = user_meta["readtime"][-1]
            tot_readtime = sum(user_meta["readtime"])
            col2.metric(
                "Total Read Time",
                second_to_text(tot_readtime, True),
                second_to_text(readtime_last, True),
                help="NewsGPT saves you time in total",
            )
        if "activities" in user_meta:
            gb_time_df, gb_cat_df = load_activities(user_meta["activities"])
            st.divider()
            st.area_chart(
                gb_time_df,
                x="timestamp",
                y="read cnt",
            )
            st.divider()
            st.bar_chart(
                gb_cat_df,
                x="category",
                y="read cnt",
            )

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
st.session_state["firestore_db"] = firestore.Client(credentials=creds)
# st.session_state["firestore_db"] = firestore.Client.from_service_account_json("assets/newsgpt_firebase_serviceAccount.json")

if st.session_state.get("error", None):
    st.toast(f'Something went wrong: {st.session_state["error"]}')
    st.session_state["error"] = None

if st.session_state.get("page_name", "login") == "login":
    login_template()
elif st.session_state.get("page_name", "login") == "signup":
    signup_template()
elif st.session_state.get("page_name", "login") == "feed":
    feed_template()
elif st.session_state.get("page_name", "login") == "summary":
    summary_template()
elif st.session_state.get("page_name", "login") == "chat_mode":
    chat_template()
