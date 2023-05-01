import pynecone as pc


def input_field(input_width, input_value, holder, func_change, _type):
    return pc.input(
        width=input_width,
        value=input_value,
        placeholder=holder,
        fontSize="13px",
        type_=_type,
        on_blur=func_change,
    )


def alert_layout(status):
    return \
        pc.alert(
            pc.alert_icon(),
            pc.alert_title("openai key status: " + status),
            status=status,
        )


def navbar(State):
    """The navbar."""
    return pc.box(
        pc.hstack(
            pc.link(
                pc.heading("NewsGPT", font_size="1.75em",
                           on_click=State.clear_history),
                href="/",
            ),
            pc.spacer(),
            pc.hstack(
                pc.input(
                    placeholder="New Topic?",
                    value=State.text,
                    on_change=State.set_text,
                    border_radius="20px",
                    width="400px",
                ),
                pc.button(
                    "Search",
                    bg="lightgreen",
                    color="black",
                    is_active=True,
                    on_click=[State.search_process,
                              State.search, State.search_process],
                    size="sm",
                    border_radius="1em",
                    variant="outline",
                    _hover={
                        "opacity": 0.6,
                    },
                ),
            ),
            pc.spacer(),
            pc.menu(
                pc.cond(
                    State.check_is_login,
                    pc.menu_button(pc.avatar(name=State.username, size="md"),),
                    pc.menu_button(
                        "Login",
                        margin_right="30px",
                        border_radius="1em",
                        _hover={
                            "opacity": 0.6,
                        },
                        width="100px",
                        height="30px",
                        color="black",
                        background="rgba(0,0,0,0.1)"
                    )
                ),
                pc.menu_list(
                    pc.cond(
                        State.check_is_login,
                        pc.vstack(
                            pc.center(
                                pc.vstack(
                                    pc.avatar(name=State.username, size="md"),
                                    pc.text(State.username),
                                )
                            ),
                            pc.menu_divider(),
                            pc.link(
                                pc.menu_item("Sign Out"),
                                on_click=State.logout
                            ),
                        ),
                        pc.vstack(
                            pc.input(
                                placeholder="username",
                                on_blur=State.set_username,
                                border_radius="10px",
                                width="80%",
                                type_="text",
                            ),
                            pc.input(
                                placeholder="openai api-key",
                                on_blur=State.set_openai_temp_key,
                                border_radius="10px",
                                width="80%",
                                type_="password",
                            ),
                            alert_layout(status=State.retrieve_api_keystate),
                            pc.button(
                                "Submit",
                                bg="lightgreen",
                                color="black",
                                is_active=True,
                                on_click=[State.on_check_apikey, State.clear_history],
                                size="sm",
                                border_radius="1em",
                                variant="outline",
                                _hover={
                                        "opacity": 0.6,
                                },
                            ),
                            align_items="center",
                        ),
                    ),
                ),
            ),
            border="0.2em solid rgba(0,0,0,0.5)",
            padding_x="2em",
            padding_y="0.5em",
            border_radius="20px",
            align_items="center",
        ),
        position="fixed",
        width="70%",
        top="0px",
        z_index="500",
        margin_top="20px",
    )
