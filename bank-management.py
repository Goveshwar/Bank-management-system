import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Listbox, END
import database_manager as db
import ai_advisor
import os

class BankSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Bank Management System (AI Advisor)")

        # -------- WINDOW SIZE (HALF SCREEN, CENTERED) --------
        self.master.update_idletasks()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        width = screen_width // 2
        height = screen_height // 2

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.master.geometry(f"{width}x{height}+{x}+{y}")
        self.master.minsize(650, 550)
        self.master.resizable(True, True)

        # Better default font
        self.master.option_add("*Font", ("Segoe UI", 11))

        db.setup_database()  # Ensure tables exist

        # ---------- CREATE ACCOUNT FRAME ----------
        self.create_account_frame = tk.LabelFrame(master, text="Create Account", padx=15, pady=15)
        self.create_account_frame.pack(padx=15, pady=10, fill="both", expand=True)

        tk.Label(self.create_account_frame, text="Name:").grid(row=0, column=0, sticky="e", pady=6)
        tk.Label(self.create_account_frame, text="Age:").grid(row=1, column=0, sticky="e", pady=6)
        tk.Label(self.create_account_frame, text="Salary:").grid(row=2, column=0, sticky="e", pady=6)
        tk.Label(self.create_account_frame, text="PIN:").grid(row=3, column=0, sticky="e", pady=6)

        self.name_entry = tk.Entry(self.create_account_frame, width=35)
        self.age_entry = tk.Entry(self.create_account_frame, width=35)
        self.salary_entry = tk.Entry(self.create_account_frame, width=35)
        self.pin_entry = tk.Entry(self.create_account_frame, show="*", width=35)

        self.name_entry.grid(row=0, column=1, pady=6)
        self.age_entry.grid(row=1, column=1, pady=6)
        self.salary_entry.grid(row=2, column=1, pady=6)
        self.pin_entry.grid(row=3, column=1, pady=6)

        tk.Button(
            self.create_account_frame,
            text="Create Account",
            command=self.create_account,
            bg="#2e8b57",
            fg="white"
        ).grid(row=4, column=1, pady=15, sticky="e")

        # ---------- LOGIN FRAME ----------
        self.login_frame = tk.LabelFrame(master, text="Login", padx=15, pady=15)
        self.login_frame.pack(padx=15, pady=10, fill="both", expand=True)

        tk.Label(self.login_frame, text="Name:").grid(row=0, column=0, sticky="e", pady=6)
        tk.Label(self.login_frame, text="PIN:").grid(row=1, column=0, sticky="e", pady=6)

        self.login_name_entry = tk.Entry(self.login_frame, width=35)
        self.login_pin_entry = tk.Entry(self.login_frame, show="*", width=35)

        self.login_name_entry.grid(row=0, column=1, pady=6)
        self.login_pin_entry.grid(row=1, column=1, pady=6)

        tk.Button(
            self.login_frame,
            text="Login",
            command=self.login,
            bg="#4CAF50",
            fg="white"
        ).grid(row=2, column=1, pady=15, sticky="e")

        # ---------- USER FRAME ----------
        self.user_frame = tk.LabelFrame(master, text="Account", padx=15, pady=15)
        self.info_label = tk.Label(self.user_frame, text="", justify="left", anchor="w")
        self.info_label.pack(fill="x", pady=8)

        btn_frame = tk.Frame(self.user_frame)
        btn_frame.pack(pady=10, fill="x")

        tk.Button(btn_frame, text="Deposit", command=self.deposit, bg="#ffd54f").grid(row=0, column=0, padx=8, pady=6)
        tk.Button(btn_frame, text="Withdraw", command=self.withdraw, bg="#ff8a65").grid(row=0, column=1, padx=8)
        tk.Button(btn_frame, text="Transactions", command=self.transactions, bg="#42a5f5", fg="white").grid(row=0, column=2, padx=8)

        tk.Button(btn_frame, text="AI Advisor", command=self.ai_insights, bg="#7b1fa2", fg="white").grid(row=1, column=0, padx=8, pady=6)
        tk.Button(btn_frame, text="Ask AI", command=self.ask_ai, bg="#5c6bc0", fg="white").grid(row=1, column=1, padx=8)
        tk.Button(btn_frame, text="Monthly Report", command=self.monthly_report, bg="#26a69a", fg="white").grid(row=1, column=2, padx=8)

        tk.Button(
            self.user_frame,
            text="Logout",
            command=self.logout,
            bg="#e57373",
            fg="white"
        ).pack(pady=12, fill="x", ipady=4)

        self.current_user = None

    # ---------- LOGIC METHODS (UNCHANGED) ----------
    def create_account(self):
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        salary = self.salary_entry.get().strip()
        pin = self.pin_entry.get().strip()
        if not all([name, age, salary, pin]):
            messagebox.showerror("Error", "All fields are required!")
            return
        try:
            db.add_user(name, int(age), float(salary), pin)
            messagebox.showinfo("Success", "Account Created! You can now login.")
            self.name_entry.delete(0, END)
            self.age_entry.delete(0, END)
            self.salary_entry.delete(0, END)
            self.pin_entry.delete(0, END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def login(self):
        name = self.login_name_entry.get().strip()
        pin = self.login_pin_entry.get().strip()
        user = db.get_user(name, pin)
        if user:
            self.current_user = user
            self.show_user()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    def show_user(self):
        self.create_account_frame.pack_forget()
        self.login_frame.pack_forget()
        self.user_frame.pack(padx=15, pady=10, fill="both", expand=True)
        self.refresh_user_info()

    def refresh_user_info(self):
        self.current_user = db.get_user(self.current_user[1], self.current_user[4])
        name, age, salary, balance = self.current_user[1], self.current_user[2], self.current_user[3], self.current_user[5]
        self.info_label.config(
            text=f"Welcome, {name}\nAge: {age}\nSalary: ₹{salary}\nBalance: ₹{balance:.2f}"
        )

    def deposit(self):
        amt = simpledialog.askfloat("Deposit", "Enter amount:", minvalue=0.0)
        if amt and amt > 0:
            db.update_balance(self.current_user[4], self.current_user[5] + amt)
            db.log_transaction(self.current_user[4], f"Deposited ₹{amt:.2f}")
            self.refresh_user_info()

    def withdraw(self):
        amt = simpledialog.askfloat("Withdraw", "Enter amount:", minvalue=0.0)
        if amt and amt <= self.current_user[5]:
            db.update_balance(self.current_user[4], self.current_user[5] - amt)
            db.log_transaction(self.current_user[4], f"Withdrew ₹{amt:.2f}")
            self.refresh_user_info()

    def transactions(self):
        txs = db.get_transactions(self.current_user[4])
        win = Toplevel(self.master)
        win.title("Transactions")
        win.geometry("520x380")
        lb = Listbox(win)
        lb.pack(fill="both", expand=True, padx=10, pady=10)
        for d, t in txs:
            lb.insert(END, f"{t} — {d}")

    def ai_insights(self):
        result = ai_advisor.analyze_transactions(self.current_user[4])
        win = Toplevel(self.master)
        win.title("AI Insights")
        win.geometry("600x420")
        text = tk.Text(win, wrap="word")
        text.pack(fill="both", expand=True)
        text.insert("1.0", result)
        text.config(state="disabled")

    def ask_ai(self):
        q = simpledialog.askstring("Ask AI", "Enter your question:")
        if q:
            messagebox.showinfo("AI Response", ai_advisor.ask_financial_question(q))

    def monthly_report(self):
        report = ai_advisor.generate_monthly_report(self.current_user[4])
        fname = f"monthly_report_{self.current_user[4]}.txt"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(report)
        messagebox.showinfo("Saved", f"Report saved as {fname}")

    def logout(self):
        self.user_frame.pack_forget()
        self.create_account_frame.pack(padx=15, pady=10, fill="both", expand=True)
        self.login_frame.pack(padx=15, pady=10, fill="both", expand=True)
        self.current_user = None


if __name__ == "__main__":
    root = tk.Tk()
    BankSystem(root)
    root.mainloop()
