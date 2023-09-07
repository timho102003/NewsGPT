import streamlit as st
from streamlit_extras.row import row

from config import FEED_ARTICLE_NUMS, NEWS_CATEGORIES
from utils import generate_feed_layout, load_cat_feed, load_feeds, load_search_feed


def feed_template():
    st.markdown(
        f"<h3 style='text-align:center;padding: 0px 0px;color:grey;font-size:200%;'>{st.session_state['realname']} Feed</h3><br>",
        unsafe_allow_html=True,
    )
    st.session_state.feed_dayrange = 3
    _, search_col, _ = st.columns([0.25, 0.5, 0.25])
    with search_col:
        with st.form("Search Form", clear_on_submit=True):
            search_row = row(spec=[0.8, 0.2], vertical_align="bottom", gap="medium")
            query_search = search_row.text_input(
                "Search",
                label_visibility="visible",
                placeholder="search the news",
            )
            search_submit = search_row.form_submit_button(label="Submit")

        st.number_input(
            "Day Range",
            min_value=1,
            max_value=30,
            step=1,
            help="Choose articles from the last n days up to today.",
            key="feed_dayrange",
        )
        cat_selection = st.multiselect(
            label="News Categories",
            options=["Feed"] + NEWS_CATEGORIES,
            max_selections=1,
        )

    if search_submit:
        cat_selection = ["search"]

    if not cat_selection or cat_selection[0] == "Feed":
        load_feeds(
            total_articles=FEED_ARTICLE_NUMS, data_range=st.session_state.feed_dayrange
        )
        generate_feed_layout()
    elif cat_selection[0] == "World":
        load_cat_feed(
            category="world",
            total_articles=FEED_ARTICLE_NUMS,
            data_range=st.session_state.feed_dayrange,
        )
        generate_feed_layout()
    elif cat_selection[0] == "Nation":
        load_cat_feed(
            category="nation",
            total_articles=FEED_ARTICLE_NUMS,
            data_range=st.session_state.feed_dayrange,
        )
        generate_feed_layout()
    elif cat_selection[0] == "Technology":
        load_cat_feed(
            category="Technology",
            total_articles=FEED_ARTICLE_NUMS,
            data_range=st.session_state.feed_dayrange,
        )
        generate_feed_layout()
    elif cat_selection[0] == "Science":
        load_cat_feed(
            category="science",
            total_articles=FEED_ARTICLE_NUMS,
            data_range=st.session_state.feed_dayrange,
        )
        generate_feed_layout()
    elif cat_selection[0] == "Entertainment":
        load_cat_feed(
            category="entertainment",
            total_articles=FEED_ARTICLE_NUMS,
            data_range=st.session_state.feed_dayrange,
        )
        generate_feed_layout()
    elif cat_selection[0] == "Business":
        load_cat_feed(
            category="business",
            total_articles=FEED_ARTICLE_NUMS,
            data_range=st.session_state.feed_dayrange,
        )
        generate_feed_layout()
    elif cat_selection[0] == "search":
        load_search_feed(
            search_msg=query_search,
            total_articles=FEED_ARTICLE_NUMS,
            data_range=st.session_state.feed_dayrange,
        )
        generate_feed_layout()
