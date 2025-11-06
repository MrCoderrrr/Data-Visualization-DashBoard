
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Toplevel, simpledialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime
import numpy as np
from tkcalendar import DateEntry  # Still needed for the 'Add Transaction' popup

# --- 🎨 Color & Font Definitions 🎨 ---
COLOR_BG = '#1e1e2e'
COLOR_CONTENT_BG = '#181825'
COLOR_CARD = '#313244'
COLOR_TEXT = '#cdd6f4'
COLOR_TEXT_SUBTLE = '#a6adc8'
COLOR_PRIMARY = '#89b4fa'
COLOR_GREEN = '#a6e3a1'
COLOR_RED = '#f38ba8'
COLOR_YELLOW = '#f9e2af'
COLOR_BORDER = '#45475a'

FONT_FAMILY = 'Arial'
FONT_NORMAL = (FONT_FAMILY, 11)
FONT_BOLD = (FONT_FAMILY, 11, 'bold')
FONT_TITLE = (FONT_FAMILY, 24, 'bold')
FONT_H1 = (FONT_FAMILY, 18, 'bold')
FONT_H2 = (FONT_FAMILY, 14, 'bold')
FONT_KPI = (FONT_FAMILY, 28, 'bold')


class BudgetDashboard:
    def _init_(self, root):
        self.root = root
        self.root.title("💰 Personal Budget & Spending Dashboard")
        self.root.configure(bg=COLOR_BG)
        
        self.root.state('zoomed')  # Start maximized
        self.root.minsize(1200, 700)
        
        # --- Simplified Data Management ---
        self.df = None          # The one and only dataframe
        self.file_path = None   # Path to the loaded file for saving
        self.budgets = {}       # Dictionary to store category budgets
        self.active_view_func = self.show_welcome # Function to refresh
        
        # --- Main Content Canvas ---
        self.main_canvas = None 
        self.main_scrollable_frame = None
        self.main_canvas_frame_id = None
        
        self.setup_styles()
        self.setup_ui()
        self.populate_default_budgets() # Pre-fill some budgets

    def setup_styles(self):
        """Centralized TTK styling for a modern, consistent look."""
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # --- General Widget Styles ---
        self.style.configure('.', 
                             background=COLOR_BG, 
                             foreground=COLOR_TEXT, 
                             font=FONT_NORMAL,
                             bordercolor=COLOR_BORDER)
        
        self.style.configure('TFrame', background=COLOR_BG)
        self.style.configure('TLabel', background=COLOR_BG, foreground=COLOR_TEXT)

        # --- Simple Card Style ---
        self.style.configure('Card.TFrame', 
                             background=COLOR_CARD, 
                             relief='raised', 
                             borderwidth=1, 
                             bordercolor=COLOR_BORDER)
        
        self.style.configure('Card.TLabel', 
                             background=COLOR_CARD, 
                             foreground=COLOR_TEXT, 
                             font=FONT_H2)
        
        self.style.configure('CardSubtle.TLabel', 
                             background=COLOR_CARD, 
                             foreground=COLOR_TEXT_SUBTLE, 
                             font=FONT_H2)
        
        self.style.configure('TButton', 
                             font=FONT_BOLD,
                             background=COLOR_CARD, 
                             foreground=COLOR_TEXT,
                             relief='flat',
                             padding=(10, 8))
        self.style.map('TButton',
                       background=[('active', COLOR_BORDER), ('disabled', COLOR_CARD)],
                       foreground=[('disabled', COLOR_TEXT_SUBTLE)])

        # --- Custom Styles ---
        self.style.configure('Header.TFrame', background=COLOR_PRIMARY)
        self.style.configure('Header.TLabel', 
                             background=COLOR_PRIMARY, 
                             foreground=COLOR_BG, 
                             font=FONT_TITLE)
        
        self.style.configure('Sidebar.TFrame', background=COLOR_CARD)
        
        self.style.configure('Sidebar.TButton', 
                             background=COLOR_CARD, 
                             foreground=COLOR_TEXT_SUBTLE,
                             anchor='w',
                             font=FONT_NORMAL,
                             padding=(15, 10))
        self.style.map('Sidebar.TButton',
                       background=[('active', COLOR_BORDER), ('selected', COLOR_BORDER)],
                       foreground=[('active', COLOR_TEXT), ('selected', COLOR_TEXT)])

        self.style.configure('Accent.TButton', 
                             background=COLOR_PRIMARY, 
                             foreground=COLOR_BG, 
                             font=FONT_BOLD)
        self.style.map('Accent.TButton',
                       background=[('active', '#a0c8ff')])
        
        self.style.configure('Content.TFrame', background=COLOR_CONTENT_BG)
        
        # --- Treeview (Table) Style ---
        self.style.configure('Treeview',
                             background=COLOR_CARD,
                             foreground=COLOR_TEXT,
                             fieldbackground=COLOR_CARD,
                             font=FONT_NORMAL,
                             rowheight=28)
        self.style.configure('Treeview.Heading',
                             background=COLOR_BORDER,
                             foreground=COLOR_TEXT,
                             font=FONT_BOLD,
                             padding=(10, 8))
        self.style.map('Treeview',
                       background=[('selected', COLOR_PRIMARY)],
                       foreground=[('selected', COLOR_BG)])

        # --- Entry Style (for DateEntry and Search) ---
        self.style.configure('TEntry',
                             fieldbackground=COLOR_CARD,
                             foreground=COLOR_TEXT,
                             insertcolor=COLOR_TEXT) # Cursor color
        self.style.map('TEntry',
                       fieldbackground=[('disabled', COLOR_BG), ('readonly', COLOR_CARD)],
                       foreground=[('disabled', COLOR_TEXT_SUBTLE), ('readonly', COLOR_TEXT)])
        
        # --- Combobox Style ---
        self.style.map('TCombobox',
                       fieldbackground=[('readonly', COLOR_CARD)],
                       selectbackground=[('readonly', COLOR_CARD)],
                       selectforeground=[('readonly', COLOR_TEXT)],
                       background=[('readonly', COLOR_CARD)])
        
        # --- Progressbar Style ---
        self.style.configure('Green.Horizontal.TProgressbar', 
                             troughcolor=COLOR_BG, 
                             background=COLOR_GREEN)
        self.style.configure('Red.Horizontal.TProgressbar', 
                             troughcolor=COLOR_BG, 
                             background=COLOR_RED)
        
        # Scrollbar
        self.style.configure('Vertical.TScrollbar', 
                             background=COLOR_CARD, 
                             troughcolor=COLOR_BG, 
                             arrowcolor=COLOR_TEXT)
        self.style.map('Vertical.TScrollbar',
                       background=[('active', COLOR_BORDER)])

    def setup_ui(self):
        """Sets up the main UI layout using a responsive PanedWindow."""
        
        # --- Header ---
        header_frame = ttk.Frame(self.root, style='Header.TFrame', height=80)
        header_frame.pack(fill='x', side='top')
        header_frame.pack_propagate(False)
        
        title_label = ttk.Label(header_frame, 
                                text="💰 Personal Budget & Spending Dashboard",
                                style='Header.TLabel')
        title_label.pack(pady=18) 

        # --- Main Responsive Layout ---
        self.paned_window = ttk.PanedWindow(self.root, orient='horizontal')
        self.paned_window.pack(fill='both', expand=True)

        # --- Left Sidebar ---
        self.sidebar_frame = ttk.Frame(self.paned_window, style='Sidebar.TFrame', width=350) 
        self.paned_window.add(self.sidebar_frame, weight=0) 
        self.sidebar_frame.pack_propagate(False)

        # --- Sidebar: Data Management ---
        upload_frame = ttk.Frame(self.sidebar_frame, style='Card.TFrame')
        upload_frame.pack(pady=20, padx=15, fill='x')
        upload_title = ttk.Label(upload_frame, text="📁 Data Management", style='Card.TLabel')
        upload_title.pack(pady=(10, 5), padx=10, anchor='w')
        
        upload_btn = ttk.Button(upload_frame, text="📂 Upload Excel/CSV File",
                                command=self.load_file,
                                style='Accent.TButton',
                                cursor='hand2')
        upload_btn.pack(pady=(10, 5), padx=10, fill='x')

        self.file_status = ttk.Label(upload_frame, 
                                     text="No file loaded\nSupports: .xlsx, .csv",
                                     font=(FONT_FAMILY, 9), 
                                     background=COLOR_CARD,
                                     foreground=COLOR_TEXT_SUBTLE, 
                                     wraplength=300, 
                                     justify='center')
        self.file_status.pack(pady=5, padx=10)
        
        # --- Sidebar Data Controls ---
        controls_frame = ttk.Frame(self.sidebar_frame, style='Card.TFrame')
        controls_frame.pack(pady=10, padx=15, fill='x')
        
        add_btn = ttk.Button(controls_frame, text="➕ Add Transaction",
                             command=self.open_add_transaction_window,
                             style='TButton', state='disabled', cursor='hand2')
        add_btn.pack(pady=5, padx=10, fill='x')
        self.add_trans_btn = add_btn # Save reference
        
        save_btn = ttk.Button(controls_frame, text="💾 Save Changes",
                              command=self.save_to_excel,
                              style='TButton', state='disabled', cursor='hand2')
        save_btn.pack(pady=5, padx=10, fill='x')
        self.save_btn = save_btn # Save reference

        # --- Sidebar: Visualizations (FIXED: Scrollbar removed) ---
        view_frame = ttk.Frame(self.sidebar_frame, style='Card.TFrame')
        view_frame.pack(pady=10, padx=15, fill='both', expand=True)
        
        view_title = ttk.Label(view_frame, text="📈 Visualizations", style='Card.TLabel')
        view_title.pack(pady=(10, 5), padx=10, anchor='w')
        
        views = [
            ("📊 Overview Dashboard", self.show_overview),
            ("💰 Budgets & Goals", self.show_budgets_page), 
            ("🥧 Spending by Category", self.show_category_pie),
            ("📈 Income vs Expense", self.show_income_expense),
            ("📅 Monthly Trends", self.show_monthly_trends),
            ("✨ Yearly Summary", self.show_yearly_summary), 
            ("🏆 Top 5 Expenses", self.show_top_expenses),
            ("🔔 Subscription Tracker", self.show_subscriptions),
            ("📋 All Transactions", self.show_all_transactions)
        ]
        self.view_buttons = {}
