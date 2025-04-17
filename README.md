import tkinter as tk
from tkinter import messagebox
import re 
users = {}
current_user = None
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
def accept_follow_request(email):
    users[current_user]["follow_requests"].remove(email)
    users[current_user]["followers"].append(email)
    users[email]["following"].append(current_user)
    messagebox.showinfo("Accept", f"You accepted {users[email]['username']}")
    view_follow_requests()
def follow_user(email):
    if email in users[current_user]["following"]:
        users[current_user]["following"].remove(email) 
        users[email]["followers"].remove(current_user)
        messagebox.showinfo("Unfollow","Unfollow successfully!") 
    elif users[email]["private"]==True:
        send_follow_request(email)
    else:
        users[current_user]["following"].append(email)
        users[email]["followers"].appennd(current_user)
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
    users[current_user]["blocked"].append(email)
    messagebox.showinfo("Unblocked", f"You unblocked {users[email]['username']}")
    view_blocked_accounts()
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
def save_post_to_favorites(post):
    if post not in users[current_user]["saved_post"]:
        post["saved_by"].append(current_user)
        users[current_user]["saved_post"].append(post)
        messagebox.showinfo("Save","Save successfully!") 
    else:
        post["saved_by"].remove(current_user)
        users[current_user]["saved_post"].remove(post)
        messagebox.showinfo("Delete","Delete successfully!")
def like_post(post):
    if current_user in post["likes"]:
        post["likes"].remove(current_user)
    else:
        post["likes"].append(current_user)
def like_story(story):
    if current_user in story["likes"]:
        story["likes"].remove(current_user)
        messagebox.showinfo("D like","You do not like this story")
    else:
        story["likes"].append(current_user) 
        messagebox.showinfo("Like","You like this story") 
