from datetime import datetime
import calendar
import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt

# Global variable to store the username
current_username = ""

def show_signup():
    login_button.pack_forget()
    signup_frame.pack()

def show_login():
    signup_button.pack_forget()
    login_frame.pack()

def sign_up():
    global current_username  # Use the global keyword
    username = signup_username_entry.get()
    password = signup_password_entry.get()
    confirm_password = signup_confirm_password_entry.get()
    initial_balance = signup_balance_entry.get()

    if username and password and confirm_password and initial_balance:
        if password == confirm_password:
            with open("login_details.txt", "a") as file:
                file.write(username + "," + password + "," + initial_balance + "\n")
            current_username = username  # Store the username
            show_dashboard(float(initial_balance))
        else:
            messagebox.showerror("Error", "Passwords do not match.")
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def log_in():
    global current_username  # Use the global keyword
    username = login_username_entry.get()
    password = login_password_entry.get()

    if username and password:
        with open("login_details.txt", "r") as file:
            for line in file:
                stored_username, stored_password, balance = line.strip().split(",")
                if stored_username == username and stored_password == password:
                    current_username = username  # Store the username
                    show_dashboard(float(balance))
                    return
        messagebox.showerror("Error", "Invalid username or password.")
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def add_income():
    global current_username  # Use the global keyword
    income = float(simpledialog.askstring("Add Income", "Enter the amount of income:"))
    if income:
        with open("login_details.txt", "r") as file:
            lines = file.readlines()

        with open("login_details.txt", "w") as file:
            for line in lines:
                stored_username, stored_password, balance = line.strip().split(",")
                if stored_username == current_username:
                    balance = str(float(balance) + income)
                file.write(stored_username + "," + stored_password + "," + balance + "\n")

        balance_label.configure(text="Current Balance: $" + balance)

def add_expense():
    global current_username
    description = simpledialog.askstring("Add Expense", "Enter the description of the expense:")
    amount = simpledialog.askfloat("Add Expense", "Enter the amount of the expense:")
    if description and amount:
        with open("login_details.txt", "r") as file:
            lines = file.readlines()

        with open("login_details.txt", "w") as file:
            for line in lines:
                stored_username, stored_password, balance = line.strip().split(",")
                if stored_username == current_username:
                    balance = str(float(balance) - amount)
                file.write(stored_username + "," + stored_password + "," + balance + "\n")

        balance_label.configure(text="Current Balance: $" + balance)

        with open(current_username + "_expenses.txt", "a") as file:
            file.write(description + "," + str(amount) + "\n")

        # Check if it's a bill expense
        if description.lower() in ["electricity", "maintenance"]:
            now = datetime.now()
            month = now.month
            year = now.year
            month_name = calendar.month_name[month]
            bill_filename = current_username + "_" + str(year) + "_" + month_name.lower() + "_bills.txt"
            with open(bill_filename, "a") as bill_file:
                bill_file.write(description + "," + str(amount) + "\n")

        messagebox.showinfo("Expense Added", "Expense added successfully.")
    else:
        messagebox.showerror("Error", "Please enter both description and amount of the expense.")


def view_expenses():
    global current_username  # Use the global keyword
    try:
        with open(current_username + "_expenses.txt", "r") as file:
            expenses = file.readlines()

        if expenses:
            expense_list = ""
            for expense in expenses:
                description, amount = expense.strip().split(",")
                expense_list += "Description: " + description + "\nAmount: $" + amount + "\n\n"

            messagebox.showinfo("Expenses", expense_list)
        else:
            messagebox.showinfo("Expenses", "No expenses found.")
    except FileNotFoundError:
        messagebox.showinfo("Expenses", "No expenses found.")

def logout():
    global current_username  # Use the global keyword
    current_username = ""  # Clear the stored username
    dashboard_frame.pack_forget()
    login_frame.pack()
    login_button.grid(row=3, column=0, columnspan=2, pady=10)
    signup_button.grid(row=4, column=0, columnspan=2, pady=10)

def show_dashboard(balance):
    login_frame.pack_forget()
    signup_frame.pack_forget()
    welcome_label.configure(text="Welcome, " + current_username + "!")
    balance_label.configure(text="Current Balance: $ " + str(balance))
    income_button.pack()
    expense_button.pack()
    expenses_button.pack()
    goal_settings_button.pack()
    visualization_button.pack()
    tax_planning_button.pack()
    logout_button.pack()
    dashboard_frame.pack()

def goal_settings():
    goal_settings_window = tk.Toplevel(root)
    goal_settings_window.title("Goal Settings")
    goal_settings_window.geometry("400x300")  # Set window dimensions

    add_goal_button = tk.Button(goal_settings_window, text="Add Goal", command=add_goal)
    view_goals_button = tk.Button(goal_settings_window, text="View Goals", command=view_goals)
    remove_goal_button = tk.Button(goal_settings_window, text="Remove Goal", command=remove_goal)
    visualize_goals_button = tk.Button(goal_settings_window, text="Visualize Goals", command=visualize_goals)

    add_goal_button.pack(pady=10)
    view_goals_button.pack(pady=10)
    remove_goal_button.pack(pady=10)
    visualize_goals_button.pack(pady=10)
def visualize_goals():
    global current_username  # Use the global keyword
    try:
        with open(current_username + "_goals.txt", "r") as file:
            goals = file.readlines()

        if goals:
            goal_amounts = []
            goal_descriptions = []
            for goal in goals:
                description, amount = goal.strip().split(",")
                goal_descriptions.append(description)
                goal_amounts.append(float(amount))

            # Create a bar plot of the goals
            plt.figure(figsize=(8, 6))
            plt.barh(goal_descriptions, goal_amounts)
            plt.xlabel("Amount")
            plt.ylabel("Description")
            plt.title("Goals Progress")

            # Display the plot
            plt.show()
        else:
            messagebox.showinfo("Goals", "No goals found.")
    except FileNotFoundError:
        messagebox.showinfo("Goals", "No goals found.")


def view_goals():
    global current_username  # Use the global keyword
    try:
        with open(current_username + "_goals.txt", "r") as file:
            goals = file.readlines()

        if goals:
            goal_list = ""
            for goal in goals:
                description, amount = goal.strip().split(",")
                goal_list += "Description: " + description + "\nAmount: $ " + amount + "\n\n"

            messagebox.showinfo("Goals", goal_list)
        else:
            messagebox.showinfo("Goals", "No goals found.")
    except FileNotFoundError:
        messagebox.showinfo("Goals", "No goals found.")

def remove_goal():
    global current_username  # Use the global keyword
    description = simpledialog.askstring("Remove Goal", "Enter the description of the goal to remove:")
    if description:
        with open(current_username + "_goals.txt", "r") as file:
            goals = file.readlines()

        with open(current_username + "_goals.txt", "w") as file:
            goal_found = False
            for goal in goals:
                goal_description, _ = goal.strip().split(",")
                if goal_description == description:
                    goal_found = True
                else:
                    file.write(goal)

        if goal_found:
            messagebox.showinfo("Goal Removed", "Goal removed successfully.")
        else:
            messagebox.showerror("Error", "Goal not found.")
    else:
        messagebox.showerror("Error", "Please enter the description of the goal to remove.")

def add_goal():
    global current_username  # Use the global keyword
    description = simpledialog.askstring("Add Goal", "Enter the description of the goal:")
    amount = simpledialog.askstring("Add Goal", "Enter the amount of the goal:")
    if description and amount:
        with open(current_username + "_goals.txt", "a") as file:
            file.write(description + "," + amount + "\n")
        messagebox.showinfo("Goal Added", "Goal added successfully.")
    else:
        messagebox.showerror("Error", "Please enter both description and amount of the goal.")


def view_bills():
    global current_username  # Use the global keyword
    now = datetime.now()
    month = now.month
    year = now.year
    month_name = calendar.month_name[month]
    bill_filename = current_username + "_" + str(year) + "_" + month_name.lower() + "_bills.txt"

    try:
        with open(bill_filename, "r") as file:
            bills = file.readlines()

        if bills:
            bill_list = ""
            for bill in bills:
                description, amount = bill.strip().split(",")
                bill_list += "Description: " + description + "\nAmount: $" + amount + "\n\n"

            messagebox.showinfo("Bills", bill_list)
        else:
            messagebox.showinfo("Bills", "No bills found.")
    except FileNotFoundError:
        messagebox.showinfo("Bills", "No bills found.")

def visualize_data():
    global current_username  # Use the global keyword
    try:
        with open(current_username + "_expenses.txt", "r") as file:
            expenses = file.readlines()

        if expenses:
            expense_amounts = []
            expense_descriptions = []
            for expense in expenses:
                description, amount = expense.strip().split(",")
                expense_descriptions.append(description)
                expense_amounts.append(float(amount))

            plt.bar(expense_descriptions, expense_amounts)
            plt.xlabel("Expense Description")
            plt.ylabel("Expense Amount ($)")
            plt.title("Expense Tracking")
            plt.xticks(rotation=45)
            plt.show()
        else:
            messagebox.showinfo("Data Visualization", "No expenses found.")
    except FileNotFoundError:
        messagebox.showinfo("Data Visualization", "No expenses found.")

def plan_tax():
    global current_username
    try:
        with open(current_username + "_expenses.txt", "r") as file:
            expenses = file.readlines()

        if expenses:
            total_expenses = 0
            for expense in expenses:
                _, amount = expense.strip().split(",")
                total_expenses += float(amount)

            with open("login_details.txt", "r") as file:
                lines = file.readlines()

            with open("login_details.txt", "w") as file:
                for line in lines:
                    stored_username, stored_password, balance = line.strip().split(",")
                    if stored_username == current_username:
                        income = float(balance) - total_expenses
                        tax_to_pay = income * 0.1  # Assume 10% tax rate
                        balance = str(income - tax_to_pay)
                    file.write(stored_username + "," + stored_password + "," + balance + "\n")

            messagebox.showinfo("Tax Planning", "Total Expenses: $ " + str(total_expenses) +
                                "\nTax to Pay (10% of Income): $ " + str(tax_to_pay))
            balance_label.configure(text="Current Balance: $ " + balance)
        else:
            messagebox.showinfo("Tax Planning", "No expenses found.")
    except FileNotFoundError:
        messagebox.showinfo("Tax Planning", "No expenses found.")


root = tk.Tk()
root.title("Personal Budget Software")
root.geometry("400x300")  # Set window dimensions
root.configure(bg='#e6e6e6')  # Set background color

# Create a style for buttons
button_style = "raised"
button_bg_color = "#4CAF50"  # Green color
button_fg_color = "white"
button_font = ("Helvetica", 10, "bold")

# Login and Signup buttons
login_button = tk.Button(root, text="Log In", command=show_login, bg=button_bg_color, fg=button_fg_color,
                         relief=button_style, font=button_font)
login_button.pack(pady=10)

signup_button = tk.Button(root, text="Sign Up", command=show_signup, bg=button_bg_color, fg=button_fg_color,
                          relief=button_style, font=button_font)
signup_button.pack(pady=10)

# Sign up frame
signup_frame = tk.Frame(root)

signup_label = tk.Label(signup_frame, text="<< Sign Up >>", font=("Helvetica", 16))
signup_label.grid(row=0, column=0, columnspan=2, pady=10)

signup_username_label = tk.Label(signup_frame, text="Username:")
signup_username_label.grid(row=1, column=0)

signup_username_entry = tk.Entry(signup_frame)
signup_username_entry.grid(row=1, column=1)

signup_password_label = tk.Label(signup_frame, text="Password:")
signup_password_label.grid(row=2, column=0)

signup_password_entry = tk.Entry(signup_frame, show="*")
signup_password_entry.grid(row=2, column=1)

signup_confirm_password_label = tk.Label(signup_frame, text="Confirm Password:")
signup_confirm_password_label.grid(row=3, column=0)

signup_confirm_password_entry = tk.Entry(signup_frame, show="*")
signup_confirm_password_entry.grid(row=3, column=1)

signup_balance_label = tk.Label(signup_frame, text="Initial Balance:")
signup_balance_label.grid(row=4, column=0)

signup_balance_entry = tk.Entry(signup_frame)
signup_balance_entry.grid(row=4, column=1)

signup_button = tk.Button(signup_frame, text="Sign Up", command=sign_up)
signup_button.grid(row=5, column=0, columnspan=2, pady=10)

# Login frame
login_frame = tk.Frame(root)

login_label = tk.Label(login_frame, text="<< Log In >>", font=("Helvetica", 16))
login_label.grid(row=0, column=0, columnspan=2, pady=10)

login_username_label = tk.Label(login_frame, text="Username:")
login_username_label.grid(row=1, column=0)

login_username_entry = tk.Entry(login_frame)
login_username_entry.grid(row=1, column=1)

login_password_label = tk.Label(login_frame, text="Password:")
login_password_label.grid(row=2, column=0)

login_password_entry = tk.Entry(login_frame, show="*")
login_password_entry.grid(row=2, column=1)

login_button = tk.Button(login_frame, text="Log In", command=log_in)
login_button.grid(row=3, column=0, columnspan=2, pady=10)

# Dashboard frame
dashboard_frame = tk.Frame(root, bg='#e6e6e6')  # Set background color

label_font = ("Helvetica", 12, "bold")

welcome_label = tk.Label(dashboard_frame, text="Welcome,", font=label_font, bg='#e6e6e6')
welcome_label.pack(pady=10)

balance_label = tk.Label(dashboard_frame, text="Current Balance:", font=label_font, bg='#e6e6e6')
balance_label.pack()

dashboard_button_font = ("Helvetica", 10, "bold")

income_button = tk.Button(dashboard_frame, text="Add Income", command=add_income, bg=button_bg_color,
                         fg=button_fg_color, relief=button_style, font=dashboard_button_font)
income_button.pack()
expense_button = tk.Button(dashboard_frame, text="Add Expense", command=add_expense, bg=button_bg_color,
                         fg=button_fg_color, relief=button_style, font=dashboard_button_font)
expense_button.pack()
expenses_button = tk.Button(dashboard_frame, text="View Expenses", command=view_expenses, bg=button_bg_color,
                         fg=button_fg_color, relief=button_style, font=dashboard_button_font)
expenses_button.pack()
goal_settings_button = tk.Button(dashboard_frame, text="Goal settings", command=goal_settings, bg=button_bg_color,
                         fg=button_fg_color, relief=button_style, font=dashboard_button_font)
goal_settings_button.pack()
visualization_button = tk.Button(dashboard_frame, text="Visualize Data", command=visualize_data, bg=button_bg_color,
                         fg=button_fg_color, relief=button_style, font=dashboard_button_font)
visualization_button.pack()
tax_planning_button = tk.Button(dashboard_frame, text="Tax planning", command=plan_tax, bg=button_bg_color,
                         fg=button_fg_color, relief=button_style, font=dashboard_button_font)
tax_planning_button.pack()
logout_button = tk.Button(dashboard_frame, text="Logout", command=logout, bg=button_bg_color,
                         fg=button_fg_color, relief=button_style, font=dashboard_button_font)
logout_button.pack()
#income_button = tk.Button(dashboard_frame, text="Add Income", command=add_income)
#expense_button = tk.Button(dashboard_frame, text="Add Expense", command=add_expense)
#Expenses_button = tk.Button(dashboard_frame, text="View Expenses", command=view_expenses)
#goal_settings_button = tk.Button(dashboard_frame, text="Goal Settings", command=goal_settings)
#visualization_button = tk.Button(dashboard_frame, text="Visualize Data", command=visualize_data)
#tax_planning_button = tk.Button(dashboard_frame, text="Plan Tax", command=plan_tax)
#logout_button = tk.Button(dashboard_frame, text="Logout", command=logout) 

root.mainloop()
