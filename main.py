from  discord.ext import commands
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import discord

client = commands.Bot(command_prefix='>', case_insensitive=True)

@client.event
async def on_ready():
    sns.set_theme(context='notebook', style="whitegrid", palette="bright")
    print(f"Logged as {client.user.name} : {client.user.id}")
    
@client.command()
async def hi(ctx):
    await ctx.send(f"Hi {ctx.author.mention}")

@client.command()
async def chanel(ctx):
    await ctx.send(f"kanał: {ctx.guild}")

@client.command()
async def msgs(ctx):
    guild =  ctx.guild
    df = pd.DataFrame(columns=['author','kanał','time','content'])
    for kanał in guild.text_channels:
        async for msg in kanał.history(limit = 100000):
            if msg.author == ctx.author:
                df=df.append({'author': ctx.author ,'kanał': str(kanał.name),'time': msg.created_at,'content':msg.content}, ignore_index=True)
    s = io.BytesIO()
    order = df['kanał'].value_counts().index
    sns.countplot(data=df, x='kanał', hue='kanał', dodge=False, order=order)
    plt.xlabel(None)
    plt.ylabel(None)
    plt.savefig(s, format='png', dpi = 100)
    plt.close()
    s.seek(0)
    e = discord.Embed(title="Twoje wiadomości według kanału")
    chart = discord.File(s, filename="chart.png")
    e.set_image(url="attachment://chart.png")
    await ctx.send(embed = e, file= chart)
    
client.run(os.environ.get('DC_BOT'))

