Below are updated instructions including how to install Git if you haven't already, and providing clear code blocks that can be copied and run in PowerShell. The instructions are split into logical sections so users can easily copy and paste the commands as needed.

---

# AI VTuber Project - Twitch and Discord Integrated Chatbot

**Description:**  
This project implements an AI-driven VTuber personality that can interact in Twitch chat, generate audio responses in real-time using OpenAI and Google TTS, and relay that same audio into a Discord voice channel. The bot also integrates with OBS via WebSocket for scene switching. By leveraging environment variables, no sensitive credentials are stored in the code, ensuring a secure and maintainable setup.

---

## Step-by-Step Setup Guide

### Prerequisites

1. **Git (if not installed)**  
   [Download Git](https://git-scm.com/downloads) and install it.  
   Once installed, you can verify by opening PowerShell and running:
   ```powershell
   git --version
   ```

2. **Python 3.9+**  
   Ensure you have Python 3.9 or higher installed.  
   [Download Python](https://www.python.org/downloads/) and install it.  
   Verify installation in PowerShell:
   ```powershell
   python --version
   ```

3. **Optional: Virtual Environment**  
   It’s recommended to use a virtual environment for managing dependencies:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
   *(Run these commands from within the project directory.)*

4. **OpenAI API Key**  
   Sign up or log in at [OpenAI](https://platform.openai.com/) to get your API key.

5. **Twitch OAuth Token**  
   - Obtain a bot OAuth token from [Twitch Token Generator] [https://twitchtokengenerator.com/] or from the Twitch Developer docs.
   - Ensure the bot has Chat:Read and Chat:Edit Permissions
   - Format should be: `oauth:xxxxxxxxxxxxxxxxxx`

6. **Discord Bot Token**  
   - Create a Discord bot at the [Discord Developer Portal](https://discord.com/developers/applications).
   - Copy the bot token from the "Bot" section.

7. **Google Cloud TTS Credentials**  
   - Enable the Google Text-to-Speech API in Google Cloud.
   - Ensure `GOOGLE_APPLICATION_CREDENTIALS` points to your service account key JSON file.

8. **OBS WebSocket**  
   - For older OBS versions, install the [OBS WebSocket Plugin](https://github.com/obsproject/obs-websocket).
   - For OBS 28+ or later, OBS WebSocket is built-in.
   - Enable OBS WebSocket and note the host, port, and password.

9. **Virtual Audio Cable**  
   - The bot’s audio output is directed to "CABLE Input (VB-Audio Virtual Cable)".  
   - If you don’t have VB-Audio Virtual Cable installed, get it from [VB-Audio](https://vb-audio.com/Cable/) or modify the code to use another device.

---

### Installation

Open PowerShell, then run the following:

1. **Clone the Repository** (If you don’t have Git, install it first as described above):
   ```powershell
   git clone https://github.com/Freedom4x4/twitch-ai-chatbot.git
   cd twitch-ai-chatbot
   ```

2. **Install Requirements**  
   Install the necessary Python packages:
   ```powershell
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

*(If you’re using a virtual environment, ensure it’s activated before installing.)*

---

### Setting Environment Variables

Set your environment variables in PowerShell. Replace the placeholder values with your actual keys and tokens:

```powershell
$env:OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
$env:TWITCH_OAUTH_TOKEN="oauth:YOUR_TWITCH_OAUTH_TOKEN"
$env:DISCORD_BOT_TOKEN="YOUR_DISCORD_BOT_TOKEN"
$env:OBS_HOST="localhost"
$env:OBS_PORT="4455"
$env:OBS_PASSWORD="YOUR_OBS_PASSWORD"
$env:GOOGLE_APPLICATION_CREDENTIALS="path\to\your\service_account.json"
```

*(These environment variables will only persist for the current PowerShell session. Add them to your profile script or set them permanently if desired.)*

---

### Running the Bot

From the project directory (where `chatbot.py` is located):

```powershell
python chatbot.py
```

If everything is set correctly:

- The Twitch bot will connect to the specified channel.
- The Discord bot will start and be ready for `!join` and `!leave` commands.
- Twitch chat messages will be answered by the AI and converted to speech.
- The audio is routed through the virtual cable. In your streaming software (e.g., OBS), set your audio source to this virtual cable so your viewers can hear the responses.
- Use `!join` in Discord (while you’re in a voice channel) to have the bot also relay audio into that voice channel.

---

### Usage

**Twitch:**  
The bot responds automatically to chat messages in the configured channel.

**Discord:**  
- Use `!join` in a text channel while you’re in a voice channel to have the bot join that voice channel and relay audio.  
- Use `!leave` to disconnect the bot from the voice channel.

---

### Troubleshooting

- **`NoneType object has no attribute 'replace'` Error:**  
  The Twitch OAuth token environment variable isn’t set properly. Double-check spelling and ensure you reopened PowerShell after setting it if you set them permanently.

- **Invalid Discord Token:**  
  Ensure the `DISCORD_BOT_TOKEN` is correct and that the environment variable is set.

- **TTS Issues:**  
  Check your Google Cloud credentials and ensure TTS API is enabled. Confirm `GOOGLE_APPLICATION_CREDENTIALS` is correctly set.

- **OBS Connection Problems:**  
  Verify OBS WebSocket settings, port, and password. Make sure OBS is running and the WebSocket server is active.

- **No Audio or Wrong Audio Device:**  
  If no audio is playing or your stream isn’t capturing the bot’s voice:
  - Ensure the virtual audio cable is installed and selected as the input source in your streaming software.
  - If you want to use another device, modify the `play_audio_through_virtual_cable` function in `chatbot.py` to choose a different device.

---

### Security Note

All keys are sourced from environment variables. **Do not commit** your `.env` file or any credentials to your repository. Keep your keys private and out of the codebase.

---

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
