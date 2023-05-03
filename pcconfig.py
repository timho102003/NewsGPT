import pynecone as pc


config = pc.Config(
    app_name="pynecone_playground",
    # bun_path="$HOME/.bun/bin/bun",
    api_url="0.0.0.0:8000",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
    port=3000,
)