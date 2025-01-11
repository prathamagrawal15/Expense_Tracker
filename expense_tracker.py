import tkinter as tk
from tkinter import messagebox
from collections import defaultdict
import datetime

# transaction history list
class TransactionNode:
    def __init__(self, date, category, amount, description):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description
        self.next = None
        self.prev = None

class TransactionHistory:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_transaction(self, date, category, amount, description):
        new_transaction = TransactionNode(date, category, amount, description)
        if not self.head:
            self.head = self.tail = new_transaction
        else:
            self.tail.next = new_transaction
            new_transaction.prev = self.tail
            self.tail = new_transaction

    def delete_last_transaction(self):
        if not self.tail:
            return None
        deleted = self.tail
        if self.tail.prev:
            self.tail = self.tail.prev
            self.tail.next = None
        else:
            self.head = self.tail = None
        return deleted

# tracker
class ExpenseTracker:
    def __init__(self):
        self.transactions = TransactionHistory()
        self.total_expenses = 0
        self.expenses_by_category = defaultdict(float)

    def add_expense(self, category, amount, description):
        date = datetime.date.today().strftime("%Y-%m-%d")
        self.transactions.add_transaction(date, category, amount, description)
        self.total_expenses += amount
        self.expenses_by_category[category] += amount

    def delete_last_expense(self):
        deleted = self.transactions.delete_last_transaction()
        if deleted:
            self.total_expenses -= deleted.amount
            self.expenses_by_category[deleted.category] -= deleted.amount
            if self.expenses_by_category[deleted.category] <= 0:
                del self.expenses_by_category[deleted.category]
        return deleted

# GUI for Tracker
class ExpenseTrackerApp:
    def __init__(self, root):
        self.tracker = ExpenseTracker()
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.root.geometry("400x500")  # Set window size
        self.root.configure(bg="#e0e0e0")  # Set background color

        # Create a frame for input fields
        input_frame = tk.Frame(root, bg="#e0e0e0")
        input_frame.pack(pady=10)

        # Input fields
        tk.Label(input_frame, text="Category:", bg="#e0e0e0", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(input_frame, font=("Arial", 12), bd=2, relief="groove")
        self.category_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Amount (₹):", bg="#e0e0e0", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(input_frame, font=("Arial", 12), bd=2, relief="groove")
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Description:", bg="#e0e0e0", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
        self.description_entry = tk.Entry(input_frame, font=("Arial", 12), bd=2, relief="groove")
        self.description_entry.grid(row=2, column=1, padx=5, pady=5)

        # Create a frame for buttons
        button_frame = tk.Frame(root, bg="#e0e0e0")
        button_frame.pack(pady=10)

        # Buttons with modern styles
        tk.Button(button_frame, text="Add Expense", command=self.add_expense, bg="#4CAF50", fg="white", font=("Arial", 12), bd=0, relief="flat").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete Last Expense", command=self.delete_last_expense, bg="#f44336", fg="white", font=("Arial", 12), bd=0, relief="flat").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Show Summary", command=self.show_summary, bg="#2196F3", fg="white", font=("Arial", 12), bd=0, relief="flat").pack(side=tk.LEFT, padx=5)

        # Transaction History Display
        self.history_label = tk.Label(root, text="Transaction History:", font=("Arial", 12, "bold"), bg="#e0e0e0")
        self.history_label.pack(pady=5)

        self.history_text = tk.Text(root, height=10, width=40, state="disabled", font=("Arial", 12), bd=2, relief="groove")
        self.history_text.pack(pady=5)

    def add_expense(self):
        category = self.category_entry.get().strip()
        description = self.description_entry.get().strip()
        try:
            amount = float(self.amount_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Amount must be a valid number.")
            return

        if not category or not description or amount <= 0:
            messagebox.showerror("Invalid Input", "All fields must be filled correctly.")
            return

        self.tracker.add_expense(category, amount, description)
        self.update_history()
        messagebox.showinfo("Success", "Expense added successfully!")
        self.clear_inputs()

    def delete_last_expense(self):
        deleted = self.tracker.delete_last_expense()
        if deleted:
            self.update_history()
            messagebox.showinfo("Deleted", f"Deleted last expense: ₹{deleted.amount} ({deleted.description})")
        else:
            messagebox.showinfo("No Expenses", "No expenses to delete.")

    def show_summary(self):
        summary = f"Total Expenses: ₹{self.tracker.total_expenses:.2f}\n\nExpenses by Category:\n"
        for category, total in self.tracker.expenses_by_category.items():
            summary += f"- {category}: ₹{total:.2f}\n"
        messagebox.showinfo("Summary", summary)

    def update_history(self):
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)
        current = self.tracker.transactions.head
        while current:
            self.history_text.insert(tk.END, f"{current.date} - {current.category}: ₹{current.amount} ({current.description})\n")
            current = current.next
        self.history_text.config(state="disabled")

    def clear_inputs(self):
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

# Run GUI Application
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
