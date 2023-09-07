import streamlit as st

from utils import summary_layout_template


def summary_template():
    summary_layout_template(**st.session_state["active_summary_result"])
