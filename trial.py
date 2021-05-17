import requests, os, discord
from discord.ext import commands
from dotenv import load_dotenv
from bs4 import BeautifulSoup

client = commands.Bot(command_prefix="!")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')
ID_TOKEN = os.getenv('ID_TOKEN')
USER_AGENT = os.getenv('USER_AGENT')

headers = {
    'cookie': "id_token= {}".format(ID_TOKEN),
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'user-agent': USER_AGENT,
}


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD_ID:
            break
    
    print(
        f'{client.user} is connected to the following guild :\n'
        f'{guild.name}(id: {guild.id})'
    )


session = requests.Session()
@client.command()
async def chegg(ctx, arg):
    try:


        if "https://www.chegg.com/homework-help/" not in arg: 
            await ctx.channel.send(ctx.author.mention + "This is not a chegg link!")
            return
        else:
            

            
            page = session.get(arg,headers=headers)
            pageContent = page.content
            soup = BeautifulSoup(pageContent,"html.parser")

            answerDiv = soup.find("div",{"class":"answer-given-body ugc-base"})
            answerImages = answerDiv.findAll('img')
            answerText = answerDiv.getText()


        
            for image in answerImages:
                await ctx.author.send(image['src'])

            if(not answerText):
                return

            await ctx.author.send('#######################################')
            


            file = open('answer.txt', 'w')
            file.write(answerText)
            file.close()
            my_files = [discord.File('answer.txt')]
            await ctx.author.send(files=my_files)
    except:
        await ctx.author.send("there is no text to send or something went wrong!")
        pass



client.run(TOKEN)