# ☀️ Aurinkoone
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)
[![Version](https://img.shields.io/badge/version-1.0.0-orange)](https://github.com/mimirthful/Aurinkoone/releases)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)](README.md)
![Last Commit](https://img.shields.io/github/last-commit/mimirthful/Aurinkoone)
![Issues](https://img.shields.io/github/issues/mimirthful/Aurinkoone)

Aurinkoone is a Python-based desktop app for Tampere locals, which shows weather and user's selected bus stops.


## ✨ Highlights
- Weather panel for selected city district.
- Shows bus stops chosen by the user.
- All the important information you need before you exit from your front door in one place!
- Uses wxPython native widgets, so it looks like it belongs on every system and system theme that works with wxPython


## ℹ️ Overview
Aurinkoone is a simple weather and bus stop display for Tampere city area. 
I made Aurinkoone to remove the frustration of the hassle I had every time I was going somewhere. I was stuck on my phone checking the weather and bus timetables, going from app to app, wishing that there was a place I could check all of that in a couple of glances. Aurinkoone compiles all of that information needed in one app. It should work great with Raspberry Pi + touchscreen combo, so a tinkerer could create a permanent info screen on their hallway to show that information.


## 🌞 Usage
The app downloaded from Releases can be opened from the executable. <br> If building from the source code, after build, usage is the same as for pre-built versions. <br> <br>
**Important notice!** <br> To use the bus stop features, you do need a free API key from [Digitransit](https://portal-api.digitransit.fi/). A guide how to create one [can be found here](https://digitransit.fi/en/developers/api-registration/). Only the "Acquiring API keys" part of the guide is relevant for this situation. This key is inserted once in the settings, after which the bus stop features become available. 


## ⚙️ Installation

### Releases
Windows and Linux versions can be found from [Releases](https://github.com/mimirthful/Aurinkoone/releases/tag/Aurinkoone).
They are pre-built, and only need to be extracted from the .zip/tar to work. 

### Building from the source code
This is included as an option in case the pre-built versions won't work on your system for some reason, or your system is not included in the Releases.
You need Python to be installed for this on your device.

1. Download the source code of any of the latest releases.
2. Move to the root folder of the source code.
3. I recommend creating a Python virtual environment for the release. [Quick instructions here.](https://www.w3schools.com/python/python_virtualenv.asp) This way, the dependencies needed won't install system-wide unnecessarily.
4. Check "dependencies.txt" and pip install all the packages mentioned in it.
```bash
pip install "dependency-package-name"
```
5. Run the Pyinstaller build command. Everything needed for this is in the Aurinkoone.spec file, so you shouldn't need to do anything else than run this command.
```bash
pyinstaller Aurinkoone.spec
```
6. The finished build "Aurinkoone"-folder should be available on the "release-folder-name"/dist. It should contain an executable and "_internal"-folder. You can move the Aurinkoone-folder to a place you wish to keep the app. The source code is not needed for using the app, and can be safely deleted.

## 🗨️🐛Feedback and Bug reports
If you have feedback or encounter bugs, you're free to open an issue in the Issues tab/section

## Screenshots
### Aurinkoone on Linux GNOME desktop environment
<img width="1177" height="797" alt="Screenshot From 2026-08-18 13-18-10" src="https://github.com/user-attachments/assets/03993c96-0671-45bf-b8dc-afcd23711ff8" />
<img width="1179" height="802" alt="Screenshot From 2026-08-18 13-19-28" src="https://github.com/user-attachments/assets/8034d832-8463-467d-a1a9-42befb4eb68b" />

### Aurinkoone on Windows
<img width="1610" height="987" alt="Näyttökuva 2026-08-18 150851" src="https://github.com/user-attachments/assets/05278607-ba2f-4562-ab9f-31bb89eb56ba" />
<img width="1602" height="982" alt="Näyttökuva 2026-08-18 151201" src="https://github.com/user-attachments/assets/08672cb6-611b-4f9d-9a73-a9ff16e3922b" />
<br>
Made with ❤️ in Tampere
