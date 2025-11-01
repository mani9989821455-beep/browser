Kali Browser - Installation and Usage Instructions

REQUIREMENTS:
- Python 3.8 or higher
- Windows/macOS/Linux

INSTALLATION ON WINDOWS:

1. Open Command Prompt (cmd.exe) or PowerShell
   - Press Windows + R, type cmd, and press Enter

2. Navigate to your browser project directory:
   cd "C:\Users\YourUsername\OneDrive\Documents\Projects\browser"

3. Install dependencies (choose one method):

   METHOD A - Using pip (recommended):
   python -m pip install --upgrade pip
   python -m pip install PyQt6==6.6.1 PyQt6-WebEngine==6.6.0

   METHOD B - If pip doesn't work, use python directly:
   python -m ensurepip --upgrade
   python -m pip install PyQt6==6.6.1 PyQt6-WebEngine==6.6.0

   METHOD C - Force reinstall if you have issues:
   python -m pip install --force-reinstall PyQt6==6.6.1 PyQt6-WebEngine==6.6.0

4. Run the browser:
   python kali_browser.py

INSTALLATION ON macOS:

1. Open Terminal
2. Navigate to your browser project:
   cd ~/path/to/your/browser

3. Install dependencies:
   python3 -m pip install PyQt6==6.6.1 PyQt6-WebEngine==6.6.0

4. Run the browser:
   python3 kali_browser.py

INSTALLATION ON LINUX:

1. Open Terminal
2. Install system dependencies:
   sudo apt-get install libgl1-mesa-glx libxkbcommon-x11-0

3. Navigate to your browser and install Python packages:
   cd ~/path/to/your/browser
   python3 -m pip install PyQt6==6.6.1 PyQt6-WebEngine==6.6.0

4. Run the browser:
   python3 kali_browser.py

TROUBLESHOOTING:

Problem: "DLL load failed while importing QtCore"
Solution:
   1. Uninstall existing PyQt6: python -m pip uninstall -y PyQt6 PyQt6-WebEngine
   2. Reinstall: python -m pip install PyQt6==6.6.1 PyQt6-WebEngine==6.6.0
   3. Or try: python -m pip install --only-binary :all: PyQt6 PyQt6-WebEngine

Problem: "module not found"
Solution:
   1. Make sure you're using Python 3.8+: python --version
   2. Upgrade pip: python -m pip install --upgrade pip
   3. Try installing from requirements.txt:
      python -m pip install -r requirements.txt

Problem: Screen appears blank
Solution:
   1. Check your graphics drivers are up to date
   2. Try running with: python -c "from PyQt6.QtWebEngineWidgets import QWebEngineView"
   3. This tests if WebEngine is working properly

FEATURES:
- Modern dark metallic theme (black, grey, ash, glass)
- Secure browsing with HTTPS enforcement
- URL validation and search integration
- Multiple tab support with smooth transitions
- Navigation controls (back, forward, reload, home)
- Real-time SSL/security indicator
- Lightning-fast QtWebEngine rendering
- Support for all video and image formats
- Tab management with open/close functionality
- Beautiful glass-morphism UI elements

KEYBOARD SHORTCUTS:
- Ctrl + T: New Tab
- Ctrl + W: Close Tab (or close window if only 1 tab)
- Ctrl + L: Focus address bar
- F5 or Ctrl + R: Reload
- Backspace: Back (when not in text field)
- Alt + Right Arrow: Forward

THEME DESCRIPTION:
The Kali Browser features a premium dark theme with:
- Deep black background (#0d0d0d)
- Metallic grey gradients (#252525 to #1a1a1a)
- Ash grey accents (#3a3a3a)
- Cyan blue highlights (#4a9eff) for interactive elements
- Glass-morphism effects with subtle transparency
- Smooth animations and transitions
- Professional color scheme for extended use

SECURITY:
- Automatic HTTPS upgrade warnings
- URL validation and sanitization
- Sandboxed web content
- Built-in web engine security protections

Enjoy your browsing experience!
