"""Dialog windows for help and about information."""

import tkinter as tk
from tkinter import ttk


class HelpDialog:
    """Help dialog with usage instructions."""
    
    @staticmethod
    def show(parent):
        """Show help dialog with usage instructions."""
        help_window = tk.Toplevel(parent)
        help_window.title("Help")
        help_window.geometry("600x500")
        help_window.resizable(True, True)
        help_window.transient(parent)
        help_window.grab_set()
        
        # Center the window
        help_window.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - help_window.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - help_window.winfo_height()) // 2
        help_window.geometry(f"+{x}+{y}")
        
        # Help content
        help_frame = ttk.Frame(help_window, padding="20")
        help_frame.pack(fill=tk.BOTH, expand=True)
        # Usage instructions
        usage_text = tk.Text(help_frame, wrap=tk.WORD)
        usage_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        usage_content = """USAGE INSTRUCTIONS:

1. Select ReVanced CLI JAR file using the browse button
2. Select patches RVP file using the browse button
3. Choose APK file to patch using the browse button
4. Output directory automatically set to APK's location
5. Click 'Patch APK' to start the process
6. Monitor progress in the log area

BUTTONS:
- Patch APK: Start the patching process
- Reset: Clear all file paths and log, start fresh
- Exit: Close the application

AUTOMATIC FEATURES:
- JAR and RVP paths are remembered between sessions
- Output directory automatically matches APK file location
- Output filename gets '-patched' suffix automatically

SETTINGS:
- Logs: Enable/disable saving logs to file
- Config: Enable/disable saving configuration between sessions

The application automatically validates your system and files before patching.
"""
        usage_text.insert(tk.END, usage_content)
        usage_text.config(state=tk.DISABLED)
        
        # Close button
        ttk.Button(help_frame, text="Close", command=help_window.destroy).pack()


class AboutDialog:
    """Modern about dialog with comprehensive application information."""
    
    @staticmethod
    def show(parent, version: str, author: str, license_name: str):
        """Show modern about dialog with application information."""
        about_window = tk.Toplevel(parent)
        about_window.title("About")
        about_window.geometry("550x300")
        about_window.minsize(400, 300)
        about_window.resizable(True, True)
        about_window.transient(parent)
        about_window.grab_set()
        
        # Set window icon and styling
        about_window.configure(bg='#f0f0f0')
        
        # Center the window
        about_window.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - about_window.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - about_window.winfo_height()) // 2
        about_window.geometry(f"+{x}+{y}")
        
        # Main container
        main_frame = ttk.Frame(about_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header section - compact layout
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(header_frame, text="PyReVanced").pack()
        ttk.Label(header_frame, text="Unofficial Python GUI - Use ReVanced responsibly").pack(pady=(2, 0))
        ttk.Label(header_frame, text=f"Version {version}", 
                 foreground="#0066cc").pack(pady=(5, 0))
        
        # Info grid
        info_frame = ttk.LabelFrame(main_frame, text="Application Information", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create info grid
        info_data = [
            ("Developer:", author),
            ("License:", license_name)
        ]
        
        for label, value in info_data:
            row_frame = ttk.Frame(info_frame)
            row_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(row_frame, text=label, 
                     width=15).pack(side=tk.LEFT, anchor=tk.W)
            ttk.Label(row_frame, text=value).pack(side=tk.LEFT, padx=(10, 0))
        

        # Links section
        links_frame = ttk.LabelFrame(main_frame, text="Resources & Support", padding="10")
        links_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create clickable links in a single line
        links_data = [
            ("Source Code", "https://github.com/HelllGuest/PyReVanced"),
            ("ReVanced Project", "https://github.com/revanced"),
            ("CLI Downloads", "https://github.com/revanced/revanced-cli/releases"),
            ("Patches", "https://github.com/revanced/revanced-patches/releases")
        ]
        
        # Single line container for all links
        links_container = ttk.Frame(links_frame)
        links_container.pack(expand=True)
        
        for i, (label, url) in enumerate(links_data):
            # Create clickable label
            link_label = ttk.Label(links_container, text=label, 
                                  foreground="blue", cursor="hand2")
            link_label.pack(side=tk.LEFT, padx=(0, 15) if i < len(links_data)-1 else (0, 0))
            
            # Bind click event to open URL
            link_label.bind("<Button-1>", lambda e, url=url: AboutDialog._open_url(url))
            link_label.bind("<Enter>", lambda e, lbl=link_label: lbl.configure(foreground="darkblue"))
            link_label.bind("<Leave>", lambda e, lbl=link_label: lbl.configure(foreground="blue"))
        

    
    @staticmethod
    def _open_url(url):
        """Open URL in default web browser."""
        import webbrowser
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Could not open URL: {e}")