from zoombot.core import Bot
from my_bot import MyBot

API_KEY = "_pg_qA-LQ7WCJJwXcByuxQ"
CLIENT_SECRET = "bEkJqvBHs5ByLmFgVfMluGUuK35gNwxZ"
CLIENT_ID = "un61Md2Q6CVf5BHYQ9CGw"
BOT_JID = "v1wfkk51tktg6ewqwtvusvzg@xmpp.zoom.us"
VERIFICATION_TOKEN = "6jHAI_XnRe26qVXQX-b08A"


def main():
    bot = MyBot(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        bot_jid=BOT_JID,
        verification_token = VERIFICATION_TOKEN
    )

    bot.run()


if __name__ == "__main__":
    main()
