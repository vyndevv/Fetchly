<div align="center">
  <h1>🎵 Fetchly</h1>
  <p><b>A modern, fast & simple Discord bot to download YouTube audio and videos directly into your channels.</b></p>
  
  <p>
    <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
    <img src="https://img.shields.io/badge/Discord.py-Bot-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord.py">
    <img src="https://img.shields.io/badge/FFmpeg-Required-007808?style=for-the-badge&logo=ffmpeg&logoColor=white" alt="FFmpeg">
  </p>
</div>

---

### ⚡ • Key Features

* **MP3 Format (`/mp3`)** — Extracts audio from YouTube videos with high quality (192 kbps).
* **MP4 Format (`/mp4`)** — Downloads full videos by automatically merging the best video and audio streams.
* **Bypass File Size Limits (Gofile.io)** — If a file exceeds Discord's file size limit (~25 MB), Fetchly automatically uploads it to Gofile and provides a direct download link.
* **Robust Error Handling** — Native management for invalid links, age-restricted, or private videos to prevent crashes.

---

### 🛠️ • Tech Stack & Requirements

<div align="center">

| Category | Requirements & Tools |
| :---: | :--- |
| **Language** | <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"> *(3.11 or higher)* |
| **Audio/Video Engine** | <img src="https://img.shields.io/badge/FFmpeg-007808?style=flat-square&logo=ffmpeg&logoColor=white" alt="FFmpeg"> *(Required for audio conversion & video merging)* |
| **Storage Fallback** | <img src="https://img.shields.io/badge/Gofile.io-4183C4?style=flat-square&logo=cloud&logoColor=white" alt="Gofile"> *(For files > 25MB)* |

</div>

---

### 🔑 • Required Permissions (Discord Developer Portal)

When generating your bot invite link under **OAuth2**, ensure you enable:

* **Scopes:** `bot`, `applications.commands`
* **Bot Permissions:**
  * `Send Messages`
  * `Attach Files`
  * `Read Message History`

---

### 🚀 • Installation & Setup

#### 1. Clone the Repository
Clone or download this repository to your local machine:
```bash
git clone https://github.com/vyndevv/Fetchly.git
cd fetchly
```

#### 2. Install dependencies
Install all required packages `pip` : 
```bash
pip install -r requirements.txt
```

#### 3. Configure your token
Open `bot.py` and replace the placeholder with your actual Discord Bot Token : 
```python
TOKEN="your_token"
```

#### 4. Start the bot
Run python command directly in your Fetchly folder :
```python
python bot.py
```
