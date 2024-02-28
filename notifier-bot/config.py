import tomli

config = None

with open("config.toml", "rb") as f:
    try:
        config = tomli.load(f)
    except tomli.TOMLDecodeError:
        print("Failed to load configuration. Please check the formatting of config.toml")
        exit(-1)

token = config["bot"]["token"]
default_channel_id = config["bot"]["default_channel_id"]
default_color = config["bot"]["default_color"]
reddit_client_id = config["reddit"]["client_id"]
reddit_client_secret = config["reddit"]["client_secret"]
reddit_user_agent = config["reddit"]["user_agent"]
watchers = config["watchers"]
