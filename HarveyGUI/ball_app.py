# ball_app.py - Standalone spinning ball application using ball.png
import sys
import math
import os
import subprocess
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPainter, QPixmap, QTransform

from pathlib import Path
class StandaloneBall(QWidget):
    def __init__(self):
        super().__init__()
        self.harvey_process = None  # Track running Harvey process
        self.setupUI()
        self.setupAnimation()
        self.load_ball_image()
        
    def setupUI(self):
        # Make window frameless and transparent
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Set size for the ball
        self.setFixedSize(200, 200)  # Adjust based on your ball.png size
        self.move(400, 300)  # Center on screen
        
        # Enable focus so we can receive keyboard events
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()  # Give focus to this widget
        
        # Animation variables
        self.rotation = 0  # Current rotation angle
        self.is_spinning = False  # Start stopped, spin when clicked
        self.ball_pixmap = None
        self.original_size = 160  # Original size of the ball
        self.large_size = 280  # Much larger size when spinning (was 200)
        self.current_scale = 1.0  # Current scale factor
        self.target_scale = 1.0  # Target scale factor
        self.scale_speed = 0.1  # Speed of scaling animation
        
        # Dragging variables
        self.dragging = False
        self.drag_start_position = None
        
    def load_ball_image(self):
        """Load the ball.png image"""
        try:
            # Try to load ball.png from the current directory
            if os.path.exists("ball.png"):
                self.ball_pixmap = QPixmap("ball.png")
                print("Loaded ball.png successfully")
            else:
                print("ball.png not found in current directory")
                # Create a simple fallback circle if image not found
                self.ball_pixmap = QPixmap(160, 160)
                self.ball_pixmap.fill(Qt.transparent)
                painter = QPainter(self.ball_pixmap)
                painter.setRenderHint(QPainter.Antialiasing)
                painter.setBrush(Qt.blue)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(0, 0, 160, 160)
                painter.end()
                print("Using fallback blue circle")
                
            # Scale the image to original size
            if self.ball_pixmap:
                self.ball_pixmap = self.ball_pixmap.scaled(self.original_size, self.original_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                
        except Exception as e:
            print(f"Error loading ball image: {e}")
            self.ball_pixmap = None
        
    def setupAnimation(self):
        # Timer for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateAnimation)
        
    def start_spinning(self):
        """Start the ball spinning, scale it up, and launch make_it_happen_it_works.py"""
        print("Starting ball spinning and launching Harvey workflow...")
        self.is_spinning = True
        self.target_scale = self.large_size / self.original_size  # Scale to larger size
        self.timer.start(16)  # ~60 FPS
        # Launch make_it_happen_it_works.py
        try:
            script_path = Path(__file__).resolve().parent.parent / 'harvey-that-fricking-works' / 'make_it_happen_it_works.py'
            if script_path.exists():
                self.harvey_process = subprocess.Popen([sys.executable, str(script_path)])
                print(f"Started make_it_happen_it_works.py with PID {self.harvey_process.pid}")
            else:
                print(f"Script not found: {script_path}")
        except Exception as e:
            print(f"❌ Failed to start script: {e}")
        
    def stop_spinning(self):
        """Stop the ball spinning, scale it back to original size, and terminate the Harvey process"""
        print("Stopping ball spinning and terminating Harvey workflow...")
        self.is_spinning = False
        self.target_scale = 1.0  # Scale back to original size
        # Keep timer running for scale animation
        if not self.timer.isActive():
            self.timer.start(16)
        # Terminate the make_it_happen_it_works.py process
        try:
            if self.harvey_process and self.harvey_process.poll() is None:
                print(f"Terminating process with PID {self.harvey_process.pid}")
                self.harvey_process.terminate()
                try:
                    self.harvey_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.harvey_process.kill()
                print("Process terminated.")
            else:
                print("No process running.")
        except Exception as e:
            print(f"❌ Failed to stop process: {e}")
        self.harvey_process = None
        
    def toggle_spinning(self):
        """Toggle spinning on/off"""
        if self.is_spinning:
            self.stop_spinning()
        else:
            self.start_spinning()
        
    def updateAnimation(self):
        # Update rotation if spinning
        if self.is_spinning:
            self.rotation += 3  # Speed of rotation (degrees per frame)
            if self.rotation >= 360:
                self.rotation = 0
        
        # Update scaling animation
        if abs(self.current_scale - self.target_scale) > 0.01:
            # Animate towards target scale
            if self.current_scale < self.target_scale:
                self.current_scale += self.scale_speed
                if self.current_scale > self.target_scale:
                    self.current_scale = self.target_scale
            else:
                self.current_scale -= self.scale_speed
                if self.current_scale < self.target_scale:
                    self.current_scale = self.target_scale
        elif not self.is_spinning and self.current_scale == self.target_scale:
            # Stop timer if not spinning and scaling is done
            self.timer.stop()
        
        self.update()  # Trigger repaint
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Set 10% transparency (90% opacity)
        painter.setOpacity(0.90)
        
        # Clear background to fully transparent
        painter.fillRect(self.rect(), Qt.transparent)
        
        if self.ball_pixmap:
            # Calculate center position for the ball
            center_x = self.width() // 2
            center_y = self.height() // 2
            
            # Apply current scale to the pixmap size
            scaled_width = int(self.ball_pixmap.width() * self.current_scale)
            scaled_height = int(self.ball_pixmap.height() * self.current_scale)
            
            # Create transformation for rotation and scaling
            transform = QTransform()
            transform.translate(center_x, center_y)  # Move to center
            transform.rotate(self.rotation)  # Rotate
            transform.scale(self.current_scale, self.current_scale)  # Scale
            transform.translate(-self.ball_pixmap.width() // 2, -self.ball_pixmap.height() // 2)  # Move back
            
            painter.setTransform(transform)
            painter.drawPixmap(0, 0, self.ball_pixmap)
        else:
            # Fallback: draw text if no image
            painter.setPen(Qt.white)
            painter.drawText(self.rect(), Qt.AlignCenter, "No\nBall\nImage")
            
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Start dragging
            self.dragging = True
            self.drag_start_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            
    def mouseMoveEvent(self, event):
        # Handle dragging
        if event.buttons() == Qt.LeftButton and self.dragging and self.drag_start_position:
            self.move(event.globalPosition().toPoint() - self.drag_start_position)
            
    def mouseReleaseEvent(self, event):
        # Handle click to toggle spinning (only if we weren't dragging much)
        if event.button() == Qt.LeftButton and self.dragging:
            # Check if this was a click (minimal movement) or a drag
            if self.drag_start_position:
                drag_distance = (event.globalPosition().toPoint() - (self.frameGeometry().topLeft() + self.drag_start_position)).manhattanLength()
                
                # If moved less than 10 pixels, consider it a click
                if drag_distance < 10:
                    self.toggle_spinning()
                
            self.dragging = False
            self.drag_start_position = None
            
    def keyPressEvent(self, event):
        # Press Escape to close and exit application
        if event.key() == Qt.Key_Escape:
            print("Escape pressed - closing application...")
            self.close()
            QApplication.quit()  # Ensure the application exits completely
        # Press Space to toggle spinning
        elif event.key() == Qt.Key_Space:
            self.toggle_spinning()
            
    def closeEvent(self, event):
        """Handle window close event"""
        print("Closing Harvey Ball...")
        self.timer.stop()  # Stop the animation timer
        # Kill any running Harvey process
        if self.harvey_process:
            print("Killing running Harvey process...")
            self.harvey_process.terminate()
            try:
                self.harvey_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.harvey_process.kill()
            print("Harvey process killed.")
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the standalone ball
    ball = StandaloneBall()
    ball.show()

    print("Harvey Ball is running!")
    print("- Click on the ball to start/stop spinning (it will grow when spinning)")
    print("- Drag the ball to move it around")
    print("- Press Space to toggle spinning")
    print("- Press Escape to close")

    sys.exit(app.exec())