import requests
from collections import Counter
import tkinter as tk
from tkinter import ttk, messagebox

def get_user_info(username):
    res = requests.get(f"https://api.github.com/users/{username}")
    if res.status_code != 200:
        return None
    return res.json()

def get_repos(username):
    repos = []
    page = 1
    while True:
        res = requests.get(f"https://api.github.com/users/{username}/repos?page={page}&per_page=100")
        if res.status_code != 200 or not res.json():
            break
        repos.extend(res.json())
        page += 1
    return repos

def analyze():
    username = entry.get().strip()
    if not username:
        messagebox.showwarning("Input Error", "Please enter a GitHub username.")
        return

    output_box.configure(state="normal")
    output_box.delete("1.0", tk.END)

    user = get_user_info(username)
    if not user:
        output_box.insert(tk.END, "❌ User not found.\n")
        output_box.configure(state="disabled")
        return

    repos = get_repos(username)
    output_box.insert(tk.END, f"👤 Username: {user['login']}\n")
    output_box.insert(tk.END, f"📦 Public Repos: {user['public_repos']}\n")
    output_box.insert(tk.END, f"👥 Followers: {user['followers']}\n")
    output_box.insert(tk.END, f"🌟 Total Stars: {sum(r['stargazers_count'] for r in repos)}\n\n")

    languages = Counter()
    for repo in repos:
        lang = repo['language']
        if lang:
            languages[lang] += 1

    if languages:
        output_box.insert(tk.END, "🗣️ Top Languages:\n")
        for lang, count in languages.most_common(5):
            output_box.insert(tk.END, f" - {lang}: {count} repos\n")

    top_starred = sorted(repos, key=lambda r: r['stargazers_count'], reverse=True)[:3]
    output_box.insert(tk.END, "\n🌟 Top Starred Repos:\n")
    for repo in top_starred:
        output_box.insert(tk.END, f" - {repo['name']} ({repo['stargazers_count']}⭐)\n    {repo['html_url']}\n")

    output_box.configure(state="disabled")

# GUI Setup
root = tk.Tk()
root.title("GitHub Profile Analyzer")
root.geometry("600x500")
root.configure(bg="#1e1e1e")

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 11), padding=6, background="#3c3c3c", foreground="white")
style.configure("TEntry", font=("Segoe UI", 11))

# Title
title = tk.Label(root, text="🔍 GitHub Profile Analyzer", font=("Segoe UI", 16, "bold"), bg="#1e1e1e", fg="white")
title.pack(pady=10)

# Entry
entry_frame = tk.Frame(root, bg="#1e1e1e")
entry_frame.pack(pady=5)

entry = ttk.Entry(entry_frame, width=40)
entry.pack(side=tk.LEFT, padx=10)

btn = ttk.Button(entry_frame, text="Analyze", command=analyze)
btn.pack(side=tk.LEFT)

# Output Box
output_frame = tk.Frame(root, bg="#1e1e1e")
output_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

output_box = tk.Text(output_frame, wrap=tk.WORD, font=("Consolas", 11), bg="#2d2d2d", fg="#eeeeee", insertbackground="white")
output_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
output_box.configure(state="disabled")

scrollbar = ttk.Scrollbar(output_frame, command=output_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_box['yscrollcommand'] = scrollbar.set

# Run GUI
root.mainloop()
