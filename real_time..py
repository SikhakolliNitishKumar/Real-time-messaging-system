import tkinter as tk
from tkinter import messagebox
from collections import defaultdict
import time

# Trie Node Definition
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

# Trie for Autocomplete Feature
class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_end_of_word = True

    def search(self, prefix):
        current = self.root
        for char in prefix:
            if char not in current.children:
                return []  # No suggestions if prefix isn't found
            current = current.children[char]
        return self._autocomplete_from_node(current, prefix)
    
    def _autocomplete_from_node(self, node, prefix):
        suggestions = []
        if node.is_end_of_word:
            suggestions.append(prefix)
        
        for char, next_node in node.children.items():
            suggestions.extend(self._autocomplete_from_node(next_node, prefix + char))
        
        return suggestions

# Messaging App with User Registration and Login
class RealTimeMessagingApp:
    def __init__(self):
        self.users = {}  # Store users
        self.passwords = {}  # Store passwords
        self.messages = defaultdict(list)  # Store messages for each user
        self.trie = Trie()  # Initialize Trie for usernames
    
    def register_user(self, username, password):
        if username in self.users:
            return False  # Username already exists
        self.users[username] = username
        self.passwords[username] = password
        self.trie.insert(username)  # Insert username into the Trie
        return True

    def login_user(self, username, password):
        if username in self.users and self.passwords[username] == password:
            return True
        return False

    def send_message(self, from_user, to_user, message):
        if to_user not in self.users:
            return False  # Recipient does not exist
        
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        full_message = f"From: {from_user} | Time: {timestamp} | Message: {message}"
        self.messages[to_user].append(full_message)  # Store message for the recipient
        return True

    def receive_messages(self, username):
        if username not in self.messages or not self.messages[username]:
            return ["No new messages."]
        return self.messages[username]  # Return messages sent to the logged-in user
    
    def autocomplete_users(self, prefix):
        return self.trie.search(prefix)  # Get autocomplete suggestions

# Tkinter GUI for Messaging App
class MessagingAppWindow:
    def __init__(self, root, messaging_app):
        self.messaging_app = messaging_app
        self.logged_in_user = None

        # Main Window Setup
        self.root = root
        self.root.title("Real-Time Messaging App")
        self.root.geometry("600x400")  # Adjusted window size
        self.root.configure(bg='#E8F6EF')  # Light background color

        # Fonts and styles
        self.title_font = ('Helvetica', 16, 'bold')
        self.label_font = ('Helvetica', 12)
        self.button_font = ('Helvetica', 10)

        # Login/Register Frame
        self.login_frame = tk.Frame(root, bg='#E8F6EF')
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Username:", font=self.label_font, bg='#E8F6EF').grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.login_frame, text="Password:", font=self.label_font, bg='#E8F6EF').grid(row=1, column=0, padx=10, pady=10)

        self.username_entry = tk.Entry(self.login_frame, font=self.label_font)
        self.password_entry = tk.Entry(self.login_frame, show="*", font=self.label_font)

        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.login_frame, text="Login", command=self.login, font=self.button_font, bg='#A3E4D7').grid(row=2, column=0, pady=10)
        tk.Button(self.login_frame, text="Register", command=self.register, font=self.button_font, bg='#A3E4D7').grid(row=2, column=1, pady=10)

        # Messaging Frame (hidden at first)
        self.messaging_frame = tk.Frame(root, bg='#E8F6EF')
        
        # Left Side: Search Users
        self.left_frame = tk.Frame(self.messaging_frame, bg='black', width=200)  # Set width for the left frame
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)  # Fill vertically

        tk.Label(self.left_frame, text="Search Users:", font=self.label_font, bg='black', fg='white').pack(pady=5)
        self.user_search_entry = tk.Entry(self.left_frame, font=self.label_font)
        self.user_search_entry.pack(pady=5)
        self.user_search_entry.bind("<KeyRelease>", self.search_users)  # Bind search key release

        self.user_listbox = tk.Listbox(self.left_frame, width=30, height=15, font=self.label_font, bg='black', fg='white')  # Change listbox colors
        self.user_listbox.pack(pady=5)
        self.user_listbox.bind("<<ListboxSelect>>", self.select_user)  # Bind user selection

        # Right Side: Messaging
        self.right_frame = tk.Frame(self.messaging_frame, bg='#E8F6EF')
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        tk.Label(self.right_frame, text="Recipient:", font=self.label_font, bg='#E8F6EF').grid(row=0, column=0, padx=10, pady=10)
        self.recipient_entry = tk.Entry(self.right_frame, width=30, font=self.label_font)
        self.recipient_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.right_frame, text="Message:", font=self.label_font, bg='#E8F6EF').grid(row=1, column=0, padx=10, pady=10)
        self.message_entry = tk.Entry(self.right_frame, width=30, font=self.label_font)
        self.message_entry.grid(row=1, column=1, padx=10, pady=10)

        # Buttons in a separate frame to keep them visible
        button_frame = tk.Frame(self.right_frame, bg='#E8F6EF')
        button_frame.grid(row=2, columnspan=2, pady=10)

        tk.Button(button_frame, text="Send", command=self.send_message, font=self.button_font, bg='#AED6F1').grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Check Messages", command=self.check_messages, font=self.button_font, bg='#AED6F1').grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Log Out", command=self.logout, font=self.button_font, bg='#F1948A').grid(row=0, column=2, padx=5)

        # Messages Display Area
        self.messages_display = tk.Text(self.right_frame, width=40, height=15, font=self.label_font, bg='white')
        self.messages_display.grid(row=3, columnspan=2, padx=10, pady=10)

        # Set the frame for autocomplete suggestions
        self.autocomplete_listbox = tk.Listbox(self.messaging_frame, width=30, height=5, font=self.label_font)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.messaging_app.login_user(username, password):
            self.logged_in_user = username
            messagebox.showinfo("Login", f"Welcome {username}!")
            self.show_messaging_frame()
            self.update_user_list()  # Update the user list after login
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.messaging_app.register_user(username, password):
            messagebox.showinfo("Registration", "Registration successful!")
        else:
            messagebox.showerror("Registration Failed", "Username already exists.")

    def show_messaging_frame(self):
        self.login_frame.pack_forget()  # Hide login frame
        self.messaging_frame.pack(fill=tk.BOTH, expand=True)  # Show messaging frame

    def update_user_list(self):
        self.user_listbox.delete(0, tk.END)  # Clear current user list
        for user in self.messaging_app.users:
            self.user_listbox.insert(tk.END, user)  # Populate with registered users

    def search_users(self, event):
        prefix = self.user_search_entry.get()
        self.user_listbox.delete(0, tk.END)  # Clear current list
        for user in self.messaging_app.autocomplete_users(prefix):
            self.user_listbox.insert(tk.END, user)  # Populate with suggestions

    def select_user(self, event):
        selected_index = self.user_listbox.curselection()
        if selected_index:
            recipient = self.user_listbox.get(selected_index)
            self.recipient_entry.delete(0, tk.END)  # Clear recipient entry
            self.recipient_entry.insert(0, recipient)  # Insert selected recipient
            self.autocomplete_listbox.place_forget()  # Hide the suggestion box
            
            # Display messages from the selected user
            self.display_user_messages(recipient)

    def display_user_messages(self, user):
        # Only display messages sent to the logged-in user
        messages = self.messaging_app.receive_messages(self.logged_in_user)  # Get messages for the logged-in user
        self.messages_display.delete(1.0, tk.END)  # Clear the text area
        self.messages_display.insert(tk.END, f"Messages for {self.logged_in_user}:\n" + "\n".join(messages))  # Display messages

    def send_message(self):
        recipient = self.recipient_entry.get()
        message = self.message_entry.get()
        if self.messaging_app.send_message(self.logged_in_user, recipient, message):
            messagebox.showinfo("Message Sent", "Your message has been sent.")
            self.message_entry.delete(0, tk.END)  # Clear message entry
            self.display_user_messages(recipient)  # Update displayed messages for the recipient
        else:
            messagebox.showerror("Error", "Failed to send message. Check recipient.")

    def check_messages(self):
        messages = self.messaging_app.receive_messages(self.logged_in_user)
        messagebox.showinfo("Messages", "\n".join(messages))  # Show received messages

    def logout(self):
        self.logged_in_user = None
        self.username_entry.delete(0, tk.END)  # Clear username entry
        self.password_entry.delete(0, tk.END)  # Clear password entry
        self.messaging_frame.pack_forget()  # Hide messaging frame
        self.login_frame.pack(pady=20)  # Show login frame

    def autocomplete_recipients(self, event):
        prefix = self.recipient_entry.get()
        suggestions = self.messaging_app.autocomplete_users(prefix)
        self.autocomplete_listbox.delete(0, tk.END)  # Clear current suggestions
        for user in suggestions:
            self.autocomplete_listbox.insert(tk.END, user)  # Populate with suggestions
        
        # Show suggestions only if there are any
        if suggestions:
            # Place the listbox below the recipient entry
            self.autocomplete_listbox.place(x=self.recipient_entry.winfo_x(), y=self.recipient_entry.winfo_y() + 25)
        else:
            self.autocomplete_listbox.place_forget()  # Hide if no suggestions

# Main Program Execution
if __name__ == "__main__":
    root = tk.Tk()
    messaging_app = RealTimeMessagingApp()
    app_window = MessagingAppWindow(root, messaging_app)

    # Bind the recipient entry for autocomplete
    app_window.recipient_entry.bind("<KeyRelease>", app_window.autocomplete_recipients)

    root.mainloop()
