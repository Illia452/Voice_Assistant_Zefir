
INSTRUCTION = """

<role>
Ти — Зефір, швидкий та лаконічний голосовий помічник. Твоя мета — миттєво обробляти команди користувача.
</role>

<constraints>
1. ВІДПОВІДЬ: Тільки в форматі JSON. Жодного зайвого тексту поза межами JSON.
2. СТИЛЬ: Голосова відповідь (voice_response) має бути максимально короткою (до 10-15 слів), без спецсимволів (*, #), чіткою для озвучування.
3. ШВИДКІСТЬ: Не витрачай час на ввічливі вступи, якщо вони не є частиною відповіді.
</constraints>

<commands_list>
Нижче перелік команд, які ти можеш виконувати. Якщо наміру користувача немає в списку, command_found = false.
- "light_on" (увімкнути світло)
- "screen" (скріншот екрану)
- "light_off" (вимкнути світло)
- "music_play" (грати музику)
- "set_timer" (встановити таймер, параметр: час у секундах)
- "get_weather" (погода)
- "stop" (зупинити все)
</commands_list>

<output_format>
Кожна твоя відповідь ПОВИННА мати таку структуру:
{
  "command_found": boolean,
  "command_id": "string або null",
  "parameter": "string або null",
  "voice_response": "Текст, який буде озвучено користувачу"
}
</output_format>

<examples>
User: "Зефір, увімкни світло будь ласка"
Response: {"command_found": true, "command_id": "light_on", "parameter": null, "voice_response": "Вмикаю світло."}

User: "Яка сьогодні погода?"
Response: {"command_found": true, "command_id": "get_weather", "parameter": null, "voice_response": "Зараз перевірю погоду для вас."}

User: "Привіт, як справи?"
Response: {"command_found": false, "command_id": null, "parameter": null, "voice_response": "Привіт! У мене все чудово. Чим можу допомогти?"}
</examples>


USER COMMAND = "Відкрий но браузер"


"""



from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
load_dotenv("../secret_data/gemini_api_key.env")
import time

client = genai.Client(api_key=os.getenv("API_KEY"))
chat = client.chats.create(model="gemini-2.5-flash")



# start = time.time()

# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents=INSTRUCTION,
#     config=types.GenerateContentConfig(
#     thinking_config=types.ThinkingConfig(thinking_budget=0)
#         # Turn off thinking:
#         # thinking_config=types.ThinkingConfig(thinking_budget=0)
#         # Turn on dynamic thinking:
#         # thinking_config=types.ThinkingConfig(thinking_budget=-1)
#     ),
# )

data = """
[{'Name': 'Inkscape'}, {'Name': 'Inkview'}, {'Name': 'Firefox'}, {'Name': 'ਢ⭨ ॣ Firefox'}, {'Name': 'License'}, {'Name': 'Dev-C++'}, {'Name': 'Nsight Redistributable'
}, {'Name': 'NVIDIA GeForce NOW'}, {'Name': 'ॢ?ઠ ⠭ '}, {'Name': 'Python 3.11 Manuals (64-bit)'}, {'Name': 'Python 3.11 (64-bit)'}, {'Name': 'Viber'}, {'Name': 'TLaunc
her'}, {'Name': 'uTorrent Web'}, {'Name': 'Google Chrome'}, {'Name': 'VirusTotal'}, {'Name': 'GitHub'}, {'Name': 'Minestar Launcher'}, {'Name': 'NVIDIA'}, {'Name': 'Dolphin Anty'}, {'Name': 'Discord'}, {'Name': 'GitHub Desktop'}, {'Name': 'Adobe Illustrator 2025'}, {'Name': 'Adobe Photoshop 2025'}, {'Name': 'Adobe After Effects 2025'}, {'Name': 'Adobe Premiere Pro 2025'}, {'Name': 'Anki'}, {'Name': ' 몠 Grand Theft Auto V'}, {'Name': ' Grand Theft Auto V'}, {'Name': 'TreeSize Free ?'}, {'Name': 'DeepL'}, {'Name': 'CrystalMark 3D25'}, {'Name': 'TreeSizeFree.exe'}, {'Name': 'Steam Support Center'}, {'Name': 'Git FAQs (Frequently Asked Questions)'}, {'Name': 
'Node.js website'}, {'Name': 'Node.js documentation'}, {'Name': 'Grass'}, {'Name': 'Install Additional Tools for Node.js'}, {'Name': 'Safer Web'}, {'Name': 'Git Bash'}, {'Name': 'TreeSize Free'}, {'Name': 'Uninstall Zoom Workplace'}, {'Name': 'Python 3.11 Module Docs (64-bit)'}, {'Name': 'Git CMD'}, {'Name': "㢠 '\u0bac"}, {'Name': 'Node.js command prompt'}, {'Name': 'Uninstall Node.js'}, {'Name': 'Uninstall NVIDIA Nsight Compute 2022.3.0'}, {'Name': 'ᯥ '}, {'Name': 'Performance Monitor'}, {'Name': 'Viber(Compatibility Mode)'}, {'Name': 'Event Viewer'}, {'Name': 'Task Scheduler'}, {'Name': 'Resource Monitor'}, {'Name': 'Uninstall NVIDIA Nsight Systems 2022.4.2'}, {'Name': 'Windows Speech Recognition'}, {'Name': 'IDLE (Python 3.11 64-bit)'}, {'Name': 'Internet Explorer'}, {'Name': 'PowerToys (Preview)'}, {'Name': 'OneDrive'}, {'Name': 'Visual Studio Code'}, {'Name': 'Windows Media Player'}, {'Name': '? \u0ba1稩 ?'}, {'Name': 'Microsoft Edge'}, {'Name': '㧥 Opera GX'}, {'Name': '㧥 Opera'}, {'Name': 'Run Prop, Run!'}, {'Name': 'STALCRAFT X'}, {'Name': 'One-armed cook'}, {'Name': 'Euro Truck Simulator 2'}, {'Name': "Bronzebeard's Tavern"}, {'Name': 'One-armed robber'}, {'Name': 'Idle Hero TD'}, {'Name': 'Trainfort Playtest'}, {'Name': 'Backseat Drivers Demo'}, {'Name': 'Human Fall Flat'}, {'Name': 'Satisfactory'}, {'Name': 'Telegram'}, {'Name': 'LibreOffice Base'}, {'Name': 'LibreOffice Calc'}, {'Name': 'LibreOffice Draw'}, {'Name': 'LibreOffice Impress'}, {'Name': 'LibreOffice Math'}, {'Name': 'LibreOffice (筨 ०)'}, {'Name': 'LibreOffice'}, {'Name': 'LibreOffice Writer'}, {'Name': 'Zoom Workplace'}, {'Name': ' ᨬ?'}, {'Name': '饭 ᪠'}, 
{'Name': 'Component Services'}, {'Name': '⨬?㢠 ᪨  ⨬?㢠  \u0ba1'}, {'Name': 'iSCSI Initiator'}, {'Name': "?⨪ '? Windows"}, {'Name': 'System Configuration'}, {'Name': '??  ⥬'}, {'Name': 'Paint'}, {'Name': ''}, {'Name': 'ODBC Data Sources (64-bit)'}, {'Name': '? 㢠 ? 㢠'}, {'Name': '? '}, {'Name': ' ?'}, {'Name': 'Services'}, {'Name': '? 宯 ࠣ?'}, {'Name': 'Windows Defender Firewall with Advanced Security'}, {'Name': '  ᪠㢠  Windows'}, {'Name': 'Windows PowerShell ISE'}, {'Name': 'Math Input Panel
'}, {'Name': 'CrystalDiskInfo'}, {'Name': 'Git GUI'}, {'Name': 'Git Release Notes'}, {'Name': 'Google Drive'}, {'Name': 'Google Play ? ()'}, {'Name': 'Intel(R) Rapid 
Storage Technology'}, {'Name': 'Node.js'}, {'Name': 'Notepad++'}, {'Name': 'Nsight Compute'}, {'Name': 'Nsight Systems 2022.4.2'}, {'Name': 'GeForce Experience'}, {'Name': 'Browse NVIDIA Tools Extension'}, {'Name': 'Visual Profiler'}, {'Name': 'ॢ?ઠ ⠭ '}, {'Name': 'Proton VPN'}, {'Name': 'Waves MaxxAudioPro'}, {'Name': 'WordPad'}, 
{'Name': 'Console RAR manual'}, {'Name': 'What is new in the latest version'}, {'Name': 'WinRAR help'}, {'Name': 'WinRAR'}, {'Name': ' Age of Civilizations II'}, {'Name': 'Uninstall Age of Civilizations II'}, {'Name': 'AIDA64'}, {'Name': 'Uninstall AIDA64'}, {'Name': 'Battle.net'}, {'Name': 'Epic Games Launcher'}, {'Name': 'Nsight Monitor'}, {'Name': 'Qt Designer'}, {'Name': 'Steam'}, {'Name': 'Ubisoft Connect'}, {'Name': 'Uninstall'}, {'Name': 'Uplay'}, {'Name': 'ODBC Data Sources (32-bit)'}, {'Name': 'Windows PowerShell ISE (x86)'}, {'Name': 'Registry Editor'}, {'Name': '㢠'}, {'Name': '䮭'}, {'Name': 'Mixed Reality Portal'}, {'Name': '宯  ?'}, {'Name': 
'Cortana'}, {'Name': '쩮 ᮫? Xbox'}, {'Name': '?'}, {'Name': 'Minecraft'}, {'Name': '  Windows'}, {'Name': '?'}, {'Name': ' 㢠 ? IntelR'}, {'Name': 'Paint 3D'}, {'Name
': 'Words of Wonders : Crossword'}, {'Name': ''}, {'Name': ''}, {'Name': 'TranslucentTB'}, {'Name': 'Skype'}, {'Name': '㦡 Windows  १ࢭ ?\ue8a0'}, {'Name': 'Microsoft 
Whiteboard'}, {'Name': ''}, {'Name': '3D-?'}, {'Name': 'OneNote for Windows 10'}, {'Name': 'Geometry DashCraft Editor'}, {'Name': '?燐 ? ᬠ䮭'}, {'Name': 'Weather'}, {'Name': 'NVIDIA Control Panel'}, {'Name': 'Game Bar'}, {'Name': 'Roblox'}, {'Name': 'Lively Wallpaper'}, {'Name': ''}, {'Name': ''}, {'Name': 'Dell SupportAssist'}, {'Name': '?筨'}, {'Name': 'Outlook'}, {'Name': '⮣?'}, {'Name': ' ??'}, {'Name': 'Inkscape'}, {'Name': 'Solitaire & Casual Games'}, {'Name': 'Torrent Manager'}, {'Name': ''}, {'Name': 'Xbox'}, {'Name': '?ணࠢ'}, {'Name': '?쬨  ⥫ணࠬ'}, {'Name': 'Roblox'}, {'Name': 'Microsoft 365 Copilot'}, {'Name': 'Microsoft Store'}, {'Name': 'Copilot'
}]
"""


response = chat.send_message("Наскільки швидко ти можеш обробляти масиви даних?")
print(response.text)

response = chat.send_message(f"Скажи чи є тут додаток WORD у моєму списку \n  {data}")
print(response.text)

response = chat.send_message(f"Отаке завдання для тебе складне?")
print(response.text)

for message in chat.get_history():
    print(f'role - {message.role}',end=": ")
    print(message.parts[0].text)

# print(response.text)
# print(start-time.time())





