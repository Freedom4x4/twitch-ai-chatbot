import os
import openai
import asyncio
import random
import time
import threading
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import read
from queue import Queue
from google.cloud import texttospeech
from twitchio.ext import commands
from obswebsocket import obsws, requests
from nextcord.ext import commands as discord_commands
from nextcord import FFmpegPCMAudio, Intents

# Load credentials from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
TWITCH_OAUTH_TOKEN = os.getenv("TWITCH_OAUTH_TOKEN")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OBS_HOST = os.getenv("OBS_HOST", "localhost")
OBS_PORT = int(os.getenv("OBS_PORT", "4455"))
OBS_PASSWORD = os.getenv("OBS_PASSWORD")

# Global conversation history
chat_history = [
    {
        "role": "system",
        "content": (
            "You are a conversational assistant. Your job is to maintain an engaging conversation. "
            "You should interact naturally and keep the flow of the conversation enjoyable. "
            "Avoid being overly focused on past contexts and aim for a conversational, human-like flow."
        )
    }
]

# Global variables
is_audio_playing = threading.Event()
playback_lock = threading.Lock()
audio_queue = Queue()
discord_voice_client = None

def save_tts_to_file(text, filename="output.wav"):
    """Convert text to speech and save as WAV file."""
    try:
        clean_text = text.replace('"', '').replace("'", "").replace("&", "and")
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=clean_text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Journey-F",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        with open(filename, "wb") as out:
            out.write(response.audio_content)
        print(f"Audio content written to {filename}")
    except Exception as e:
        print(f"Error using Google TTS: {e}")

def play_audio_through_virtual_cable(filename="output.wav"):
    """Play audio through a virtual audio cable."""
    global is_audio_playing
    with playback_lock:
        try:
            print(f"Attempting to play audio: {filename}")
            rate, data = read(filename)
            if data.dtype != np.int16:
                data = (data * np.iinfo(np.int16).max).astype(np.int16)
            virtual_device = None
            for idx, device in enumerate(sd.query_devices()):
                if "CABLE Input (VB-Audio Virtual Cable)" in device['name']:
                    virtual_device = idx
                    break
            if virtual_device is None:
                raise ValueError("Virtual cable device not found.")

            is_audio_playing.set()
            sd.play(data, samplerate=rate, device=virtual_device)
            sd.wait()
        except Exception as e:
            print(f"Error playing audio: {e}")
        finally:
            is_audio_playing.clear()

def queue_audio(filename="output.wav"):
    """Queue an audio file to be played."""
    global audio_queue
    audio_queue.put(filename)
    if not is_audio_playing.is_set():
        play_audio_from_queue()

def play_audio_from_queue():
    """Play all audio files in the queue sequentially."""
    global audio_queue, is_audio_playing
    if not audio_queue.empty():
        filename = audio_queue.get()
        try:
            play_audio_through_virtual_cable(filename)
        except Exception as e:
            print(f"Error playing queued audio: {e}")
        finally:
            is_audio_playing.clear()
            if not audio_queue.empty():
                play_audio_from_queue()

def generate_response(user_input, username):
    """Generate a response using OpenAI's API and produce TTS."""
    global chat_history
    try:
        chat_history.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history
        )
        response_text = response['choices'][0]['message']['content'].strip()
        chat_history.append({"role": "assistant", "content": response_text})
        filename = "output.wav"
        save_tts_to_file(response_text, filename)
        queue_audio(filename)
        return response_text
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm sorry, I couldn't generate a response."

async def idle_chat(bot):
    """Send idle chat messages when the bot is not actively chatting."""
    while True:
        print("Idle chat loop running...")
        if not bot.chat_active:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an AI assistant. Silently pick a random topic and generate an interesting fact about it. No facts about honey."}
                    ]
                )
                random_fact = response['choices'][0]['message']['content'].strip()
                await bot.connected_channels[0].send(random_fact)
                print(f"Idle chat fact sent: {random_fact}")
                save_tts_to_file(random_fact)
                queue_audio("output.wav")
            except Exception as e:
                print(f"Error generating or sending fact: {e}")
            await asyncio.sleep(150)
        else:
            await asyncio.sleep(150)

class Bot(commands.Bot):
    """Twitch Bot Implementation."""
    def __init__(self):
        super().__init__(
            token=TWITCH_OAUTH_TOKEN,
            prefix="!",
            initial_channels=["freedom_4x4"]  # replace if needed or make configurable
        )
        self.chat_active = False
        self.obs_host = OBS_HOST
        self.obs_port = OBS_PORT
        self.obs_password = OBS_PASSWORD
        self.ws = None

    async def event_ready(self):
        print(f"Logged in as | {self.nick}")
        try:
            self.ws = obsws(self.obs_host, self.obs_port, self.obs_password)
            self.ws.connect()
            print("Connected to OBS!")
        except Exception as e:
            print(f"Failed to connect to OBS: {e}")
        asyncio.create_task(idle_chat(self))

    async def event_message(self, message):
        global discord_voice_client
        if not message.author or not message.content:
            return
        print(f"Message received: {message.content} from {message.author.name}")
        self.chat_active = True
        if message.author.name.lower() == self.nick.lower():
            return
        try:
            response = generate_response(message.content, message.author.name)
            await message.channel.send(response)
            
            # If we have a Discord voice client, play the generated audio there as well
            if discord_voice_client and discord_voice_client.is_connected():
                if discord_voice_client.is_playing():
                    discord_voice_client.stop()
                discord_voice_client.play(FFmpegPCMAudio("output.wav"))
        except Exception as e:
            print(f"Error handling message: {e}")
        await asyncio.sleep(300)
        self.chat_active = False

    async def event_usernotice_subscription(self, metadata):
        user = metadata['user']['display_name']
        await self.connected_channels[0].send(f"🎉 Thanks for subscribing, {user}! You're awesome! 🎉")

    async def event_usernotice_raid(self, metadata):
        raider = metadata['user']['display_name']
        viewers = metadata['msg-param-viewerCount']
        await self.connected_channels[0].send(
            f"🛑 Raid alert! {raider} brought {viewers} amazing people! "
            f"Check out their channel at https://www.twitch.tv/{raider} and give them some love! 🛑"
        )

    async def event_usernotice_gifted_subscription(self, metadata):
        gifter = metadata['user']['display_name']
        recipient = metadata['msg-param-recipient-display-name']
        await self.connected_channels[0].send(
            f"🎁 {gifter} gifted a subscription to {recipient}! Spread the love! 🎁"
        )

    def switch_to_scene(self, scene_name):
        try:
            self.ws.call(requests.SetCurrentProgramScene(scene_name))
        except Exception as e:
            print(f"Failed to switch scene: {e}")

class DiscordBot(discord_commands.Bot):
    def __init__(self):
        intents = Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self):
        print(f"Discord bot connected as {self.user}")

@discord_commands.command(name="join")
async def join(ctx):
    global discord_voice_client
    try:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                vc = await channel.connect()
                discord_voice_client = vc
                await ctx.send(f"Joined {channel.name}. I will relay audio from Twitch responses here.")
            else:
                await ctx.send("I'm already connected to a voice channel!")
        else:
            await ctx.send("You need to be in a voice channel to use this command.")
    except Exception as e:
        print(f"Error in join command: {e}")
        await ctx.send("An error occurred while trying to join the voice channel.")

@discord_commands.command(name="leave")
async def leave(ctx):
    global discord_voice_client
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        discord_voice_client = None
        await ctx.send("Disconnected from the voice channel.")
    else:
        await ctx.send("I'm not in a voice channel!")

bot = Bot()
discord_bot = DiscordBot()
discord_bot.add_command(join)
discord_bot.add_command(leave)

def run_bots():
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start())
    loop.create_task(discord_bot.start(DISCORD_BOT_TOKEN))
    loop.run_forever()

if __name__ == "__main__":
    run_bots()
