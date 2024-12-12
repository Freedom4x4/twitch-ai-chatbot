# AI VTuber Project - Twitch and Discord Integrated Chatbot

**Description:**  
This project implements an AI-driven VTuber personality that can interact in Twitch chat, generate audio responses in real-time using OpenAI and Google TTS, and relay that same audio into a Discord voice channel. The bot also integrates with OBS via WebSocket for scene switching. By leveraging environment variables, no sensitive credentials are stored in the code, ensuring a secure and maintainable setup.

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
   - Obtain a bot OAuth token from [Twitch Token Generator](https://twitchapps.com/tmi/) or follow the Twitch developer docs.
   - Format should be: `oauth:xxxxxxxxxxxxxxxxxx`

5. **Discord Bot Token**  
   - Create a Discord bot at the [Discord Developer Portal](https://discord.com/developers/applications).
   - Copy the bot token from the “Bot” section.

6. **Google Cloud TTS Credentials**  
   - Enable the Google Text-to-Speech API in Google Cloud.
   - Ensure `GOOGLE_APPLICATION_CREDENTIALS` points to your service account key JSON file.

7. **OBS WebSocket**  
   - For older OBS versions, install the [OBS WebSocket Plugin](https://github.com/obsproject/obs-websocket).
   - For OBS 28+ or later, OBS WebSocket is built-in.
   - Enable OBS WebSocket and note the host, port, and password.

8. **Virtual Audio Cable or Equivalent Audio Routing**  
   - By default, the bot’s audio output is directed through "CABLE Input (VB-Audio Virtual Cable)".  
   - If you don’t have VB-Audio Virtual Cable installed, you can:
     - Install it from [VB-Audio](https://vb-audio.com/Cable/) and set your streaming software to capture from "CABLE Input".  
     - Modify the code in `play_audio_through_virtual_cable` to use a different device.  
   - Ensure your streaming software (e.g., OBS) captures the virtual cable audio so viewers can hear the responses.

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Freedom4x4/twitch-ai-chatbot.git
   cd twitch-ai-chatbot
   ```

2. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```
   
   `requirements.txt` should include:
   - openai  
   - google-cloud-texttospeech  
   - twitchio  
   - nextcord  
   - obs-websocket-py  
   - sounddevice  
   - scipy  
   - numpy

### Setting Environment Variables

**Windows (Command Prompt):**
```cmd
setx OPENAI_API_KEY "YOUR_OPENAI_API_KEY"
setx TWITCH_OAUTH_TOKEN "oauth:YOUR_TWITCH_OAUTH_TOKEN"
setx DISCORD_BOT_TOKEN "YOUR_DISCORD_BOT_TOKEN"
setx OBS_HOST "localhost"
setx OBS_PORT "4455"
setx OBS_PASSWORD "YOUR_OBS_PASSWORD"
setx GOOGLE_APPLICATION_CREDENTIALS "path\to\your\service_account.json"
```
*(Close and reopen your terminal after running these commands.)*

**Linux/macOS:**
```bash
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
export TWITCH_OAUTH_TOKEN="oauth:YOUR_TWITCH_OAUTH_TOKEN"
export DISCORD_BOT_TOKEN="YOUR_DISCORD_BOT_TOKEN"
export OBS_HOST="localhost"
export OBS_PORT="4455"
export OBS_PASSWORD="YOUR_OBS_PASSWORD"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service_account.json"
```
*(Add these lines to `~/.bashrc` or `~/.zshrc` for persistence.)*

### Running the Bot

```bash
python chatbot.py
```

If everything is set correctly:

- The Twitch bot will connect to the specified channel.
- The Discord bot will start and be ready for `!join` and `!leave` commands.
- Twitch chat messages will be answered by the AI and converted to speech.
- The audio is routed through the virtual cable. In your streaming software, set your audio source to this virtual cable so your viewers can hear the responses.
- Use `!join` in Discord (while you’re in a voice channel) to have the bot also relay audio into that voice channel.

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

- **No Audio or Wrong Audio Device:**  
  If audio is not playing or not captured by your stream, ensure the virtual audio cable is installed and selected. If you prefer a different device, edit the `play_audio_through_virtual_cable` function to select a different audio device index.

### Security Note

All keys are sourced from environment variables. **Do not commit** your `.env` file or any credentials to your repository. Keep your keys private and out of the codebase.

### License

**MIT License**  
```
© [2024] Freedom.4x4

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:  

The above copyright notice and this permission notice shall  
be included in all copies or substantial portions of the Software.  

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,  
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES  
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,  
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER  
DEALINGS IN THE SOFTWARE.
```
