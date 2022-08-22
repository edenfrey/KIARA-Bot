
from ast import parse
from prediction_model.code.TextClassifier import TextClassifier
import os
from dotenv import load_dotenv
import hikari
import lightbulb
import requests
import json
from serpapi import GoogleSearch

load_dotenv()
text_classifier = TextClassifier()
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
TEST_GUILD_ID = os.getenv("TEST_GUILD")
BOT_ID = os.getenv("BOT_ID_STRING")
RANDOM_FACTS_API = "https://uselessfacts.jsph.pl/random.json?language=en"
TODAY_FACT_API = "https://uselessfacts.jsph.pl/today.json?language=en"
SERP_API_KEY = os.getenv("SERP_API_KEY")

# Instantiate Bot
bot = lightbulb.BotApp(token=BOT_TOKEN)

# Events
@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print("KIARA is Online")
    return

@bot.listen(hikari.GuildMessageCreateEvent)
async def ping(event) -> None:
    if event.is_bot or not event.content:
        return
    elif event.content.startswith(BOT_ID):
        type = text_classifier.predict(event.content)
        if type == "SENTENCE":
            await event.message.respond("Cool! I can't really understand fully yet but I'm learning!")
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
        else:
            response = requests.get(RANDOM_FACTS_API)
            data = response.text
            parse_json = json.loads(data)
            fact = parse_json["text"]
            src = parse_json['source_url']
            res = fact + "\nSource: " + src
            await event.message.respond(res)


# Commands
@bot.command
@lightbulb.command('ping','Replies Pong!')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(context):
    await context.respond('Pong!')

@bot.command
@lightbulb.command('search','Search Test')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(context):
    QUERY = "empire state building"
    JSON_LINK = "https://serpapi.com/search.json?engine=google&q=" + QUERY + "&google_domain=google.com&gl=my&hl=en&start=1&num=5&device=mobile&api_key=" + SERP_API_KEY
    response = requests.get(JSON_LINK)
    data = response.text
    parse_json = json.loads(data)
    await context.respond("Here are some results i found :)")
    for i in parse_json['organic_results']:
        res = ""
        TITLE = i['title']
        LINK = i['link']
        res = TITLE  + "\n" + LINK
        await context.respond(res)
    await context.respond('Pong!')

bot.run()