def show_subscriptions(self):
    if self.df is None:
        return
    self.clear_content_frame()
    self.set_active_button(self.show_subscriptions)

    subscription_keywords = [
        'subscription', 'netflix', 'spotify', 'amazon prime',
        'youtube', 'hulu', 'disney', 'apple', 'gym', 'membership'
    ]

    subs = self.df[
        (self.df['Type'] == 'Expense') &
        (
            self.df['Category'].str.lower().str.contains('|'.join(subscription_keywords), na=False) |
            self.df.get('Description', pd.Series(dtype=str)).str.lower().str.contains('|'.join(subscription_keywords), na=False)
        )
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

    title_lbl = ttk.Label(total_frame, text="Total Subscription Cost",
                          style='CardSubtle.TLabel', anchor='center')
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
    if self.df is None:
        return
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

    populate_tree(self.df)


# --- Budget Page Functions ---
def populate_default_budgets(self):
    """Pre-populates some budgets for demo purposes."""
    self.budgets = {
        'Food': 10000,
        'Shopping': 8000,
        'Transport': 5000,
        'Entertainment': 3000
    }


def set_category_budget(self):
    """Opens dialogs to set a budget for a category."""
    category = simpledialog.askstring("Set Budget", "Enter category name:", parent=self.root)
    if not category:
        return

    amount = simpledialog.askfloat("Set Budget", f"Enter monthly budget for '{category}':", parent=self.root)
    if amount is not None and amount >= 0:
        self.budgets[category] = amount
        self.show_budgets_page()  # Refresh the view
    elif amount is not None:
        messagebox.showerror("Error", "Budget must be a positive number.")


def show_budgets_page(self):
    if self.df is None:
        return
    self.clear_content_frame()
    self.set_active_button(self.show_budgets_page)

    if self.df.empty:
        latest_month = "N/A"
        current_month_df = pd.DataFrame()
    else:
        latest_date_in_data = self.df['Date'].max()
        latest_month = latest_date_in_data.strftime('%B %Y')
        current_month_df = self.df[
            (self.df['Date'].dt.year == latest_date_in_data.year) &
            (self.df['Date'].dt.month == latest_date_in_data.month) &
            (self.df['Type'] == 'Expense')
        ]

    header_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
    header_frame.pack(fill='x', padx=40, pady=20)

    title = ttk.Label(header_frame, text=f"💰 Monthly Budgets ({latest_month})",
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

        ttk.Label(title_frame, text=f"₹{spending:,.0f} / ₹{budget_amount:,.0f}",
                  font=FONT_H2, background=COLOR_CARD, foreground=text_color).pack(side='right')

        pb = ttk.Progressbar(card, orient='horizontal', length=300,
                             mode='determinate', style=style_name)
        pb.pack(fill='x', padx=20, pady=(5, 20))
        pb['value'] = min(percentage, 100)

    self.root.update_idletasks()
    self.on_scrollframe_configure()


# --- Main execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetDashboard(root)
    root.mainloop()
