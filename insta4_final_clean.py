import tkinter as tk
from tkinter import messagebox
import re 
users = {}
current_user = None
def apply_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg="gray")
    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="gray")
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
def is_valid_username(username):
    username = str(username)
    username = username.lower()
    if len(username)>=3 and len(username)<=20:
        pattern = r"^[a-z][a-z0-9._-]*$" 
        if re.match(pattern,username):
            return True
        else:
            return False
    else:
        return False 
def is_valid_email(email):
    pattern = r"^[a-z0-9][a-z0-9._-]*[a-z0-9]@[a-z0-9][a-z0-9._-]*[a-z0-9]\.[a-z]{2,}$" 
    if re.match(pattern,email):
        return True
    else:
        return False
def is_valid_password(password):
    if len(password)>=5:
        pattern = r"^[A-Za-z0-9@._-][A-Za-z0-9@._-]*$"
        if re.match(pattern,password):
            return True
        else:
            return False
    else:
        return False 
def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()
def show_main_screen():
    clear_screen()
    tk.Label(root, text="Welcome", font=("Arial", 18, "bold")).pack(pady=10)
    tk.Button(root, text="Login", command=login_screen).pack(pady=10)
    tk.Button(root, text="Sign Up", command=sign_up_screen).pack(pady=5)
def login_screen(): 
    clear_screen()
    tk.Label(root, text="Login", font=("Arial", 18, "bold")).pack(pady=10)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)
    apply_placeholder(username_entry, "Username")
    password_entry = tk.Entry(root)
    password_entry.pack(pady=5)
    apply_placeholder(password_entry, "Password")
    tk.Button(root, text="Login", command=lambda: login(username_entry.get(), password_entry.get())).pack(pady=10)
    tk.Button(root, text="Back", command=show_main_screen).pack(pady=5)
def sign_up_screen():
    clear_screen()
    tk.Label(root, text="Sign Up", font=("Arial", 18, "bold")).pack(pady=10)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)
    apply_placeholder(username_entry, "Username")
    email_entry = tk.Entry(root)
    email_entry.pack(pady=5)
    apply_placeholder(email_entry, "Email")
    password_entry = tk.Entry(root)
    password_entry.pack(pady=5)
    apply_placeholder(password_entry, "Password")
    tk.Button(root, text="Sign Up", command=lambda: sign_up(username_entry.get(), email_entry.get(), password_entry.get())).pack(pady=10)
    tk.Button(root, text="Back", command=show_main_screen).pack(pady=5)
def login(username,password):
    global current_user
    for email in users:
        if users[email]["username"]==username and users[email]["password"]==password:
            current_user = email
            show_home_screen()
            return
    messagebox.showerror("Login Error", "Invalid username or password")
def sign_up(username,email,password):
    if not is_valid_username(username):
        messagebox.showerror("Error","Invalid username format!")
        return
    if not is_valid_email(email):
        messagebox.showerror("Error","Invalid email format!") 
        return
    if not is_valid_password(password):
        messagebox.showerror("Error","Invalid password format!")
        return
    if email in users:
        messagebox.showerror("Error","Email already exists!")
        return 
    if username in users:
        messagebox.showerror("Error","Username already exists!")
        return
    if is_valid_username(username) and is_valid_email(email) and is_valid_password(password) and email not in users and username not in users:
        users[email] = { 
        "username": username, 
        "email": email, 
        "password": password, 
        "bio": "", 
        "followers": [], 
        "following": [], 
        "posts": [], 
        "messages": {}, 
        "blocked": [], 
        "private": False, 
        "activities": [], 
        "follow_requests": [], 
        "groups": {}, 
        "saved_posts": []} 
        messagebox.showinfo("Sign Up", "Account created successfully!")
        show_main_screen()
def log_out():
    global current_user
    current_user = None
    show_main_screen()
def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()
def show_home_screen():
    clear_screen()
    tk.Label(root, text="Home", font=("Arial", 18, "bold")).pack(pady=10)
    tk.Button(root, text="View Posts", command=view_feed).pack(pady=5)
    tk.Button(root, text="View Stories", command=view_stories).pack(pady=5)
    tk.Button(root, text="Messages", command=view_messages).pack(pady=5)
    if users[current_user]["private"]:
        tk.Button(root, text="Follow Requests", command=view_follow_requests).pack(pady=5)
    tk.Button(root, text="Profile", command=view_profile).pack(pady=5)
    tk.Button(root, text="Add Post", command=add_post).pack(pady=5)
    tk.Button(root, text="Add Story", command=add_story).pack(pady=5)
    tk.Button(root, text="Search", command=search_user_screen).pack(pady=5)
    tk.Button(root, text="Log Out", command=log_out).pack(pady=10)
def view_follow_requests():
    clear_screen()
    tk.Label(root, text="Follow Requests", font=("Arial", 18, "bold")).pack(pady=10)
    requests = users[current_user].get("follow_requests", [])
    if requests:
        for req in requests:
            tk.Button(root, text=f"Accept {users[req]['username']}", command=lambda r=req: accept_follow_request(r)).pack(pady=5)
    else:
        tk.Label(root, text="No follow requests.").pack(pady=5)
    tk.Button(root, text="Back", command=show_home_screen).pack(pady=5)
def accept_follow_request(email):
    users[current_user]["follow_requests"].remove(email)
    users[current_user]["followers"].append(email)
    users[email]["following"].append(current_user)
    messagebox.showinfo("Accept", f"You accepted {users[email]['username']}")
    view_follow_requests()
def search_user_screen():
    clear_screen()
    tk.Label(root, text="Search User", font=("Arial", 18, "bold")).pack(pady=10)
    search_entry = tk.Entry(root)
    search_entry.pack(pady=5)
    apply_placeholder(search_entry, "Enter Username")
    tk.Button(root, text="Search", command=lambda: search_user(search_entry.get())).pack(pady=5)
    tk.Button(root, text="Back", command=show_home_screen).pack(pady=5)
def search_user(username):
    user_email = next((email for email, user in users.items() if user["username"] == username and current_user not in user["blocked"]), None)
    if user_email:
        view_other_profile(user_email)
    else:
        messagebox.showerror("Error", "User not found or you are blocked!")
def view_user_posts(user_email):
    clear_screen()
    user = users[user_email]
    tk.Label(root, text=f"{user['username']}'s Posts", font=("Arial", 18, "bold")).pack(pady=10)
    if user["private"] and current_user not in user["followers"] and user_email != current_user:
        tk.Label(root, text="This account is private.").pack(pady=5)
    else:
        for post in user["posts"]:
            tk.Button(root, text=post["content"], command=lambda p=post: view_post_details(p, user_email)).pack(pady=5)
    tk.Button(root, text="Back", command=lambda: view_other_profile(user_email) if user_email != current_user else view_profile()).pack(pady=5)
def view_other_profile(user_email):
    clear_screen()
    user = users[user_email]
    tk.Label(root, text=f"Profile: {user['username']}", font=("Arial", 18, "bold")).pack(pady=10)
    tk.Label(root, text=f"Bio: {user['bio']}").pack(pady=5)
    tk.Label(root, text=f"Followers: {len(user['followers'])}").pack(pady=5)
    tk.Label(root, text=f"Following: {len(user['following'])}").pack(pady=5)
    if user["private"] and current_user not in user["followers"]:
        tk.Label(root, text="This account is private.").pack(pady=10)
        if current_user not in user["follow_requests"]:
            tk.Button(root, text="Send Follow Request", command=lambda: send_follow_request(user_email)).pack(pady=5)
        else:
            tk.Label(root, text="Follow request sent.").pack(pady=5)
    else:
        tk.Button(root, text="View Posts", command=lambda: view_user_posts(user_email)).pack(pady=5)
        tk.Button(root, text="View Stories", command=lambda: view_user_stories(user_email)).pack(pady=5)
        if user_email not in users[current_user]["blocked"]:
            if user_email in users[current_user]["following"]:
                tk.Button(root, text="Unfollow", command=lambda: follow_user(user_email)).pack(pady=5)
            else:
                tk.Button(root, text="Follow", command=lambda: follow_user(user_email)).pack(pady=5)
            tk.Button(root, text="Send Message", command=lambda: open_chat_window(user_email)).pack(pady=5)
            tk.Button(root, text="Block User", command=lambda: block_user(user_email)).pack(pady=5)
    tk.Button(root, text="Back", command=search_user_screen).pack(pady=5)
def follow_user(email):
    if email in users[current_user]["following"]:
        users[current_user]["following"].remove(email) 
        users[email]["followers"].remove(current_user)
        messagebox.showinfo("Unfollow","Unfollow successfully!") 
    elif users[email]["private"]==True:
        send_follow_request(email)
    else:
        users[current_user]["following"].append(email)
        users[email]["followers"].append(current_user)
        messagebox.showinfo("Follow","Follow successfully!") 
def send_follow_request(email):
    if  current_user in users[email]["follow_requests"]:
        messagebox.showerror("Error","Follow request already sent")
    else:
        users[email]["follow_requests"].append(current_user)
        messagebox.showinfo("Follow request","Send successfully!") 
def block_user(email):
    if email in users[current_user]["followers"]:
        users[current_user]["followers"].remove(email)
        users[email]["following"].remove(current_user)
    if current_user in users[email]["followers"]:
        users[email]["followers"].remove(current_user)
        users[current_user]["following"].remove(email)
    if email in users[current_user]["messages"]:
        del users[current_user]["messages"][email]
    if current_user in users[email]["messages"]:
        del users[email]["messages"][current_user]
    users[current_user]["blocked"].append(email) 
    messagebox.showinfo("Block", f"You blocked {users[email]['username']}")
    show_home_screen()
def unblock_user(email):
    users[current_user]["blocked"].remove(email)
    messagebox.showinfo("Unblocked", f"You unblocked {users[email]['username']}")
    view_blocked_accounts()
def view_blocked_accounts():
    clear_screen()
    tk.Label(root, text="Blocked Accounts", font=("Arial", 18, "bold")).pack(pady=10)
    blocked_users = users[current_user]["blocked"]
    if blocked_users:
        for blocked in blocked_users:
            tk.Button(root, text=f"Unblock {users[blocked]['username']}", command=lambda b=blocked: unblock_user(b)).pack(pady=5)
    else:
        tk.Label(root, text="No blocked users.").pack(pady=5)
    tk.Button(root, text="Back", command=view_profile).pack(pady=5)
def edit_profile():
    clear_screen()
    tk.Label(root, text="Edit Profile", font=("Arial", 18, "bold")).pack(pady=10)
    new_username_entry = tk.Entry(root)
    new_username_entry.pack(pady=5)
    apply_placeholder(new_username_entry, "New Username")
    new_bio_entry = tk.Entry(root)
    new_bio_entry.pack(pady=5)
    apply_placeholder(new_bio_entry, "New Bio")
    new_password_entry = tk.Entry(root)
    new_password_entry.pack(pady=5)
    apply_placeholder(new_password_entry, "New Password")
    privacy_var = tk.StringVar(value="Private" if users[current_user]["private"] else "Public")
    privacy_option = tk.OptionMenu(root, privacy_var, "Public", "Private")
    privacy_option.pack(pady=5)
    tk.Button(root, text="Save", command=lambda: save_profile(new_username_entry.get(), new_bio_entry.get(), new_password_entry.get(), privacy_var.get())).pack(pady=5)
    tk.Button(root, text="Back", command=view_profile).pack(pady=5)
def save_profile(username, bio, password, privacy_status):
    if username and not is_valid_username(username):
        messagebox.showerror("Error", "Username must be at least 5 characters and only contain lowercase letters, _ or .")
        return
    if password and not is_valid_password(password):
        messagebox.showerror("Error", "Password must be at least 8 characters.")
        return
    if username:
        users[current_user]["username"] = username
    if bio:
        users[current_user]["bio"] = bio
    if password:
        users[current_user]["password"] = password
    users[current_user]["private"] = True if privacy_status == "Private" else False
    messagebox.showinfo("Success", "Profile updated successfully!")
    view_profile()
def view_profile():
    clear_screen()
    user = users[current_user]
    tk.Label(root, text=f"Profile: {user['username']}", font=("Arial", 18, "bold")).pack(pady=10)
    tk.Label(root, text=f"Bio: {user['bio']}").pack(pady=5)
    tk.Label(root, text=f"Followers: {len(user['followers'])}").pack(pady=5)
    tk.Label(root, text=f"Following: {len(user['following'])}").pack(pady=5)
    tk.Button(root, text="Edit Profile", command=edit_profile).pack(pady=5)
    tk.Button(root, text="View Posts", command=lambda: view_user_posts(current_user)).pack(pady=5)
    tk.Button(root, text="View Stories", command=lambda: view_user_stories(current_user)).pack(pady=5)
    tk.Button(root, text="View Blocked Accounts", command=view_blocked_accounts).pack(pady=5)
    tk.Button(root, text="Saved", command=view_saved_posts).pack(pady=5)  # دکمه نمایش پست‌های ذخیره‌شده اضافه شد
    tk.Button(root, text="Back", command=show_home_screen).pack(pady=5)
def view_saved_posts():
    clear_screen()
    tk.Label(root, text="Saved Posts", font=("Arial", 18, "bold")).pack(pady=10)
    saved_posts = users[current_user].get("saved_posts", [])
    if saved_posts:
        for post in saved_posts:
            tk.Button(root, text=post["content"], command=lambda p=post: view_post_details(p, next(email for email, user in users.items() if p in user["posts"]))).pack(pady=5)
    else:
        tk.Label(root, text="No saved posts.").pack(pady=5)
    tk.Button(root, text="Back", command=view_profile).pack(pady=5)
def save_post_to_favorites(post):
    if post not in users[current_user]["saved_posts"]:
        post["saved_by"].append(current_user)
        users[current_user]["saved_posts"].append(post)
        messagebox.showinfo("Save","Save successfully!") 
    else:
        post["saved_by"].remove(current_user)
        users[current_user]["saved_post"].remove(post)
        messagebox.showinfo("Delete","Delete successfully!") 
def add_post():
    clear_screen()
    tk.Label(root, text="New Post", font=("Arial", 18, "bold")).pack(pady=10)
    post_entry = tk.Entry(root)
    post_entry.pack(pady=5)
    apply_placeholder(post_entry, "Write your post...")
    tk.Button(root, text="Post", command=lambda: save_post(post_entry.get())).pack(pady=5)
    tk.Button(root, text="Back", command=show_home_screen).pack(pady=5)
def save_post(content):
    if content.strip():
        post = {"content": content, "likes": [], "comments": [], "saved_by": []}
        users[current_user]["posts"].append(post)
        users[current_user]["activities"].append("You added a new post")
        messagebox.showinfo("Success", "Post added successfully!")
        view_user_posts(current_user)
    else:
        messagebox.showerror("Error", "Post content cannot be empty!")
def like_post(post):
    if current_user in post["likes"]:
        post["likes"].remove(current_user)
    else:
        post["likes"].append(current_user)
def view_post_details(post, user_email):
    clear_screen()
    tk.Label(root, text=f"Post by {users[user_email]['username']}", font=("Arial", 18, "bold")).pack(pady=10)
    tk.Label(root, text=post["content"]).pack(pady=5)
    tk.Label(root, text=f"Likes: {len(post['likes'])}").pack(pady=5)
    tk.Label(root, text=f"Comments: {len(post['comments'])}").pack(pady=5)
    tk.Label(root, text=f"Saved by: {len(post.get('saved_by', []))} users").pack(pady=5)  
    tk.Button(root, text="Like", command=lambda: like_post(post)).pack(pady=5)
    tk.Button(root, text="Comment", command=lambda: comment_on_post(post)).pack(pady=5)
    tk.Button(root, text="View Comments", command=lambda: view_comments(post)).pack(pady=5)  
    tk.Button(root, text="Save", command=lambda: save_post_to_favorites(post)).pack(pady=5)  
    tk.Button(root, text="Share", command=lambda: share_post(post)).pack(pady=5)  
    tk.Button(root, text="Back", command=lambda: view_user_posts(user_email)).pack(pady=5)
def share_post(post):
    clear_screen()
    tk.Label(root, text="Share Post", font=("Arial", 18, "bold")).pack(pady=10)
    search_entry = tk.Entry(root)
    search_entry.pack(pady=5)
    apply_placeholder(search_entry, "Enter username or group name")
    tk.Button(root, text="Search", command=lambda: search_and_share_post(post, search_entry.get())).pack(pady=5)
    tk.Button(root, text="Back", command=lambda: view_post_details(post, next(email for email, user in users.items() if post in user["posts"]))).pack(pady=5)
def search_and_share_post(post, target):
    target_email = next((email for email, user in users.items() if user["username"] == target), None)
    if target_email:
        if target_email not in users[current_user]["messages"]:
            users[current_user]["messages"][target_email] = []
        if current_user not in users[target_email]["messages"]:
            users[target_email]["messages"][current_user] = []
        users[current_user]["messages"][target_email].append((current_user, f"Shared Post: {post['content']}"))
        users[target_email]["messages"][current_user].append((current_user, f"Shared Post: {post['content']}"))
        messagebox.showinfo("Success", f"Post shared with {target}")
    else:
        messagebox.showerror("Error", "User not found!")
    show_home_screen()
def view_comments(post):
    clear_screen()
    tk.Label(root, text="Comments", font=("Arial", 18, "bold")).pack(pady=10)
    if post["comments"]:
        for user, comment in post["comments"]:
            tk.Label(root, text=f"{users[user]['username']}: {comment}").pack(pady=5)
    else:
        tk.Label(root, text="No comments yet").pack(pady=5)
    tk.Button(root, text="Back", command=lambda: view_post_details(post, next(email for email, user in users.items() if post in user["posts"]))).pack(pady=5)
def comment_on_post(post):
    clear_screen()
    tk.Label(root, text="Comment on Post", font=("Arial", 18, "bold")).pack(pady=10)
    comment_entry = tk.Entry(root)
    comment_entry.pack(pady=5)
    apply_placeholder(comment_entry, "Write a comment...")
    tk.Button(root, text="Comment", command=lambda: save_post_comment(post, comment_entry.get())).pack(pady=5)
    tk.Button(root, text="Back", command=lambda: view_post_details(post, next(email for email, user in users.items() if post in user["posts"]))).pack(pady=5)
def save_post_comment(post, comment):
    if comment.strip():
        post["comments"].append((current_user, comment))
        users[current_user]["activities"].append("You commented on a post")
        messagebox.showinfo("Success", "Comment added!")
    else:
        messagebox.showerror("Error", "Comment cannot be empty!")
    view_comments(post)
def add_story():
    clear_screen()
    tk.Label(root, text="New Story", font=("Arial", 18, "bold")).pack(pady=10)
    story_entry = tk.Entry(root)
    story_entry.pack(pady=5)
    apply_placeholder(story_entry, "Write your story...")
    tk.Button(root, text="Story", command=lambda: save_story(story_entry.get())).pack(pady=5)
    tk.Button(root, text="Back", command=show_home_screen).pack(pady=5)
def save_story(content):
    if content.strip():
        story = {"content": content, "likes": []}
        users[current_user].setdefault("stories", []).append(story)
        users[current_user]["activities"].append("You added a new story")
        messagebox.showinfo("Success", "Story added successfully!")
        view_user_stories(current_user)
    else:
        messagebox.showerror("Error", "Story content cannot be empty!")
def view_user_stories(user_email):
    clear_screen()
    user = users[user_email]
    tk.Label(root, text=f"{user['username']}'s Stories", font=("Arial", 18, "bold")).pack(pady=10)
    if "stories" in user and user["stories"]:
        for story in user["stories"]:
            tk.Button(root, text=story["content"], command=lambda s=story: view_story_details(s, user_email)).pack(pady=5)
    else:
        tk.Label(root, text="No stories available.").pack(pady=5)
    tk.Button(root, text="Back", command=lambda: view_other_profile(user_email) if user_email != current_user else view_profile()).pack(pady=5)
def view_story_details(story, user_email):
    clear_screen()
    tk.Label(root, text=f"Story by {users[user_email]['username']}", font=("Arial", 18, "bold")).pack(pady=10)
    tk.Label(root, text=story["content"]).pack(pady=5)
    tk.Label(root, text=f"Likes: {len(story['likes'])}").pack(pady=5)
    tk.Button(root, text="Like", command=lambda: like_story(story)).pack(pady=5)
    tk.Button(root, text="Back", command=lambda: view_user_stories(user_email)).pack(pady=5)
def like_story(story):
    if current_user in story["likes"]:
        story["likes"].remove(current_user)
        messagebox.showinfo("D like","You do not like this story")
    else:
        story["likes"].append(current_user) 
        messagebox.showinfo("Like","You like this story") 
def view_stories():
    clear_screen()
    tk.Label(root, text="Stories Feed", font=("Arial", 18, "bold")).pack(pady=10)
    for user_email in users[current_user]["following"]:
        if "stories" in users[user_email] and users[user_email]["stories"]:
            tk.Button(root, text=f"View {users[user_email]['username']}'s Stories", command=lambda u=user_email: view_user_stories(u)).pack(pady=5)
    tk.Button(root, text="Back", command=show_home_screen).pack(pady=5)
def view_feed():
    clear_screen()
    tk.Label(root, text="Home Feed", font=("Arial", 18, "bold")).pack(pady=10)
    for user_email in users[current_user]["following"]:
        if not users[user_email]["private"] or current_user in users[user_email]["followers"]:
            for post in users[user_email]["posts"]:
                tk.Button(root, text=post["content"], command=lambda p=post: view_post_details(p, user_email)).pack(pady=5)
        else:
            tk.Label(root, text=f"{users[user_email]['username']}'s account is private.").pack(pady=5)
    tk.Button(root, text="Back", command=show_home_screen).pack(pady=5)
def send_chat_message(chat_user_email, message):
    if message.strip():
        if chat_user_email not in users[current_user]["messages"]:
            users[current_user]["messages"][chat_user_email] = []
        if current_user not in users[chat_user_email]["messages"]:
            users[chat_user_email]["messages"][current_user] = []
        users[current_user]["messages"][chat_user_email].append((current_user, message))
        users[chat_user_email]["messages"][current_user].append((current_user, message))
        open_chat_window(chat_user_email)
    else:
        messagebox.showerror("Error", "Message cannot be empty!")
def open_chat_window(chat_user_email):
    clear_screen()
    tk.Label(root, text=f"Chat with {users[chat_user_email]['username']}", font=("Arial", 18, "bold")).pack(pady=10)
    chat_frame = tk.Frame(root)
    chat_frame.pack(pady=10)
    chat_messages = users[current_user]["messages"].get(chat_user_email, [])
    if not chat_messages:
        tk.Label(chat_frame, text="No messages yet.").pack(pady=5)
    for sender, message in chat_messages:
        sender_name = "You" if sender == current_user else users[sender]["username"]
        tk.Label(chat_frame, text=f"{sender_name}: {message}").pack(pady=2, anchor="w" if sender == current_user else "e")
    message_entry = tk.Entry(root)
    message_entry.pack(pady=5)
    apply_placeholder(message_entry, "Type a message...")
    tk.Button(root, text="Send", command=lambda: send_chat_message(chat_user_email, message_entry.get())).pack(pady=5)
    tk.Button(root, text="Back", command=view_messages).pack(pady=5)
def view_messages():
    clear_screen()
    tk.Label(root, text="Messages", font=("Arial", 18, "bold")).pack(pady=10)
    chat_users = set(users[current_user]["messages"].keys())
    chat_groups = users[current_user].get("groups", {})
    for user in chat_users:
        tk.Button(root, text=users[user]["username"], command=lambda u=user: open_chat_window(u)).pack(pady=5)
    for group_name in chat_groups:
        tk.Button(root, text=f"Group: {group_name}", command=lambda g=group_name: open_group_chat(g)).pack(pady=5)
    tk.Button(root, text="Add Group", command=add_group).pack(pady=5)
    tk.Button(root, text="Back", command=show_home_screen).pack(pady=5)
def send_group_message(group_name, message):
    if not message.strip():
        messagebox.showerror("Error", "Message cannot be empty!")
        return
    group_data = users[current_user]["groups"][group_name]
    if group_data:
        new_message = (current_user, message)
        group_data["messages"].append(new_message)
        for member in group_data["members"]:
            if member != current_user:
                users[member]["groups"][group_name]["messages"] = group_data["messages"]
    open_group_chat(group_name)
    open_group_chat(group_name)
def open_group_chat(group_name):
    clear_screen()
    tk.Label(root, text=f"Group: {group_name}", font=("Arial", 18, "bold")).pack(pady=10)
    chat_frame = tk.Frame(root)
    chat_frame.pack(pady=10)
    group_data = users[current_user]["groups"].get(group_name, {})
    chat_messages = group_data.get("messages", [])
    for sender, message in chat_messages:
        sender_name = "You" if sender == current_user else users[sender]["username"]
        tk.Label(chat_frame, text=f"{sender_name}: {message}").pack(pady=2, anchor="w" if sender == current_user else "e")
    message_entry = tk.Entry(root)
    message_entry.pack(pady=5)
    apply_placeholder(message_entry, "Type a message...")
    tk.Button(root, text="Send", command=lambda: send_group_message(group_name, message_entry.get())).pack(pady=5)
    if group_data.get("admin") == current_user:
        tk.Button(root, text="Manage Group", command=lambda: manage_group(group_name)).pack(pady=5)
    tk.Button(root, text="Back", command=view_messages).pack(pady=5)
def add_group():
    clear_screen()
    tk.Label(root, text="Create Group", font=("Arial", 18, "bold")).pack(pady=10)
    group_name_entry = tk.Entry(root)
    group_name_entry.pack(pady=5)
    apply_placeholder(group_name_entry, "Group Name")
    members_entry = tk.Entry(root)
    members_entry.pack(pady=5)
    apply_placeholder(members_entry, "Enter usernames (comma separated)")
    tk.Button(root, text="Create", command=lambda: save_group(group_name_entry.get(), members_entry.get())).pack(pady=5)
    tk.Button(root, text="Back", command=view_messages).pack(pady=5)
def save_group(group_name, members):
    if not group_name.strip():
        messagebox.showerror("Error", "Group name cannot be empty!")
        return
    members_list = [user.strip() for user in members.split(",") if user.strip()]
    group_members = [email for email, data in users.items() if data["username"] in members_list]
    if not group_members:
        messagebox.showerror("Error", "No valid members found!")
        return
    group_members.append(current_user)
    users[current_user].setdefault("groups", {})[group_name] = {"members": group_members, "messages": [], "admin": current_user}
    for member in group_members:
        if member != current_user:
            users[member].setdefault("groups", {})[group_name] = {"members": group_members, "messages": [], "admin": current_user}
    messagebox.showinfo("Success", f"Group '{group_name}' created successfully!")
    view_messages()
def manage_group(group_name):
    clear_screen()
    tk.Label(root, text=f"Manage Group: {group_name}", font=("Arial", 18, "bold")).pack(pady=10)
    group_data = users[current_user]["groups"][group_name]
    members = group_data["members"]
    tk.Label(root, text="Members:").pack(pady=5)
    for member in members:
        if member != current_user:
            tk.Button(root, text=f"Remove {users[member]['username']}", command=lambda m=member: remove_group_member(group_name, m)).pack(pady=5)
    add_member_entry = tk.Entry(root)
    add_member_entry.pack(pady=5)
    apply_placeholder(add_member_entry, "Enter username to add")
    tk.Button(root, text="Add Member", command=lambda: add_group_member(group_name, add_member_entry.get())).pack(pady=5)
    tk.Button(root, text="Back", command=lambda: open_group_chat(group_name)).pack(pady=5)
def add_group_member(group_name, username):
    new_member = next((email for email, user in users.items() if user["username"] == username), None)
    if new_member and new_member not in users[current_user]["groups"][group_name]["members"]:
        users[current_user]["groups"][group_name]["members"].append(new_member)
        users[new_member].setdefault("groups", {})[group_name] = {
            "members": users[current_user]["groups"][group_name]["members"],
            "messages": users[current_user]["groups"][group_name]["messages"],
            "admin": users[current_user]["groups"][group_name]["admin"]
        }
        messagebox.showinfo("Success", f"{username} added to the group!")
    else:
        messagebox.showerror("Error", "Invalid username or already in group!")
    manage_group(group_name)
def remove_group_member(group_name, member_email):
    if member_email in users[current_user]["groups"][group_name]["members"]:
        users[current_user]["groups"][group_name]["members"].remove(member_email)
        del users[member_email]["groups"][group_name]
        messagebox.showinfo("Success", f"{users[member_email]['username']} removed from the group!")
    else:
        messagebox.showerror("Error", "Member not found!")
    manage_group(group_name)
def initialize_app():
    global root
    root = tk.Tk()
    root.geometry("400x600")
    root.title("Social Media App")
    show_main_screen()
    root.mainloop()
initialize_app()