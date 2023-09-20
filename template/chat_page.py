import readtime
import streamlit as st
from streamlit_extras.row import row
from streamlit_extras.switch_page_button import switch_page

from utils import (
    generate_anno_text,
    second_to_text,
    update_activities,
    update_negatives,
    update_positives,
)



prompt_content = {
    "5W1H": 'Summarize the content details in the "5W1H" approach (Who, What, When, Where, Why, and How) in bullet points',
    "Similar Viewpoints": "Compare between the articles and provide the similar viewpoints in bullet points",
    "Discrepency Viewpoints": "Compare between the articles and provide the discrepency viewpoints in bullet points"
}

def predefine_prompt():
    st.session_state.initial_prompt.append(prompt_content[st.session_state.prompt_selection])


def chat_template():
    title = st.session_state["active_chat_result"]["title"]
    image = st.session_state["active_chat_result"]["image"]
    author = st.session_state["active_chat_result"]["author"]
    publish = st.session_state["active_chat_result"]["publish"]
    reference = st.session_state["active_chat_result"]["reference"]
    id = st.session_state["active_chat_result"]["id"]
    category = st.session_state["active_chat_result"]["category"]
    ori_tot_readtime = st.session_state["active_chat_result"]["ori_tot_readtime"]
    ner_loc = st.session_state["active_chat_result"]["ner_loc"]
    ner_org = st.session_state["active_chat_result"]["ner_org"]
    ner_per = st.session_state["active_chat_result"]["ner_per"]

    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
    with col2:
        go_back_to_feed = st.button(
            "Back To Feed",
            on_click=update_activities,
            kwargs={
                "title": title,
                "id": id,
                "category": category,
                "summary_rt": st.session_state.reading_time,
                "ori_rt": ori_tot_readtime,
                "ner_loc": ner_loc,
                "ner_org": ner_org,
                "ner_per": ner_per,
                "chat_mode": True,
            },
        )
        if go_back_to_feed:
            st.session_state["page_name"] = "feed"
            switch_page("home")

        with st.container():
            st.markdown(
                """
            <style>
                .title {
                    text-align: center;
                    font-size: 200%;
                    font-weight: bold;
                    color: black;
                    margin-bottom: 10px;
                    padding: 10px;
                    border-radius: 10px;
                }
                .author-publish, .read-time {
                    text-align: center;
                    font-size: 80%;
                    color: grey;
                    margin: 5px 0;
                }
                .summary-heading, .similarity-heading, .difference-heading {
                    text-align: justify;
                    font-size: 150%;
                    font-weight: bold;
                    color: white;
                    margin-top: 20px;
                    padding: 10px;
                    border-radius: 10px;
                    max-width: 90%;
                }
                .centered-image img {
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                    border-radius: 10px; /* Rounded corners */
                    max-width: 100%; /* Responsive */
                }
                .content {
                    text-align: justify;
                    margin: 0 auto;
                    max-width: 90%; /* Adjust to match the image width */
                }
            </style>
            """,
                unsafe_allow_html=True,
            )

            st.markdown("<div class='rounded-container'>", unsafe_allow_html=True)
            st.markdown(f"<div class='title'>{title}</div>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='centered-image'><img src='{image}' alt='Image'></div>",
                unsafe_allow_html=True,
            )  # Centered and rounded image
            st.markdown(
                f"<p class='author-publish'>category: {category}</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p class='author-publish'>author: {author}</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p class='author-publish'>published: {publish}</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p class='author-publish'>reference article number: {len(reference)}</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p class='read-time'>NewsGPT help you save: {second_to_text(ori_tot_readtime - st.session_state.reading_time)}</p>",
                unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("Tags"):
                if ner_org:
                    generate_anno_text(ner_org, label="ORG")
                if ner_per:
                    generate_anno_text(ner_per, label="PER")
                if ner_loc:
                    generate_anno_text(ner_loc, label="LOC")

            with st.expander("Reference Article Links"):
                for r_i, ref in enumerate(reference):
                    st.markdown(f'{r_i}. [{ref["title"]}]({ref["url"]})')

    thumbtext, thumbbt1, thumbbt2, _ = st.columns([0.4, 0.1, 0.1, 0.4])
    is_like = thumbbt1.button(
        "👍",
        on_click=update_positives,
        kwargs={
            "title": title,
            "id": id,
            "category": category,
            "ner_loc": ner_loc,
            "ner_org": ner_org,
            "ner_per": ner_per,
        },
        help="I like the news content, please recommend more",
    )

    not_like = thumbbt2.button(
        "👎",
        on_click=update_negatives,
        kwargs={
            "title": title,
            "id": id,
            "category": category,
            "ner_loc": ner_loc,
            "ner_org": ner_org,
            "ner_per": ner_per,
        },
        help="I don't like the news content, please don't feed to me",
    )
    if is_like:
        st.toast(f"Thanks for liking the summary and article: {title}", icon="👍")

    if not_like:
        st.toast(f"We will make the recommendation better for you. Trust us!", icon="👎")

    prompt = st.chat_input("Ask me any question about the news")
    if st.session_state.initial_prompt:
        prompt = st.session_state.initial_prompt.pop(0)
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:  # Display the prior chat messages
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message(
            "assistant",
        ):
            with st.spinner("Thinking..."):
                # response = st.session_state["chat_engine"].chat(prompt)
                try:
                    response = st.session_state["chat_engine"].query(prompt)
                    response = response.response
                except:
                    response = "Unable to retrieve the result due to some unexpected reason."
                st.write(response)
                message = {"role": "assistant", "content": response}
                st.session_state.reading_time += readtime.of_text(
                    response
                ).seconds
                st.session_state.messages.append(
                    message
                )  # Add response to message history

                print(st.session_state.reading_time)
    predefine_prompt_row = row(
        [0.05, 0.15, 0.15, 0.3, 0.15, 0.15, 0.05],
        vertical_align="center",
        gap="medium",
    )
    if len(reference) > 1:
        for _ in range(3):
            predefine_prompt_row.write("")

        predefine_prompt_row.selectbox('Predefined Prompt', 
                    options=["", "5W1H", "Similar Viewpoints", "Discrepency Viewpoints"], 
                    index=0,
                    key="prompt_selection",
                    on_change=predefine_prompt)
            
        # predefine_prompt_row.button(
        #     "5W1H",
        #     on_click=predefine_prompt,
        #     kwargs={
        #         "prompt": 'Summarize the content details in the "5W1H" approach (Who, What, When, Where, Why, and How) in bullet points'
        #     },
        # )
        # predefine_prompt_row.button(
        #     "Similar Viewpoints",
        #     on_click=predefine_prompt,
        #     kwargs={
        #         "prompt": "Compare between the articles and provide the similar viewpoints in bullet points"
        #     },
        # )
        # predefine_prompt_row.button(
        #     "Discrepency Viewpoints",
        #     on_click=predefine_prompt,
        #     kwargs={
        #         "prompt": "Compare between the articles and provide the discrepency viewpoints in bullet points"
        #     },
        # )
