import tkinter as tk
import subprocess
import sys
import os
from PIL import Image, ImageTk

class FaceRecognitionAttendanceApp:
    def __init__(self, master):
        # Color Palette
        self.colors = {
            'primary_blue': '#0000FF',      # Primary Blue
            'white': '#FFFFFF',             # White
            'navy_blue': '#000080',         # Navy Blue
            'background': '#F0F0F0'         # Soft background
        }

        self.master = master
        master.title("Face Recognition Attendance System")
        master.geometry("800x900")  # Slightly increased window size
        master.configure(bg=self.colors['background'])

        # Get current directory
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

        # Main Container
        self.main_container = tk.Frame(master, bg=self.colors['background'])
        self.main_container.pack(expand=True, fill='both', padx=20, pady=20)

        # Logo and Header Section
        self.header_frame = tk.Frame(self.main_container, bg=self.colors['background'])
        self.header_frame.pack(side='top', fill='x', pady=(0, 20))

        # Logo filenames with full paths
        self.right_logo_path = os.path.join(self.current_dir, 'isi.png')

        # Logo Frame
        self.logo_frame = tk.Frame(self.header_frame, bg=self.colors['background'])
        self.logo_frame.pack(fill='x', expand=True)

        # Right Logo Space
        self.right_logo_label = self.create_logo_label(200, 200)  # Use original dimensions
        self.right_logo_label.pack(side='right', padx=10)
        self.load_logo(self.right_logo_path, self.right_logo_label)

        # Title Label
        self.title_label = tk.Label(
            self.main_container, 
            text="Face Recognition\nAttendance System", 
            font=("Helvetica", 24, "bold"),
            bg=self.colors['background'],
            fg=self.colors['primary_blue']
        )
        self.title_label.pack(pady=20)

        # Buttons Frame
        self.button_frame = tk.Frame(self.main_container, bg=self.colors['background'])
        self.button_frame.pack(expand=True)

        # Button Configurations
        button_configs = [
            ("Capture Faces", "get_faces_from_camera_tkinter.py", 
             "Open camera to capture faces for registration"),
            ("Extract Features", "features_extraction_to_csv.py", 
             "Extract facial features and save to CSV"),
            ("Take Attendance", "attendance_taker.py", 
             "Run face recognition and mark attendance"),
            ("Web Interface", "app.py", 
             "Open web-based interface for attendance")
        ]

        # Create Buttons
        for title, script, tooltip in button_configs:
            btn = self.create_button(title, script, tooltip)
            btn.pack(pady=10, padx=40, fill='x')

    def create_logo_label(self, width, height):
        """Create a logo label with consistent styling"""
        return tk.Label(
            self.logo_frame, 
            bg=self.colors['background'],  # Changed from white to match background
            width=width,
            height=height
        )

    def load_logo(self, logo_path, label):
        """
        Load and set logo with advanced error handling and resizing
        """
        try:
            # Detailed file path checking
            print(f"Attempting to load logo from: {logo_path}")
            
            # Check if file exists
            if not os.path.exists(logo_path):
                print(f"Error: Logo file not found at {logo_path}")
                return

            # Open the image
            original_image = Image.open(logo_path)
            
            # Get original image dimensions
            original_width, original_height = original_image.size
            print(f"Original logo dimensions: {original_width}x{original_height}")
            
            # Resize with specific constraints
            resized_image = original_image.resize((label['width'], label['height']), Image.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(resized_image)
            
            # Update label
            label.configure(image=photo)
            label.image = photo  # Keep a reference!
            
            print(f"Logo loaded successfully: {logo_path}")
        
        except FileNotFoundError:
            print(f"File not found: {logo_path}")
        except Image.UnidentifiedImageError:
            print(f"Unidentified image format: {logo_path}")
        except Exception as e:
            print(f"Unexpected error loading logo {logo_path}: {e}")

    def create_button(self, title, script, tooltip):
        """Create styled buttons"""
        btn = tk.Button(
            self.button_frame, 
            text=title,
            command=lambda: self.run_script(script),
            font=("Helvetica", 12, "bold"),
            bg=self.colors['navy_blue'],
            fg=self.colors['white'],
            activebackground='#0000FF',
            relief=tk.RAISED,
            height=2,
            borderwidth=3
        )
        
        # Hover effects
        btn.bind("<Enter>", lambda e: e.widget.configure(
            bg='#0000FF', 
            fg=self.colors['white']
        ))
        btn.bind("<Leave>", lambda e: e.widget.configure(
            bg=self.colors['navy_blue'], 
            fg=self.colors['white']
        ))
        
        return btn

    def run_script(self, script_name):
        """Run the selected script"""
        try:
            subprocess.Popen([sys.executable, script_name])
        except Exception as e:
            tk.messagebox.showerror("Error", f"Could not run {script_name}: {str(e)}")

def main():
    root = tk.Tk()
    app = FaceRecognitionAttendanceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()