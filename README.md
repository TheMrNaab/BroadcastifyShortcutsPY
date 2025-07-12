# BroadcastifyShortcutsPY

This shortcut installs the following files into Pythonista:

- `broadcastify.py`
- `channels.json`

### Setup Instructions

1. **Install Pythonista**  
   Download Pythonista 3 from the App Store:  
   [Get Pythonista](https://apps.apple.com/us/app/pythonista-3/id1085978097)

2. **Open Pythonista**  
   Launch the app on your device.

3. **Create a New Script**
   - Tap the Menu button
   - Tap **This iPhone**
   - Tap the **+** button to create the install file
   - Choose **Empty Script** 
   - Name it: `install.py`
   - Tap **Create**

5. **Paste This Code Into the File**  
   Copy the code below and paste it into `install.py`:

   ```python
   import urllib.request
   exec(urllib.request.urlopen("https://raw.githubusercontent.com/TheMrNaab/BroadcastifyShortcutsPY/main/install.py").read())
   ```

6. **Run the Installer**  
   Tap the **Play** ▶️ button to run the script.  
   This will download and set up the Broadcastify files into a folder called `BroadcastifyShortcutsPY`.

7. **Open and Use the App**
   - Tap the **menu** button
   - Tap **This iPhone**
   - Open the new folder: `BroadcastifyShortcutsPY`
   - Tap on `broadcastify.py`  
   - Press **Play** ▶️ to start using it

9. *(Optional)* **Add to Apple Shortcuts**  
   - Open the **Shortcuts** app  
   - Tap **+** to create a new shortcut  
   - Search for **Run Pythonista Script**  
   - Choose `broadcastify.py` from the folder  
   - You can add this shortcut to your Home Screen or ask **Siri** to run it
