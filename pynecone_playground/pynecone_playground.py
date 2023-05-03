import asyncio
import functools
import time

import pynecone as pc

from components import navbar
from function import SearchEngine, SummaryAgent
from pcconfig import config

from .styles import article_box_style, title_style

filename = f"{config.app_name}/{config.app_name}.py"

text_style = {
    "color": "green",
    "font_family": "Comic Sans MS",
    "font_size": "1.2em",
    "font_weight": "bold",
    "box_shadow": "rgba(1, 1, 1, 0.8) 5px 5px, rgba(1, 1, 1, 0.4) 10px 10px",
}


def add(sth):
    return sth + " sth "


class State(pc.State):
    """The app state."""

    username: str = ""  # Tim
    logged_in: bool = False  # True
    api_keystate: str = "info"

    # Search
    text: str = ""
    search_text: str = ""
    search_loading: bool = False
    titles: list = []
    _search_engine = SearchEngine()
    _src_metadatas: list = []

    # Summarize
    summary_text: str = ""
    summarize_loading: bool = True
    openai_apikey: str = ""
    openai_apikey_value: str = ""
    _summarize_agent = SummaryAgent()

    def search_process(self):
        self.search_loading = not self.search_loading

    def summarize_process(self):
        self.summarize_loading = not self.summarize_loading

    def set_text(self, text):
        self.text = text

    def search(self):
        self.initial_search()
        self.search_text = "intext:" + self.text
        self.titles, self._src_metadatas = self._search_engine.search(
            keys=self.search_text, when="1d"
        )

    async def summarize(self, title, num_sum=2):
        if not self.check_is_login:
            self.summary_text = "<strong>Please set up your openai api-key before running NewsGPT</strong>"
            return
        self.summary_text = ""
        err_msg = ""
        loop = asyncio.get_event_loop()
        cur_index = self.titles.index(title)
        # cur_src_meta = self._search_engine.fetch(self._src_metadatas[cur_index][2])
        cur_src_meta = await loop.run_in_executor(
            None,
            functools.partial(
                self._search_engine.fetch, rss_feed=self._src_metadatas[cur_index][2]
            ),
        )
        # await asyncio.sleep(0.2)
        is_valid_key, _ = self._summarize_agent.is_valid_api_key(
            apikey=self.openai_apikey
        )

        start = time.time()
        if isinstance(cur_src_meta, dict) and is_valid_key:
            related_titles = [cur_src_meta["title"]]
            related_summary_list = []
            # ai_response = self._summarize_agent.ask(message=cur_src_meta["body"], api_key=self.openai_apikey)
            ai_response = await loop.run_in_executor(
                None,
                functools.partial(
                    self._summarize_agent.ask,
                    message=cur_src_meta["body"],
                    api_key=self.openai_apikey,
                ),
            )
            if not ai_response.startswith("[error]"):
                related_summary_list.append(ai_response)
                rc_link = []
                src_img = cur_src_meta["image"]
                rc_link.append(cur_src_meta["url"])
                _, r_metadatas = self._search_engine.search(
                    "intext:" + cur_src_meta["title"], when="7d"
                )
                for r_i, r in enumerate(r_metadatas[1: num_sum + 1]):
                    # r_meta = self._search_engine.fetch(r[2])
                    r_meta = await loop.run_in_executor(
                        None,
                        functools.partial(
                            self._search_engine.fetch, rss_feed=r[2]),
                    )
                    # await asyncio.sleep(0.2)
                    if isinstance(r_meta, dict):
                        related_titles.append(r_meta["title"])
                        rc_link.append(r_meta["url"])
                        ai_response = await loop.run_in_executor(
                            None,
                            functools.partial(
                                self._summarize_agent.ask,
                                message=r_meta["body"],
                                api_key=self.openai_apikey,
                            ),
                        )
                        # ai_response = self._summarize_agent.ask(message=r_meta["body"], api_key=self.openai_apikey)
                        if not ai_response.startswith("[error]"):
                            related_summary_list.append(ai_response)
                        else:
                            err_msg += ai_response + ", "
                    # await asyncio.sleep(0.2)
            else:
                err_msg += ai_response


            if len(related_summary_list) == 0:
                self.summary_text = err_msg
            else:
                related_summary_list = ", ".join(
                    [
                        f"article {rsi}: {rs}"
                        for rsi, rs in enumerate(related_summary_list)
                    ]
                )
                # ai_final_out = self._summarize_agent.ask(message=related_summary_list, api_key=self.openai_apikey, state="finalize")
                ai_final_out = await loop.run_in_executor(
                    None,
                    functools.partial(
                        self._summarize_agent.ask,
                        message=related_summary_list,
                        api_key=self.openai_apikey,
                        state="finalize",
                    ),
                )
                # await asyncio.sleep(0.2)
                if ai_final_out.startswith("[error]"):
                    self.summary_text = ai_final_out
                else:
                    # html_out = self.form_output(final_response=ai_final_out, urls=rc_link, ref_titles=related_titles, src_img=src_img)
                    html_out = f"""
                            <div style="text-align:center;">
                                <img src={src_img} style="display:block; margin:auto; border-radius: 10px;">
                            </div><br>
                        """
                    html_out += ai_final_out
                    ref_list = [
                        f"<li><a href={url} style='color: blue;'>{title}</a></li>"
                        for url, title in zip(rc_link, related_titles)
                    ]
                    ref_list = f"<ul>{''.join(ref_list)}</ul>"
                    divider = '<br><hr style="border-top: 1px solid #ccc;">'
                    html_out += divider + "<br><p>Reference:</p>" + ref_list
                    self.summary_text = html_out.replace("/\n", "")
                    # await asyncio.sleep(0.2)
        else:
            self.summary_text = cur_src_meta
        end = time.time()
        print("Elapse: {}".format(end - start))
    
    def initial_search(self):
        self.search_text = ""
        self.summary_text = ""
        self.titles = []
        self._src_metadatas = []

    def clear_all_history(self):
        self.text = ""
        self.search_text = ""
        self.summary_text = ""
        self.titles = []
        self._src_metadatas = []

    def logout(self,):
        self.openai_apikey = ""
        self.openai_apikey_value = ""
        self.username = ""
        self.api_keystate = "info"

    def on_check_apikey(self):
        is_success, _ = self._summarize_agent.is_valid_api_key(
            apikey=self.openai_apikey_value)
        if is_success:
            self.openai_apikey = self.openai_apikey_value
            self.api_keystate = "success"
        else:
            self.openai_apikey = ""
            self.openai_apikey_value = ""
            self.username = ""
            self.api_keystate = "error"

    def set_openai_temp_key(self, key):
        self.openai_apikey_value = key

    def set_username(self, text):
        self.username = text.upper()

    @pc.var
    def check_is_login(self):
        return not self.openai_apikey == ""
    
    @pc.var
    def retrieve_api_keystate(self) -> str:
        return self.api_keystate


def article_card(data):
    return pc.container(
        pc.box(
            pc.text(data, style=title_style),
            on_click=[
                State.summarize_process,
                State.summarize(data),
                State.summarize_process,
            ],
            style=article_box_style,
            _hover={"cursor": "pointer"},
        ),
    )


def index() -> pc.Component:
    return pc.vstack(
        navbar(State),
        pc.grid(
            pc.grid_item(pc.spacer(), row_span=5, col_span=1),
            pc.cond(
                State.search_loading,
                pc.circular_progress(
                    is_indeterminate=True, position="absolute", top="50%", left="30%"
                ),
                pc.grid_item(
                    pc.vstack(
                        pc.foreach(State.titles, article_card),
                        overflow="auto",
                        height="750px",
                    ),
                    row_span=5,
                    col_span=3,
                    # bg="rgba(255,255,255, 0.9)",
                    margin_top="10em",
                    border_radius="20px",
                    box_shadow="7px -7px 14px #cccecf, -7px 7px 14px #ffffff",
                ),
            ),
            # pc.cond(
            #     State.summarize_loading,
            #     pc.circular_progress(
            #         is_indeterminate=True, position="absolute", top="50%", right="25%"
            #     ),
            #     pc.grid_item(
            #         pc.html(State.summary_text, padding="3em"),
            #         row_span=5,
            #         col_span=3,
            #         margin_top="10em",
            #         border_radius="20px",
            #         margin_left="50px",
            #         box_shadow="7px -7px 14px #cccecf, -7px 7px 14px #ffffff",
            #         overflow="auto",
            #         height="750px",
            #     ),
            # ),
            pc.grid_item(
                pc.skeleton_text(
                    pc.html(State.summary_text, padding="3em"),
                    no_of_lines=5,
                    start_color="pink.500",
                    end_color="orange.500",
                    is_loaded=State.summarize_loading,
                    padding="3em"
                ),
                row_span=5,
                col_span=3,
                margin_top="10em",
                border_radius="20px",
                margin_left="50px",
                box_shadow="7px -7px 14px #cccecf, -7px 7px 14px #ffffff",
                overflow="auto",
                height="750px",
            ),
            template_rows="repeat(5, 1fr)",
            template_columns="repeat(8, 1fr)",
            width="100%",
        ),
    )


# Add state and page to the app.
app = pc.App(
    state=State,
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Silkscreen&display=swap",
    ],
)
app.add_page(index)
app.compile()
