import os
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
import aiohttp

# --- CONFIGURATION ---
TOKEN = "your_token"
# ---------------------

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        print("🔄 Synchronizing...")
        await self.tree.sync()
        print("✨ Successfully Synchronized !")

bot = MyBot()

async def upload_to_gofile(file_path):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("https://api.gofile.io/servers") as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                server = data["data"]["servers"][0]["name"]
            
            url = f"https://{server}.gofile.io/uploadFile"
            data_form = aiohttp.FormData()
            data_form.add_field('file', open(file_path, 'rb'), filename=os.path.basename(file_path))
            
            async with session.post(url, data=data_form) as resp:
                if resp.status != 200:
                    return None
                result = await resp.json()
                if result["status"] == "ok":
                    return result["data"]["downloadPage"]
        except Exception as e:
            print(f"Erreur Gofile: {e}")
    return None

@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user.name}")

@bot.tree.command(name="mp3", description="Télécharge l'audio d'une vidéo YouTube en MP3")
@app_commands.describe(url="Lien de la vidéo YouTube")
async def download_mp3(interaction: discord.Interaction, url: str):
    await interaction.response.defer(thinking=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }
    
    loop = asyncio.get_event_loop()
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=True))
            filename = ydl.prepare_filename(info).replace(f".{info['ext']}", ".mp3")
    except yt_dlp.utils.DownloadError:
        await interaction.followup.send("❌ **Invalid link or link cannot be retrieved.** Make sure the video is public.")
        return
    except Exception as e:
        await interaction.followup.send(f"❌ An unexpected error has occurred : {e}")
        return

    file_size = os.path.getsize(filename)
    MAX_SAFE_SIZE = 23 * 1024 * 1024

    if file_size <= MAX_SAFE_SIZE:
        await interaction.followup.send(file=discord.File(filename))
    else:
        status_msg = await interaction.followup.send("📦 The audio file is too large for Discord. Uploading to Gofile.io...")
        download_link = await upload_to_gofile(filename)
        if download_link:
            await status_msg.edit(content=f"✅ MP3 Download Link : {download_link}")
        else:
            await status_msg.edit(content="❌ Uploade to Gofile failed.")

    if os.path.exists(filename):
        os.remove(filename)


@bot.tree.command(name="mp4", description="Télécharge une vidéo YouTube en MP4")
@app_commands.describe(url="Lien de la vidéo YouTube")
async def download_mp4(interaction: discord.Interaction, url: str):
    await interaction.response.defer(thinking=True)
    
    ydl_opts = {
        'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
    }
    
    loop = asyncio.get_event_loop()
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=True))
            filename = ydl.prepare_filename(info)
    except yt_dlp.utils.DownloadError:
        await interaction.followup.send("❌ **Invalid link or link cannot be retrieved.** Make sure the video is public.")
        return
    except Exception as e:
        await interaction.followup.send(f"❌ An unexpected error has occurred : {e}")
        return

    file_size = os.path.getsize(filename)
    MAX_SAFE_SIZE = 23 * 1024 * 1024

    if file_size <= MAX_SAFE_SIZE:
        try:
            await interaction.followup.send(file=discord.File(filename))
        except discord.errors.HTTPException:
            status_msg = await interaction.followup.send("📦 File rejected by Discord (close to the limit). Uploading to Gofile.io...")
            download_link = await upload_to_gofile(filename)
            if download_link:
                await status_msg.edit(content=f"✅ MP4 Download Link : {download_link}")
            else:
                await status_msg.edit(content="❌ Uploade to Gofile failed.")
    else:
        status_msg = await interaction.followup.send("📦 The video exceeds the Discord limit. Transfer to Gofile.io...")
        download_link = await upload_to_gofile(filename)
        if download_link:
            await status_msg.edit(content=f"✅ MP4 Download Link : {download_link}")
        else:
            await status_msg.edit(content="❌ Échec de l'upload vers Gofile.")

    if os.path.exists(filename):
        os.remove(filename)

if not os.path.exists("downloads"):
    os.makedirs("downloads")

bot.run(TOKEN)