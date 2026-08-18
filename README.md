# ☀️ Aurinkoone

Python based desktop app for Tampere locals, which shows weather and user selected bus stops.


## ✨ Highlights
- Weather panel for selected city district.
- Bus stops chosen by the user.
- All important information you need before you exit your front door!
- Uses wxpython native widgets, so it looks like it belongs on every system and system theme that works with wxpython

<img width="446" height="311" alt="image of Aurinkoone weather screen" src="https://github.com/user-attachments/assets/a17b0027-2db8-497b-ba4a-71ccfc13f882" />
<img width="446" height="311" alt="image of Aurinkoone bus stop screen" src="https://github.com/user-attachments/assets/b10db2d7-c68e-4a25-8fbb-48bea6dc5f1d" />

## ℹ️ Overview

Aurinkoone is a simple weather and bus stop display for Tampere city area. 
I made Aurinkoone to remove the frustration of the hassle I had every time I was going somewhere. I was stuck on my phone checking the weather and bus timetables, going from app to app, wishing, that there was a place I could check all of that in couple of glances. Aurinkoone compiles all of that information needed on one app. It should work great with rasperry pi + touchscreen combo,so a tinkerer could create a permanent info screen on their hallway to show that information.


## 🌞 Usage
Pre-build versions can be opened from the executable. After building from the source code, usage is same with pre-build ones.  However, to use the bus stop features, you do need a free API key from [Digitransit](https://portal-api.digitransit.fi/). A guide how to create one [can be found here](https://digitransit.fi/en/developers/api-registration/). Only the "Acquiring API keys" part is relevant for this situation. This key is inserted once in the settings, which after the bus stop features become available. 


## ⚙️ Installation

### Pre-build versions

### Building from the source code
This is included as an option in-case the pre-build versions won't work on your system. 
You need Python to be installed for this on your device.


1. Create a local copy of this repo on your device
2. Move to the root folder of the copied repo
3. Create a venv for the repo. This way, the dependencies needed won't install system-wide
4. Check "dependencies.txt" and pip install all the packages mentioned
```bash
pip install "dependency-package-name"
```
5. Run pyinstaller building command. Everything needed for this is on the Aurinkoone.spec file.
```bash
pyinstaller Aurinkoone.spec
```
6. The finished build "Aurinkoone"-folder should be available on the Aurinkoone/dist. It should contain an executable and _internal-folder. You can move the Aurinkoone-folder on a place you wish to keep the app. The rest of the repo is not needed anymore for the usage, and can be safely deleted.



## 🗨️🐛Feedback and Bug reports
If you have feedback or encounter bugs, you're free to open an issue on the issues.
