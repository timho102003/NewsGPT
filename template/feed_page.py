import streamlit as st
from streamlit_extras.row import row

from config import FEED_ARTICLE_NUMS, NEWS_CATEGORIES
from utils import generate_feed_layout, fetch_feeds


def feed_template():
    st.markdown(
        f"<h3 style='text-align:center;padding: 0px 0px;color:grey;font-size:200%;'>{st.session_state['realname']} Feed</h3><br>",
        unsafe_allow_html=True,
    )
    _, search_col, _ = st.columns([0.25, 0.5, 0.25])
    selections = ["Feed"] + NEWS_CATEGORIES if not st.session_state.is_guest else NEWS_CATEGORIES
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
            min_value=5,
            max_value=30,
            step=1,
            help="Choose articles from the last n days up to today.",
            key="feed_dayrange",
        )
        st.session_state.cat_selection = st.selectbox('Choose the news categories', 
                              options=selections, 
                              index=selections.index(st.session_state.get("cat_selection", "Feed" if not st.session_state.is_guest else "World")) \
                                if st.session_state.get("cat_selection", "Feed" if not st.session_state.is_guest else "World") != "search" else 0)
                # st.write(f'Selected option: {st.session_state.cat_selection}')

    if search_submit:
        st.session_state.cat_selection = "search"

    if st.session_state.get("cat_selection", "Feed") == "Feed":
        st.session_state.recommend = fetch_feeds(total_articles=FEED_ARTICLE_NUMS, data_range=st.session_state.feed_dayrange, thresh=0.5)
    elif st.session_state.get("cat_selection", "Feed") == "search":
        st.session_state.recommend = fetch_feeds(total_articles=FEED_ARTICLE_NUMS, 
                                                 data_range=st.session_state.feed_dayrange, 
                                                 mode=st.session_state.cat_selection,
                                                 search_msg=query_search,
                                                 thresh=0.4)
    else:
        st.session_state.recommend = fetch_feeds(total_articles=FEED_ARTICLE_NUMS, data_range=st.session_state.feed_dayrange, mode=st.session_state.cat_selection)
    generate_feed_layout()