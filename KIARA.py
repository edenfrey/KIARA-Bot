from prediction_model.code.TextClassifier import TextClassifier
import os
from dotenv import load_dotenv
import hikari


load_dotenv()
text_classifier = TextClassifier()
bot_token = os.getenv("DISCORD_BOT_TOKEN")
bot = hikari.GatewayBot(token=bot_token)


@bot.listen()
async def ping(event: hikari.GuildMessageCreateEvent) -> None:
    # If a non-bot user sends a message "hk.ping", respond with "Pong!"
    # We check there is actually content first, if no message content exists,
    # we would get `None' here.
    if event.is_bot or not event.content:
        return

    if event.content.startswith("Kiara"):
        text = "may i have a fact please"
        pred = text_classifier.predict(text)
        await event.message.respond(pred)


bot.run()