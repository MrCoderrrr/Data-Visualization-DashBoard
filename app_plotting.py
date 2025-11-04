import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime
import numpy as np

# Import styles and colors
from app_styles import (COLOR_CONTENT_BG, COLOR_BG, COLOR_CARD, COLOR_TEXT, 
                        COLOR_TEXT_SUBTLE, COLOR_GREEN, COLOR_RED, 
                        COLOR_YELLOW, COLOR_BORDER, FONT_H1, FONT_H2, FONT_KPI)

class AppPlotting:
    """Handles rendering all pages and visualizations."""

    # --- 🎨 Matplotlib Styling Helper 🎨 ---
    def style_matplotlib_fig(self, fig, ax_list):
        if not isinstance(ax_list, (list, np.ndarray)):
            ax_list = [ax_list]
        fig.patch.set_facecolor(COLOR_CONTENT_BG)
        for ax in ax_list:
            ax.set_facecolor(COLOR_CARD)
            ax.title.set_color(COLOR_TEXT)
            ax.xaxis.label.set_color(COLOR_TEXT_SUBTLE)
            ax.yaxis.label.set_color(COLOR_TEXT_SUBTLE)
            ax.tick_params(axis='x', colors=COLOR_TEXT)
            ax.tick_params(axis='y', colors=COLOR_TEXT)
            for spine in ax.spines.values():
                spine.set_edgecolor(COLOR_BORDER)
            legend = ax.get_legend()
            if legend:
                legend.get_frame().set_facecolor(COLOR_CARD)
                legend.get_frame().set_edgecolor(COLOR_BORDER)
                for text in legend.get_texts():
                    text.set_color(COLOR_TEXT)
                    
    # --- 📊 Visualization Methods 📊 ---
    def show_overview(self):
        if self.df is None: return
        self.clear_content_frame()
        self.set_active_button(self.show_overview)

        kpi_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        kpi_frame.pack(fill='x', padx=10, pady=10)
        
        income = self.df[self.df['Type'] == 'Income']['Amount'].sum()
        expenses = self.df[self.df['Type'] == 'Expense']['Amount'].sum()
        balance = income - expenses
        
        self.create_kpi_card(kpi_frame, "Total Income", f"₹{income:,.2f}", COLOR_GREEN)
        self.create_kpi_card(kpi_frame, "Total Expenses", f"₹{expenses:,.2f}", COLOR_RED)
        self.create_kpi_card(kpi_frame, "Net Balance", f"₹{balance:,.2f}", 
                             COLOR_GREEN if balance >= 0 else COLOR_RED)

        charts_frame = self.create_scrollable_container()

        # --- Pie Chart: Spending by Category ---
        fig1 = Figure(figsize=(10, 6), dpi=100)
        ax1 = fig1.add_subplot(111)
        expense_data = self.df[self.df['Type'] == 'Expense'].groupby('Category')['Amount'].sum()
        colors = plt.cm.Pastel2(np.linspace(0, 1, len(expense_data)))
        
        if not expense_data.empty:
            wedges, texts, autotexts = ax1.pie(
                expense_data.values, 
                autopct='%1.1f%%',
                startangle=90, 
                colors=colors, 
                pctdistance=0.85,
                wedgeprops={'edgecolor': COLOR_TEXT, 'linewidth': 1}
            )
            for autotext in autotexts:
                autotext.set_color(COLOR_BG)
                autotext.set_fontweight('bold')
            ax1.legend(expense_data.index, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
        else:
            ax1.text(0.5, 0.5, "No Expense Data", horizontalalignment='center', verticalalignment='center', 
                     transform=ax1.transAxes, color=COLOR_TEXT_SUBTLE, fontsize=15)
            
        ax1.set_title('Spending by Category')
        self.style_matplotlib_fig(fig1, ax1)
        
        canvas1 = FigureCanvasTkAgg(fig1, charts_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill='x', expand=True, padx=10, pady=10)

        # --- Bar Chart: Income vs Expense ---
        fig2 = Figure(figsize=(10, 6), dpi=100)
        ax2 = fig2.add_subplot(111)
        
        bar_colors = [COLOR_GREEN, COLOR_RED]
        bars = ax2.bar(['Income', 'Expenses'], [income, expenses], color=bar_colors)
        
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'₹{height:,.0f}',
                    ha='center', va='bottom', color=COLOR_TEXT, fontweight='bold')
                    
        ax2.set_title('Total Income vs Expenses')
        ax2.set_ylabel('Amount (₹)')
        self.style_matplotlib_fig(fig2, ax2)
        
        canvas2 = FigureCanvasTkAgg(fig2, charts_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill='x', expand=True, padx=10, pady=10)

        self.root.update_idletasks()
        self.on_scrollframe_configure()

    def show_category_pie(self):
        if self.df is None: return
        self.clear_content_frame()
        self.set_active_button(self.show_category_pie)

        fig = Figure(figsize=(12, 8), dpi=100)
        ax = fig.add_subplot(111)
        
        expense_data = self.df[self.df['Type'] == 'Expense'].groupby('Category')['Amount'].sum().sort_values(ascending=False)
        
        if not expense_data.empty:
            colors = plt.cm.Set3(np.linspace(0, 1, len(expense_data)))
            wedges, texts, autotexts = ax.pie(
                expense_data.values, 
                autopct='%1.1f%%', 
                startangle=90,
                colors=colors, 
                pctdistance=0.85,
                wedgeprops={'edgecolor': COLOR_TEXT, 'linewidth': 1}
            )
            for autotext in autotexts:
                autotext.set_color(COLOR_BG)
                autotext.set_fontweight('bold')
            legend_labels = [f'{cat}: ₹{amt:,.2f}' for cat, amt in expense_data.items()]
            ax.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)
        else:
            ax.text(0.5, 0.5, "No Expense Data", horizontalalignment='center', verticalalignment='center', 
                     transform=ax.transAxes, color=COLOR_TEXT_SUBTLE, fontsize=15)
            
        ax.set_title('Spending Breakdown by Category', fontsize=18, fontweight='bold')
        self.style_matplotlib_fig(fig, ax)
        
        canvas = FigureCanvasTkAgg(fig, self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=20, pady=20)

    def show_income_expense(self):
        if self.df is None: return
        self.clear_content_frame()
        self.set_active_button(self.show_income_expense)

        fig = Figure(figsize=(12, 7), dpi=100)
        ax = fig.add_subplot(111)
        
        monthly = self.df.copy()
        monthly['Month'] = monthly['Date'].dt.to_period('M').astype(str)
        monthly_summary = monthly.groupby(['Month', 'Type'])['Amount'].sum().unstack(fill_value=0)
        
        if not monthly_summary.empty:
            x = np.arange(len(monthly_summary))
            width = 0.35
            
            if 'Income' in monthly_summary.columns:
                ax.bar(x - width/2, monthly_summary['Income'],
                       width, label='Income', color=COLOR_GREEN)
            if 'Expense' in monthly_summary.columns:
                ax.bar(x + width/2, monthly_summary['Expense'],
                       width, label='Expenses', color=COLOR_RED)
                
            ax.set_xticks(x)
            ax.set_xticklabels(monthly_summary.index, rotation=45, ha='right')
            ax.legend()
        else:
            ax.text(0.5, 0.5, "No Data to Display", horizontalalignment='center', verticalalignment='center', 
                     transform=ax.transAxes, color=COLOR_TEXT_SUBTLE, fontsize=15)
            
        ax.set_title('Monthly Income vs Expenses', fontsize=18)
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount (₹)')
        self.style_matplotlib_fig(fig, ax)
        
        canvas = FigureCanvasTkAgg(fig, self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=20, pady=20)

    def show_monthly_trends(self):
        if self.df is None: return
        self.clear_content_frame()
        self.set_active_button(self.show_monthly_trends)

        fig = Figure(figsize=(12, 7), dpi=100)
        ax = fig.add_subplot(111)
        
        monthly = self.df.copy()
        monthly['Month'] = monthly['Date'].dt.to_period('M').astype(str)
        monthly_summary = monthly.groupby(['Month', 'Type'])['Amount'].sum().unstack(fill_value=0)
        
        if not monthly_summary.empty:
            if 'Income' in monthly_summary.columns:
                ax.plot(monthly_summary.index, monthly_summary['Income'],
                        marker='o', linewidth=3, label='Income', color=COLOR_GREEN, markersize=8)
            if 'Expense' in monthly_summary.columns:
                ax.plot(monthly_summary.index, monthly_summary['Expense'],
                        marker='s', linewidth=3, label='Expenses', color=COLOR_RED, markersize=8)
            ax.legend(fontsize=12)
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        else:
            ax.text(0.5, 0.5, "No Data to Display", horizontalalignment='center', verticalalignment='center', 
                     transform=ax.transAxes, color=COLOR_TEXT_SUBTLE, fontsize=15)
            
        ax.set_title('Monthly Financial Trends', fontsize=18)
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount (₹)')
        ax.grid(True, alpha=0.3, color=COLOR_BORDER, linestyle='--')
        
        self.style_matplotlib_fig(fig, ax)
        
        canvas = FigureCanvasTkAgg(fig, self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=20, pady=20)

    def show_yearly_summary(self):
        if self.df is None: return
        self.clear_content_frame()
        self.set_active_button(self.show_yearly_summary)

        fig = Figure(figsize=(12, 7), dpi=100)
        ax = fig.add_subplot(111)
        
        yearly_df = self.df.copy()
        yearly_df['Year'] = yearly_df['Date'].dt.year
        yearly_summary = yearly_df.groupby(['Year', 'Type'])['Amount'].sum().unstack(fill_value=0)
        
        if not yearly_summary.empty:
            x = np.arange(len(yearly_summary))
            width = 0.35
            
            if 'Income' in yearly_summary.columns:
                ax.bar(x - width/2, yearly_summary['Income'],
                       width, label='Income', color=COLOR_GREEN)
            if 'Expense' in yearly_summary.columns:
                ax.bar(x + width/2, yearly_summary['Expense'],
                       width, label='Expenses', color=COLOR_RED)
            
            ax.set_xticks(x)
            ax.set_xticklabels(yearly_summary.index)
            ax.legend()
        else:
            ax.text(0.5, 0.5, "No Data to Display", horizontalalignment='center', verticalalignment='center', 
                     transform=ax.transAxes, color=COLOR_TEXT_SUBTLE, fontsize=15)
            
        ax.set_title('Yearly Income vs Expenses', fontsize=18)
        ax.set_xlabel('Year')
        ax.set_ylabel('Amount (₹)')
        
        self.style_matplotlib_fig(fig, ax)
        
        canvas = FigureCanvasTkAgg(fig, self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=20, pady=20)

    def show_top_expenses(self):
        if self.df is None: return
        self.clear_content_frame()
        self.set_active_button(self.show_top_expenses)

        top_5 = self.df[self.df['Type'] == 'Expense'].nlargest(5, 'Amount')
        
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        title = ttk.Label(table_frame, text="🏆 Top 5 Highest Expenses",
                          font=FONT_H1, style='TLabel', background=COLOR_CONTENT_BG)
        title.pack(pady=20)

        tree = ttk.Treeview(table_frame, columns=('Date', 'Category', 'Description', 'Amount'),
                            show='headings', height=6, style='Treeview')
        
        tree.heading('Date', text='Date')
        tree.heading('Category', text='Category')
        tree.heading('Description', text='Description')
        tree.heading('Amount', text='Amount')
        
        tree.column('Date', width=150, anchor='center')
        tree.column('Category', width=200, anchor='center')
        tree.column('Description', width=350, anchor='w')
        tree.column('Amount', width=150, anchor='e')
        
        for idx, row in top_5.iterrows():
            tree.insert('', 'end', values=(
                row['Date'].strftime('%Y-%m-%d'),
                row['Category'],
                row.get('Description', 'N/A'),
                f"₹{row['Amount']:,.2f}"
            ))
            
        tree.pack(fill='x', expand=True, pady=10)
        
        total = top_5['Amount'].sum()
        total_label = ttk.Label(table_frame, text=f"💰 Total of Top 5: ₹{total:,.2f}",
                               font=FONT_H2, background=COLOR_CONTENT_BG, foreground=COLOR_YELLOW)
        total_label.pack(pady=10)

    def show_subscriptions(self):
        if self.df is None: return
        self.clear_content_frame()
        self.set_active_button(self.show_subscriptions)

        subscription_keywords = ['subscription', 'netflix', 'spotify', 'amazon prime',
                                'youtube', 'hulu', 'disney', 'apple', 'gym', 'membership']
        
        subs = self.df[
            (self.df['Type'] == 'Expense') &
            (self.df['Category'].str.lower().str.contains('|'.join(subscription_keywords), na=False) |
             self.df.get('Description', pd.Series(dtype=str)).str.lower().str.contains('|'.join(subscription_keywords), na=False))
        ]
        
        display_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        display_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        title = ttk.Label(display_frame, text="🔔 Subscription Tracker",
                          font=FONT_H1, background=COLOR_CONTENT_BG)
        title.pack(pady=20)
        
        if len(subs) == 0:
            no_subs = ttk.Label(display_frame, text="No recurring subscriptions found.",
                                font=FONT_H2, background=COLOR_CONTENT_BG,
                                foreground=COLOR_TEXT_SUBTLE)
            no_subs.pack(pady=50)
            return

        total = subs['Amount'].sum()
        total_frame = ttk.Frame(display_frame, style='Card.TFrame')
        total_frame.pack(pady=10, fill='x')

        title_lbl = ttk.Label(total_frame, text="Total Subscription Cost", style='CardSubtle.TLabel', anchor='center')
        title_lbl.pack(pady=(15, 5), padx=20, fill='x')
        
        total_label = ttk.Label(total_frame,
                                text=f"₹{total:,.2f}",
                                font=FONT_KPI, 
                                background=COLOR_CARD, 
                                foreground=COLOR_RED,
                                anchor='center')
        total_label.pack(pady=(5, 20), padx=20, fill='x', expand=True)

        tree_frame = ttk.Frame(display_frame)
        tree_frame.pack(fill='both', expand=True, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=('Service', 'Category', 'Amount', 'Date'),
                            show='headings', height=15, style='Treeview')
        tree.heading('Service', text='Service')
        tree.heading('Category', text='Category')
        tree.heading('Amount', text='Cost')
        tree.heading('Date', text='Last Charged')
        tree.column('Service', width=250)
        tree.column('Category', width=200)
        tree.column('Amount', width=150, anchor='e')
        tree.column('Date', width=150, anchor='center')
        
        for idx, row in subs.iterrows():
            tree.insert('', 'end', values=(
                row.get('Description', row['Category']),
                row['Category'],
                f"₹{row['Amount']:,.2f}",
                row['Date'].strftime('%Y-%m-%d')
            ))
            
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def show_all_transactions(self):
        if self.df is None: return
        self.clear_content_frame()
        self.set_active_button(self.show_all_transactions)

        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        title = ttk.Label(table_frame, text="📋 All Transactions",
                          font=FONT_H1, background=COLOR_CONTENT_BG)
        title.pack(pady=20)

        search_frame = ttk.Frame(table_frame, style='Content.TFrame')
        search_frame.pack(fill='x', pady=10)
        ttk.Label(search_frame, text="🔍 Search:", font=FONT_BOLD,
                  background=COLOR_CONTENT_BG).pack(side='left', padx=5)
        search_entry = ttk.Entry(search_frame, font=FONT_NORMAL, width=30)
        search_entry.pack(side='left', padx=5, fill='x', expand=True)

        tree_frame = ttk.Frame(table_frame)
        tree_frame.pack(fill='both', expand=True, pady=10)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        tree = ttk.Treeview(
            tree_frame, columns=('Date', 'Category', 'Description', 'Type', 'Amount'),
            show='headings', style='Treeview'
        )
        tree.heading('Date', text='Date', anchor='w')
        tree.heading('Category', text='Category', anchor='w')
        tree.heading('Description', text='Description', anchor='w')
        tree.heading('Type', text='Type', anchor='center')
        tree.heading('Amount', text='Amount', anchor='e')
        tree.column('Date', width=120, anchor='w')
        tree.column('Category', width=150, anchor='w')
        tree.column('Description', width=300, anchor='w')
        tree.column('Type', width=100, anchor='center')
        tree.column('Amount', width=120, anchor='e')
        
        tree.tag_configure('Income', foreground=COLOR_GREEN)
        tree.tag_configure('Expense', foreground=COLOR_RED)

        def populate_tree(df_data):
            for item in tree.get_children():
                tree.delete(item)
            df_data_sorted = df_data.sort_values('Date', ascending=False)
            for idx, row in df_data_sorted.iterrows():
                tag = row['Type']
                tree.insert('', 'end', values=(
                    row['Date'].strftime('%Y-%m-%d'),
                    row['Category'],
                    row.get('Description', 'N/A'),
                    row['Type'],
                    f"₹{row['Amount']:,.2f}"
                ), tags=(tag,))

        def search_transactions():
            query = search_entry.get().lower()
            if not query:
                filtered = self.df
            else:
                filtered = self.df[
                    self.df['Category'].str.lower().str.contains(query, na=False) |
                    self.df.get('Description', pd.Series(dtype=str)).str.lower().str.contains(query, na=False)
                ]
            populate_tree(filtered)

        search_btn = ttk.Button(search_frame, text="Search", 
                                command=search_transactions,
                                style='Accent.TButton', cursor='hand2')
        search_btn.pack(side='left', padx=5)
        clear_btn = ttk.Button(search_frame, text="Clear", 
                               command=lambda: [search_entry.delete(0, tk.END), search_transactions()],
                               style='TButton', cursor='hand2')
        clear_btn.pack(side='left', padx=5)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        # Initial data load
        populate_tree(self.df)

    def show_budgets_page(self):
        if self.df is None: return
        self.clear_content_frame()
        self.set_active_button(self.show_budgets_page)
        
        if self.df.empty:
            latest_month_str = "N/A"
            current_month_df = pd.DataFrame(columns=['Category', 'Amount'])
        else:
            latest_date_in_data = self.df['Date'].max()
            latest_month_str = latest_date_in_data.strftime('%B %Y')
            current_month_df = self.df[
                (self.df['Date'].dt.year == latest_date_in_data.year) &
                (self.df['Date'].dt.month == latest_date_in_data.month) &
                (self.df['Type'] == 'Expense')
            ]
        
        header_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        header_frame.pack(fill='x', padx=40, pady=20)
        
        title = ttk.Label(header_frame, text=f"💰 Monthly Budgets ({latest_month_str})",
                          font=FONT_H1, background=COLOR_CONTENT_BG)
        title.pack(side='left')
        
        set_budget_btn = ttk.Button(header_frame, text="Set New Budget", 
                                    command=self.set_category_budget, 
                                    style='Accent.TButton', cursor='hand2')
        set_budget_btn.pack(side='right')

        budgets_frame = self.create_scrollable_container()
        
        if not self.budgets:
            no_budgets = ttk.Label(budgets_frame, text="No budgets set. Click 'Set New Budget' to start.",
                                   font=FONT_H2, background=COLOR_CONTENT_BG,
                                   foreground=COLOR_TEXT_SUBTLE)
            no_budgets.pack(pady=50, padx=20)
            return

        for category, budget_amount in self.budgets.items():
            spending = current_month_df[current_month_df['Category'] == category]['Amount'].sum()
            
            percentage = (spending / budget_amount) * 100 if budget_amount > 0 else 0
            
            if percentage > 100:
                style_name = 'Red.Horizontal.TProgressbar'
                text_color = COLOR_RED
            else:
                style_name = 'Green.Horizontal.TProgressbar'
                text_color = COLOR_GREEN
                
            card = ttk.Frame(budgets_frame, style='Card.TFrame')
            card.pack(fill='x', padx=20, pady=10)
            
            title_frame = ttk.Frame(card, style='Card.TFrame')
            title_frame.pack(fill='x', padx=20, pady=(15, 5))
            ttk.Label(title_frame, text=category, font=FONT_H2, 
                      background=COLOR_CARD, foreground=COLOR_TEXT).pack(side='left')
            
            ttk.Label(title_frame, text=f"₹{spending:,.0f} / ₹{budget_amount:,.0f}", font=FONT_H2, 
                      background=COLOR_CARD, foreground=text_color).pack(side='right')
            
            pb = ttk.Progressbar(card, orient='horizontal', length=300, 
                                 mode='determinate', style=style_name)
            pb.pack(fill='x', padx=20, pady=(5, 20))
            pb['value'] = min(percentage, 100) # Cap at 100 for display
            
        self.root.update_idletasks()
        self.on_scrollframe_configure()