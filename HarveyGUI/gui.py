# gui.py - Main application to run the UI
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt
from ui_mic import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Track microphone state (False = Off/Muted, True = On/Recording)
        self.mic_active = False
        self.process = None  # Track the subprocess running make_it_happen_it_works.py

        # Make the button checkable so it can toggle between On/Off states
        self.ui.toolButton.setCheckable(True)
        self.ui.toolButton.setChecked(False)  # Start in Off state

        # Connect the microphone button to a function
        self.ui.toolButton.clicked.connect(self.on_mic_clicked)

        # Set window title
        self.setWindowTitle("Harvey - Personal Digital Assistant")
        
    def on_mic_clicked(self):
        """Handle microphone button click - toggle between states"""
        print(f"Microphone button clicked! Current state: {self.mic_active}")
        
        # Toggle the microphone state
        self.mic_active = not self.mic_active
        
        if self.mic_active:
            # Microphone is now ON (recording)
            print("Microphone activated - Recording...")
            self.ui.toolButton.setChecked(True)  # This switches to the "On" icon
            
            # Add your voice recording/recognition logic here
            self.start_recording()
            
        else:
            # Microphone is now OFF (muted)
            print("Microphone deactivated - Stopped recording")
            self.ui.toolButton.setChecked(False)  # This switches to the "Off" icon  
            
            # Stop recording logic here
            self.stop_recording()
            
    def start_recording(self):
        """Start make_it_happen_it_works.py as a subprocess"""
        import subprocess
        import os
        print("Starting Harvey voice workflow...")
        # Path to the script (assumes HarveyGUI and harvey-that-fricking-works are siblings)
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'harvey-that-fricking-works', 'make_it_happen_it_works.py'))
        if not os.path.exists(script_path):
            print(f"Script not found: {script_path}")
            return
        # Start the process
        self.process = subprocess.Popen([sys.executable, script_path], cwd=os.path.dirname(script_path))
        print(f"Started process with PID {self.process.pid}")
        
    def stop_recording(self):
        """Stop the make_it_happen_it_works.py subprocess if running"""
        import signal
        if self.process and self.process.poll() is None:
            print(f"Terminating process with PID {self.process.pid}")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except Exception:
                self.process.kill()
            print("Process terminated.")
        else:
            print("No process running.")
        self.process = None
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
