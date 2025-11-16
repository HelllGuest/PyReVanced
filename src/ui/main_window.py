"""Main GUI window and interface components."""

import tkinter as tk
from tkinter import ttk

from .dialogs import HelpDialog, AboutDialog


class MainWindow:
    """Main application window and UI components."""
    
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
        self.setup_window()
        self.create_menu()
        self.setup_ui()
        
    def setup_window(self):
        """Configure the main window."""
        self.root.title("PyReVanced")
        self.root.geometry("1000x600")
        self.root.minsize(900, 500)
        self.root.resizable(True, True)
        
        # Bind window resize event
        self.root.bind('<Configure>', self.on_window_resize)
    
    def create_menu(self):
        """Create the application menu bar."""
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # File menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Log", command=self.app.export_log)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Help Contents", command=self.show_help_dialog)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)
    
    def setup_ui(self):
        """Setup the main user interface."""
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(1, weight=1)
        
        # Status bar with system info and settings
        self.create_status_bar(main_frame)
        
        # File input sections
        self.create_file_inputs(main_frame)
        
        # Progress section
        self.create_progress_section(main_frame)
        
        # Log area
        self.create_log_area(main_frame)
        
        # Control buttons at bottom
        self.create_control_buttons(main_frame)
        
        main_frame.rowconfigure(8, weight=1)
        self.app.cli_entry.focus()
    
    def create_status_bar(self, parent):
        """Create the status bar with system info and settings."""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        status_frame.columnconfigure(1, weight=1)
        
        # System status (left)
        status_left = ttk.Frame(status_frame)
        status_left.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(status_left, text="Status:").pack(side=tk.LEFT)
        ttk.Label(status_left, textvariable=self.app.system_status, 
                 foreground="blue").pack(side=tk.LEFT, padx=(5, 0))
        ttk.Label(status_left, text="Java:").pack(side=tk.LEFT, padx=(20, 0))
        ttk.Label(status_left, textvariable=self.app.java_version).pack(side=tk.LEFT, padx=(5, 0))
        
        # Settings (right)
        status_right = ttk.Frame(status_frame)
        status_right.grid(row=0, column=2, sticky=tk.E)
        
        self.app.logs_var = tk.BooleanVar(value=self.app.config_manager.save_logs_enabled)
        self.app.config_var = tk.BooleanVar(value=self.app.config_manager.save_config_enabled)
        
        ttk.Label(status_right, text="Settings:").pack(side=tk.LEFT, padx=(0, 5))
        
        checkboxes = [
            ("Logs", self.app.logs_var),
            ("Config", self.app.config_var)
        ]
        
        for text, variable in checkboxes:
            ttk.Checkbutton(status_right, text=text, variable=variable, 
                           command=self.app.update_preferences).pack(side=tk.LEFT, padx=(0, 10))
    
    def create_file_inputs(self, parent):
        """Create file input sections."""
        file_inputs = [
            (2, "ReVanced CLI JAR:", self.app.cli_jar_path, self.app.browse_cli_jar, "cli_entry"),
            (3, "Patches RVP:", self.app.patches_rvp_path, self.app.browse_patches, "patches_entry"),
            (4, "APK File:", self.app.apk_path, self.app.browse_apk, "apk_entry"),
            (5, "Output Directory:", self.app.output_path, self.app.browse_output, None),
            (6, "Output Filename:", self.app.output_filename, None, None)
        ]
        
        for row, label_text, variable, browse_cmd, entry_attr in file_inputs:
            ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=8)
            
            entry = ttk.Entry(parent, textvariable=variable)
            entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5, pady=8)
            
            if entry_attr:
                setattr(self.app, entry_attr, entry)
            
            if browse_cmd:
                ttk.Button(parent, text="Browse", command=browse_cmd).grid(
                    row=row, column=2, padx=5, pady=8)
        
        # Add trace for APK path to update output filename
        self.app.apk_path.trace_add('write', self.app.update_output_filename)
    
    def create_progress_section(self, parent):
        """Create progress bar and status label."""
        ttk.Label(parent, text="Progress:").grid(row=7, column=0, sticky=tk.W, pady=(20, 5))
        
        self.app.progress_bar = ttk.Progressbar(parent, mode='determinate', length=300)
        self.app.progress_bar.grid(row=7, column=1, sticky=(tk.W, tk.E), pady=(20, 5), padx=5, ipady=3)
        self.app.progress_bar['value'] = 0
        
        self.app.status_label = ttk.Label(parent, text="Ready", foreground="green")
        self.app.status_label.grid(row=7, column=2, sticky=tk.W, pady=(20, 5))
    
    def create_log_area(self, parent):
        """Create the log output area with scrollbar."""
        progress_frame = ttk.Frame(parent)
        progress_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=8)
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.rowconfigure(0, weight=1)
        
        self.app.progress_text = tk.Text(progress_frame, height=15, width=70)
        self.app.progress_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(progress_frame, orient=tk.VERTICAL, command=self.app.progress_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.app.progress_text.configure(yscrollcommand=scrollbar.set)
    
    def create_control_buttons(self, parent):
        """Create control buttons at the bottom of the window."""
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(15, 0))
        
        # Center the buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(expand=True)
        
        # Main action buttons - all same size
        buttons = [
            ("Patch APK", self.app.patch_apk),
            ("Reset", self.app.clear_all),
            ("Exit", self.root.quit)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(button_frame, text=text, command=command, width=12)
            btn.pack(side=tk.LEFT, padx=8)
    
    def on_window_resize(self, event):
        """Handle window resize events."""
        # Window resize handling (font sizing removed)
        pass
    
    def show_help_dialog(self):
        """Show the help dialog."""
        HelpDialog.show(self.root)
    
    def show_about(self):
        """Show the about dialog."""
        AboutDialog.show(self.root, self.app.__version__, self.app.__author__, self.app.__license__)