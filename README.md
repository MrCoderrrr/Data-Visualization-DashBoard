💰 Personal Budget & Financial Dashboard

Project Overview

This project is a modern, cross-platform desktop application designed for personal financial tracking and visualization. Built using Python, Tkinter, Pandas, and Matplotlib, it provides a powerful, clean, dark-themed dashboard for users to monitor income, expenses, and track their monthly budget goals.

The application is engineered using a highly modular structure (4 files) to demonstrate effective team collaboration and independent development efforts.

✨ Key Features

This application is designed for enhanced productivity in financial management, featuring real-time data integration and goal tracking:

Modular Architecture: The codebase is logically separated into 4 distinct modules, ensuring clear development boundaries and easy maintenance for the team.

Budgeting & Goal Tracking: Users can define monthly spending limits for any expense category. The Budgets & Goals page displays real-time, color-coded progress bars (Green for under budget, Red for over) based on the latest transactions in the data.

Transaction Control: Includes a dedicated modal window to add new transactions instantly, keeping the data file up-to-date.

Data Persistence: A Save Changes button allows the user to overwrite the source file (XLSX/CSV), ensuring added transactions and budget updates are permanent.

Comprehensive Visuals: Features dynamic dashboard views, including:

Key Performance Indicators (KPIs): Total Income, Expenses, and Net Balance.

Trend Analysis: Monthly and Yearly Income vs. Expense trends.

Detailed Breakdown: Spending Breakdown by Category (Pie Chart).

Modern UI: Utilizes themed Tkinter widgets (ttk) and custom-styled Matplotlib charts for a professional, consistent dark aesthetic.

🧑‍💻 Team Contribution Structure (Modular Responsibilities)

The project was successfully partitioned into four core modules, with each team member owning a critical, distinct aspect of the application:

Aditya (Module: app_styles.py)

Core Responsibility: UI/Aesthetics and Styling. Defined all visual elements, including the dark theme color palette, font constants, and custom ttk styling rules for buttons, frames, and data entry fields.

Sanket (Module: app_logic_data.py)

Core Responsibility: Data I/O and Management. Implemented the functionality for file loading (load_file), data saving (save_to_excel), and the entire transactional logic for adding new records to the dataset.

Vanshil (Module: app_logic_features.py)

Core Responsibility: Reusable Components and Budget Logic. Developed core infrastructure features, including the scrollable container logic, the reusable KPI card widget, and the foundation for the Budgeting System logic.

Vedant (Module: app_plotting.py)

Core Responsibility: Data Visualization and Rendering. Was responsible for generating all visual pages (show_overview, show_budgets_page, etc.), integrating Matplotlib graphs, and rendering all data tables (Treeview).
