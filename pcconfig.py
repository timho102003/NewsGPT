import pynecone as pc

config = pc.Config(
    app_name="pynecone_playground",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)
