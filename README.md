
# AI VTuber Project - Twitch and Discord Integrated Chatbot

**Description:**  
This project implements an AI-driven VTuber personality that can interact in Twitch chat, generate audio responses in real-time using OpenAI and Google TTS, and relay the same audio into a Discord voice channel. The bot also integrates with OBS via WebSocket for scene switching. By leveraging environment variables, no sensitive credentials are stored in the code, ensuring a secure and maintainable setup.

---

## Step-by-Step Setup Guide

### Prerequisites

1. **Python 3.9+**  
   Ensure you have Python 3.9 or higher installed.  
   [Download Python](https://www.python.org/downloads/)

2. **Optional: Virtual Environment**  
   It’s recommended to use a virtual environment for managing dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   .\venv\Scripts\activate    # On Windows
   ```

3. **OpenAI API Key**  
   Sign up or log in at [OpenAI](https://platform.openai.com/) to get your API key.

4. **Twitch OAuth Token**  
   - Obtain a bot OAuth token from [Twitch Token Generator](https://twitchapps.com/tmi/) or follow Twitch developer docs.
   - Format should be: `oauth:xxxxxxxxxxxxxxxxxx`

5. **Discord Bot Token**  
   - Create a Discord bot at the [Discord Developer Portal](https://discord.com/developers/applications).
   - Copy the bot token from the “Bot” section.

6. **Google Cloud TTS Credentials**  
   - Enable Google Text-to-Speech API in Google Cloud.
   - Ensure `GOOGLE_APPLICATION_CREDENTIALS` points to your service account key JSON file.

7. **OBS WebSocket**  
   - For older OBS versions, install the [OBS WebSocket Plugin](https://github.com/obsproject/obs-websocket).
   - For OBS 28+ or later, OBS WebSocket is built-in.
   - Enable OBS WebSocket and note the host, port, and password.

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/YourUsername/YourRepoName.git
   cd YourRepoName
   ```

2. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```
   
   Ensure `requirements.txt` includes:
   - openai  
   - google-cloud-texttospeech  
   - twitchio  
   - nextcord  
   - obs-websocket-py  
   - sounddevice  
   - scipy  
   - numpy

### Setting Environment Variables

Set the following environment variables with your actual keys. After setting them, open a new terminal session so they are recognized.

**Windows (Command Prompt):**
```cmd
setx OPENAI_API_KEY "YOUR_OPENAI_API_KEY"
setx TWITCH_OAUTH_TOKEN "oauth:YOUR_TWITCH_OAUTH_TOKEN"
setx DISCORD_BOT_TOKEN "YOUR_DISCORD_BOT_TOKEN"
setx OBS_HOST "localhost"
setx OBS_PORT "4455"
setx OBS_PASSWORD "YOUR_OBS_PASSWORD"
```
*(Close and reopen your terminal after running these commands.)*

**Linux/macOS (temporary for the current session):**
```bash
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
export TWITCH_OAUTH_TOKEN="oauth:YOUR_TWITCH_OAUTH_TOKEN"
export DISCORD_BOT_TOKEN="YOUR_DISCORD_BOT_TOKEN"
export OBS_HOST="localhost"
export OBS_PORT="4455"
export OBS_PASSWORD="YOUR_OBS_PASSWORD"
```
*(Add these lines to `~/.bashrc` or `~/.zshrc` for persistence.)*

### Running the Bot

```bash
python chatbot.py
```

If everything is set correctly:

- The Twitch bot will connect to the specified channel.
- The Discord bot will start and be ready for `!join` and `!leave` commands.
- Twitch chat messages will be answered by the AI and converted to speech. Audio will play through a virtual cable and can also be relayed to Discord if you’ve issued the `!join` command there.

### Usage

- **Twitch:**  
  The bot responds automatically to chat messages in the configured channel.

- **Discord:**  
  Use `!join` in a text channel while you’re in a voice channel to have the bot join that voice channel and relay audio.  
  Use `!leave` to disconnect the bot from the voice channel.

### Troubleshooting

- **`NoneType object has no attribute 'replace'` Error:**  
  The Twitch OAuth token environment variable isn’t set properly. Check spelling and re-open your terminal after setting it.

- **Invalid Discord Token:**  
  Ensure you’re using the correct bot token and that the environment variable is set correctly.

- **TTS Issues:**  
  Check your Google Cloud credentials and ensure you have the TTS API enabled. Make sure `GOOGLE_APPLICATION_CREDENTIALS` is correctly set.

- **OBS Connection Problems:**  
  Verify OBS WebSocket settings, port, and password. Confirm that OBS is running and the WebSocket server is active.

### Security Note

All keys are sourced from environment variables. **Do not commit** your `.env` file or any credentials to your repository. Keep your keys private and out of the codebase.

### License

[Add your license here, e.g., MIT License]
```
