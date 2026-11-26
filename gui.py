#!/usr/bin/env python3
"""Desktop viewer for the read-only Ubuntu Server baseline report."""

import subprocess
import threading
import tkinter as tk
from tkinter import ttk


BG = "#0b1220"
TEXT = "#edf4ff"
MUTED = "#9bacbf"
ACCENT = "#45d6c5"


class BaselineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ubuntu Server Baseline")
        self.geometry("900x650")
        self.minsize(720, 520)
        self.configure(bg=BG)
        self._style()
        self._build()

    def _style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", font=("Arial", 10))
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=TEXT)
        style.configure("Muted.TLabel", background=BG, foreground=MUTED)
        style.configure("TButton", padding=(12, 8), background="#24364b",
                        foreground=TEXT, borderwidth=0)
        style.configure("Accent.TButton", background=ACCENT, foreground="#07131b",
                        font=("Arial", 10, "bold"))

    def _build(self):
        shell = ttk.Frame(self, padding=24)
        shell.pack(fill="both", expand=True)
        ttk.Label(shell, text="LINUX HOST REVIEW  /  READ ONLY", style="Muted.TLabel").pack(anchor="w")
        ttk.Label(shell, text="Ubuntu Server Baseline", font=("Arial", 25, "bold")).pack(anchor="w", pady=(6, 4))
        ttk.Label(shell, text="Reports local status, firewall state, listening sockets and Jellyfin service state.",
                  style="Muted.TLabel").pack(anchor="w", pady=(0, 16))
        banner = tk.Frame(shell, bg="#17283a", padx=14, pady=12)
        banner.pack(fill="x", pady=(0, 14))
        tk.Label(banner, text="This check does not change system settings. Output may include host details.",
                 bg="#17283a", fg="#dbe8f5", font=("Arial", 10)).pack(anchor="w")
        self.run_button = ttk.Button(shell, text="Run read-only check", style="Accent.TButton", command=self.run_check)
        self.run_button.pack(anchor="e", pady=(0, 12))
        self.status = tk.StringVar(value="Run this on the Ubuntu host you want to review.")
        ttk.Label(shell, textvariable=self.status, style="Muted.TLabel").pack(anchor="w", pady=(0, 8))
        self.output = tk.Text(shell, bg="#070d16", fg=TEXT, insertbackground=TEXT,
                              relief="flat", padx=16, pady=14, font=("Menlo", 11), wrap="none")
        self.output.pack(fill="both", expand=True)
        self.output.insert("end", "The report will appear here.\n")
        self.output.configure(state="disabled")

    def run_check(self):
        self.run_button.configure(state="disabled")
        self.status.set("Collecting local status…")
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        result = subprocess.run(["bash", "baseline_check.sh"], capture_output=True,
                                text=True, timeout=120)
        self.after(0, self._finish, result)

    def _finish(self, result):
        self.run_button.configure(state="normal")
        self.status.set("Report ready." if result.returncode == 0 else "The check could not run on this system.")
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", result.stdout if result.returncode == 0 else result.stderr)
        self.output.configure(state="disabled")


if __name__ == "__main__":
    BaselineApp().mainloop()
