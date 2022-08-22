# Import necessary modules and libraries
import os
from prediction_model.code.TextClassifier import TextClassifier # Import self-made classifier model.
from dotenv import load_dotenv # To retrieve secret environment variables from .env

# Discord Bot Modules
import hikari
import lightbulb

# API Data Requesting and Processing
import requests # API requesting
import json # For loading and reading requested data

text_classifier = TextClassifier() # Instantiate text classifier

# Retrieve Secret Environment Variables and Constants
load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
TEST_GUILD_ID = os.getenv("TEST_GUILD")
BOT_ID = os.getenv("BOT_ID_STRING")
SERP_API_KEY = os.getenv("SERP_API_KEY")
# Link for Facts API Fetching
RANDOM_FACTS_API = "https://uselessfacts.jsph.pl/random.json?language=en"
TODAY_FACT_API = "https://uselessfacts.jsph.pl/today.json?language=en"

# Instantiate Bot
bot = lightbulb.BotApp(token=BOT_TOKEN)

# Events
@bot.listen(hikari.StartedEvent)
async def on_started(event):
    """
    To print in console if bot successfully started.
    """
    print("KIARA is now online!")
    return

@bot.listen(hikari.GuildMessageCreateEvent)
async def on_read_message(event) -> None:
    """
    Reads all messages in guild and checks if KIARA is mentioned in the beginning. If it is, runs text classification and performs necessary task.
    """
    if event.is_bot or not event.content: # If message from bot or no content, return.
        return
    elif event.content.startswith(BOT_ID): # If message starts with "@KIARA" mentioned, perform task.
        # Remove name and perform classification
        sentence = event.content.split(' ',1)[1] 
        type = text_classifier.predict(sentence)

        # If it is a simple sentence and statement, simply answer with pre-curated text.
        if type == "SENTENCE":
            await event.message.respond("Cool! I can't really understand fully yet but I'm learning!")

        # If it is a question, perform query to SerpAPI to perform google search. Give results.
        elif type == "QUESTION":
            QUERY = event.content.split(' ',1)[1]
            JSON_LINK = "https://serpapi.com/search.json?engine=google&q=" + QUERY + "&google_domain=google.com&gl=my&hl=en&start=1&num=5&device=mobile&api_key=" + SERP_API_KEY
            response = requests.get(JSON_LINK)
            data = response.text
            parse_json = json.loads(data)
            await event.message.respond("Here are some results i found :)")
            for i in parse_json['organic_results']:
                res = ""
                TITLE = i['title']
                LINK = i['link']
                res = TITLE  + "\n" + LINK
                await event.message.respond(res)

        # IF it is a request for a fact, perform API fetch from FactAPI and give result.
        elif type == "FACTREQ":
            response = requests.get(RANDOM_FACTS_API)
            data = response.text
            parse_json = json.loads(data)
            fact = parse_json["text"]
            src = parse_json['source_url']
            res = fact + "\nSource: " + src
            await event.message.respond(res)
    else:
        return


# Commands
@bot.command
@lightbulb.command('ping','Replies Pong!')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(context):
    """
    Simple command. If "/ping" is called, reply with Pong!
    """
    await context.respond('Pong!')

bot.run()