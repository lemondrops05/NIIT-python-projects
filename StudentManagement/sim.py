# Function to display the load screen
def load_screen():
    # Create the main window
    load_window = tk.Tk()
    load_window.title("Loading")

    # Set the initial size to 6.1-inch display (1080x2400 pixels)
    load_window.geometry("1080x2400")

    # Configure the background color
    load_window.configure(bg='#fff5ff')  # Lighter pink background

    # Load custom font (If Nectarine and Roca One fonts are installed on your system)
    load_window.option_add("*Font", "Nectarine 50")  # Set the font and size

    # Create a frame to center the content
    center_frame = tk.Frame(load_window, bg='#fff5ff')
    center_frame.place(relx=0.5, rely=0.5, anchor='center')

    # Display the loading label
    label = tk.Label(center_frame, text="Welcome...", fg='#f20775', bg='#fff5ff')
    label.pack(pady=(0, 10))  # Reduced padding to bring the label closer to the progress bar

    # Create and style the progress bar
    style = ttk.Style()
    style.configure("TProgressbar",
                    troughcolor='#ff9eff',  # Light pink trough
                    background='#ff6f16',  # Orange progress
                    thickness=80)  # Increase thickness for a thicker bar

    progress_bar = ttk.Progressbar(center_frame, style="TProgressbar", length=800, mode='determinate')
    progress_bar.pack()


    # Function to simulate progress
    def update_progress(value=0):
        if value <= 100:
            progress_bar['value'] = value
            load_window.after(20, update_progress, value + 1)
        else:
            load_window.destroy()
            sign_in_sign_up_page()

    # Start updating the progress bar
    update_progress()

    load_window.mainloop()

# Example users dictionary for demonstration
users = {"user1": "password1", "user2": "password2"}

def sign_in_sign_up_page():
    auth_window = tk.Tk()
    auth_window.title("Sign In/Sign Up")

    # Set the window size
    auth_window.geometry("1080x2400")
    auth_window.configure(bg='#fff5ff')  # Lighter pink background for the entire window

    # Create a center frame with background color
    center_frame = tk.Frame(auth_window, bg='#fff5ff')
    center_frame.place(relx=0.5, rely=0.5, anchor='center')

    # Username label and entry
    tk.Label(center_frame, text="Username", fg='#f20775', bg='#fff5ff', font=("Arial", 20)).grid(row=0, column=0, pady=10)
    username_entry = tk.Entry(center_frame, font=("Arial", 20))
    username_entry.grid(row=0, column=1, pady=10)

    # Password label and entry
    tk.Label(center_frame, text="Password", fg='#f20775', bg='#fff5ff', font=("Arial", 20)).grid(row=1, column=0, pady=10)
    password_entry = tk.Entry(center_frame, show="*", font=("Arial", 20))
    password_entry.grid(row=1, column=1, pady=10)

    # Function to simulate button press effect
    def on_press(button):
        button.configure(bg='#ff6f16')  # Darker orange on press

    def on_release(button, original_color):
        button.configure(bg=original_color)  # Revert to original color

    def sign_in():
        username = username_entry.get()
        password = password_entry.get()
        if users.get(username) == password:
            auth_window.destroy()
            customer_home_page(username)
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def sign_up():
        username = username_entry.get()
        password = password_entry.get()
        if username not in users:
            users[username] = password
            messagebox.showinfo("Success", "Account created successfully")
        else:
            messagebox.showerror("Error", "Username already exists")

    # Sign In button
    sign_in_button = tk.Button(center_frame, text="Sign In", command=sign_in, bg='#f20775', fg='#fff5ff', height=2, width=15, font=("Arial", 20))
    sign_in_button.grid(row=2, column=0, pady=20)
    sign_in_button.bind("<ButtonPress>", lambda event: on_press(sign_in_button))
    sign_in_button.bind("<ButtonRelease>", lambda event: on_release(sign_in_button, '#ff9eff'))

    # Sign Up button
    sign_up_button = tk.Button(center_frame, text="Sign Up", command=sign_up, bg='#f20775', fg='#fff5ff', height=2, width=15, font=("Arial", 20))
    sign_up_button.grid(row=2, column=1, pady=20)
    sign_up_button.bind("<ButtonPress>", lambda event: on_press(sign_up_button))
    sign_up_button.bind("<ButtonRelease>", lambda event: on_release(sign_up_button, '#ff9eff'))

    # Admin Sign In button
    admin_button = tk.Button(center_frame, text="Admin Sign In",
                             command=lambda: messagebox.showinfo("Admin", "Admin Sign In Page"),
                             bg='#ff9eff', fg='#fff5ff', height=2, width=30, font=("Arial", 20))
    admin_button.grid(row=3, column=0, columnspan=2, pady=20)
    admin_button.bind("<ButtonPress>", lambda event: on_press(admin_button))
    admin_button.bind("<ButtonRelease>", lambda event: on_release(admin_button, '#ff9eff'))

    auth_window.mainloop()