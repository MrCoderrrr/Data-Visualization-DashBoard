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

        # Use the scrollable container
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
