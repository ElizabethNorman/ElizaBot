"""
ElizaBot Version 1
A simple, fun discord bot made for my own amusement.
Made by Elizabeth Norman, @spicedboi
"""

import discord
from discord.ext import commands
import random
import praw
from profanity_check import predict


def check_for_no_repeat(s):
    for i in range(len(s)):
        for j in range(i + 1, len(s)):
            if s[i] == s[j] and str.isalpha(s[i]):
                return False
    return True


def get_char_unicode(c): 
    unicode_chars = ['\U0001F1E6', '\U0001F1E7', '\U0001F1E8', '\U0001F1E9', '\U0001F1Ea', '\U0001F1Eb', '\U0001F1Ec',
                     '\U0001F1Ed', '\U0001F1Ee', '\U0001F1Ef', '\U0001F1F0', '\U0001F1F1', '\U0001F1F2', '\U0001F1F3',
                     '\U0001F1F4', '\U0001F1F5', '\U0001F1F6', '\U0001F1F7', '\U0001F1F8', '\U0001F1F9', '\U0001F1Fa',
                     '\U0001F1Fb', '\U0001F1Fc', '\U0001F1Fd', '\U0001F1Fe', '\U0001F1Ff']
    return unicode_chars[ord(c) - 97]


def find_swears(s):
    s = [s]
    return predict(s)


def return_dan():
    file_no = random.randint(1, 3)
    return "dan" + str(file_no) + ".gif"


client = commands.Bot('.')
reddit = praw.Reddit(client_id='CLIENT ID',
                     client_secret='SECRET IT',
                     user_agent='bot fun', check_for_asynch=False)


@client.event
async def on_ready():
    print('we have logged in as {0.user}'.format(client))


@client.command()
async def prequel(ctx):
    memes_submissions = reddit.subreddit('PrequelMemes').hot()
    post_to_pick = random.randint(1, 25)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    await ctx.send(submission.url)


@client.command()
async def flipcoin(ctx):
    result = random.randint(1, 2)
    if result == 1:
        await ctx.send("heads")
    else:
        await ctx.send("tails")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    string = str.lower(message.content)
    if find_swears(string):
        embed = discord.Embed(title="You swore!", description="No swearing " + message.author.mention + "!")
        randy_dan = return_dan()
        file = discord.File("dangifs/" + randy_dan, filename=randy_dan)
        embed.set_image(url="attachment://" + randy_dan)
        await message.channel.send(file=file, embed=embed)
    elif check_for_no_repeat(string):
        for i in range(len(string)):
            if str.isalpha(string[i]):
                await message.add_reaction(get_char_unicode(string[i]))
    await client.process_commands(message)


client.run('DISCORD CLIENT ID')
