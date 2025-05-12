import serial
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import re
import time
import json

# ----- Configurable Error Database -----
ps5_errors = {
    "CE-108255-1": "Application crash. Try reinstalling or updating the game/system software.",
    "NW-102308-4": "Cannot connect to server. Check network connection or PSN status.",
    "WS-116521-6": "PSN is busy. Try again later.",
    "SU-101193-5": "System update failed. Retry or check the update file.",
    "NP-104602-3": "Cannot connect to PSN. Check your network settings.",
    # Extend this as needed...
}

error_code_regex = re.compile(r'([A-Z]{2}-\d{6}-\d)')

class PS5LogDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("PS5 UART Log Dashboard")
        self.serial_thread = None
        self.running = False

        self.setup_ui()

    def setup_ui(self):
        # Top control frame
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(control_frame, text="Serial Port:").pack(side='left')
        self.port_entry = ttk.Entry(control_frame)
        self.port_entry.insert(0, "/dev/ttyUSB0")
        self.port_entry.pack(side='left', padx=5)

        ttk.Label(control_frame, text="Baud Rate:").pack(side='left')
        self.baud_entry = ttk.Entry(control_frame, width=10)
        self.baud_entry.insert(0, "115200")
        self.baud_entry.pack(side='left', padx=5)

        self.connect_btn = ttk.Button(control_frame, text="Connect", command=self.toggle_serial)
        self.connect_btn.pack(side='left', padx=5)

        self.save_logs = tk.BooleanVar(value=True)
        ttk.Checkbutton(control_frame, text="Save Logs", variable=self.save_logs).pack(side='left', padx=10)

        # Search bar
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side='left')
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side='left', fill='x', expand=True, padx=5)
        ttk.Button(search_frame, text="Filter", command=self.apply_filter).pack(side='left', padx=5)

        # Log display
        self.log_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=20)
        self.log_display.pack(fill='both', expand=True, padx=10, pady=5)

        # Error details panel
        self.error_panel = tk.Text(self.root, height=4, bg='#f0f0f0')
        self.error_panel.pack(fill='x', padx=10, pady=5)
        self.error_panel.insert(tk.END, "Error details will appear here...")
        self.error_panel.config(state='disabled')

    def toggle_serial(self):
        if self.running:
            self.running = False
            self.connect_btn.config(text="Connect")
        else:
            port = self.port_entry.get()
            try:
                baud = int(self.baud_entry.get())
                self.ser = serial.Serial(port, baud, timeout=1)
                self.running = True
                self.connect_btn.config(text="Disconnect")
                self.serial_thread = threading.Thread(target=self.read_uart, daemon=True)
                self.serial_thread.start()
            except Exception as e:
                messagebox.showerror("Connection Error", str(e))

    def read_uart(self):
        log_file = open(f"ps5_log_{int(time.time())}.txt", "w") if self.save_logs.get() else None
        while self.running:
            try:
                line = self.ser.readline().decode(errors='ignore').strip()
                if not line:
                    continue

                timestamp = time.strftime("[%H:%M:%S] ")
                display_line = timestamp + line + '\n'
                self.log_display.insert(tk.END, display_line)
                self.log_display.see(tk.END)

                if log_file:
                    log_file.write(display_line)

                matches = error_code_regex.findall(line)
                for code in matches:
                    desc = ps5_errors.get(code, "Unknown error. Consider updating your DB.")
                    self.log_display.insert(tk.END, f"\n[!] Error Detected: {code} — {desc}\n", "error")
                    self.log_display.see(tk.END)
                    self.show_error_details(code, desc)
            except Exception as e:
                print("UART Read Error:", e)
                break
        if log_file:
            log_file.close()

    def apply_filter(self):
        keyword = self.search_entry.get().lower()
        content = self.log_display.get("1.0", tk.END)
        filtered = [line for line in content.splitlines() if keyword in line.lower()]
        self.log_display.delete("1.0", tk.END)
        self.log_display.insert(tk.END, '\n'.join(filtered))

    def show_error_details(self, code, desc):
        self.error_panel.config(state='normal')
        self.error_panel.delete("1.0", tk.END)
        self.error_panel.insert(tk.END, f"{code}: {desc}")
        self.error_panel.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = PS5LogDashboard(root)
    root.mainloop()
