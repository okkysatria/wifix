import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import threading

BACKGROUND_COLOR = '#2e2e2e'
TEXT_COLOR = 'white'
BUTTON_COLORS = {
    'search': '#FFA500',
    'rescan': '#4CAF50',
    'save': '#2196F3'
}
FONT = ("Helvetica", 12)

class WifiPasswordViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Wi-Fi Password Viewer")
        self.root.geometry("700x500")
        self.root.configure(bg=BACKGROUND_COLOR)
        self.root.resizable(False, False)
        
        self.create_widgets()
        self.restart_scan()
    
    def create_widgets(self):
        title_label = tk.Label(self.root, text="Wi-Fi Password Viewer", font=("Helvetica", 16, "bold"), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
        title_label.pack(pady=10)
        
        search_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        search_frame.pack(pady=5)
        
        self.search_entry = tk.Entry(search_frame, width=40, font=FONT)
        self.search_entry.grid(row=0, column=0, padx=10)
        self.search_entry.bind("<Return>", self.on_search_entry_return)  # Bind Enter key
        
        search_button = tk.Button(search_frame, text="Search", command=self.search_wifi, bg=BUTTON_COLORS['search'], fg=TEXT_COLOR, font=FONT)
        search_button.grid(row=0, column=1)
        
        self.output_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Courier", 10), width=80, height=20, bg="#1e1e1e", fg=TEXT_COLOR, insertbackground="white")
        self.output_area.pack(pady=10)
        
        self.output_area.tag_configure("bold", font=("Courier", 10, "bold"))
        
        button_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        button_frame.pack(pady=10)
        
        self.loading_label = tk.Label(button_frame, text="", font=FONT, fg="yellow", bg=BACKGROUND_COLOR)
        self.loading_label.grid(row=0, column=0, padx=10)
        
        self.scan_button = tk.Button(button_frame, text="Rescan", command=self.restart_scan, bg=BUTTON_COLORS['rescan'], fg=TEXT_COLOR, font=FONT)
        self.scan_button.grid(row=0, column=1, padx=10)
        
        self.save_button = tk.Button(button_frame, text="Save to Note", command=self.save_to_note, bg=BUTTON_COLORS['save'], fg=TEXT_COLOR, font=FONT)
        self.save_button.grid(row=0, column=2, padx=10)
    
    def show_loading(self):
        self.loading_label.config(text="Loading...")
    
    def hide_loading(self):
        self.loading_label.config(text="")
    
    def display_wifi_passwords(self):
        self.show_loading()
        
        self.output_area.delete(1.0, tk.END)
        
        command = '''for /f "skip=9 tokens=1,2 delims=:" %i in ('netsh wlan show profiles') do @echo %j | findstr -i -v echo | netsh wlan show profiles %j key=clear'''
        
        try:
            output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
            parsed_output = self.parse_output(output)
            if parsed_output:
                self.output_area.insert(tk.END, parsed_output)
            else:
                self.output_area.insert(tk.END, "No Wi-Fi profiles found.")
        except subprocess.CalledProcessError as e:
            self.output_area.insert(tk.END, f"Error occurred: {e.output}")
        
        self.hide_loading()
    
    def parse_output(self, output):
        parsed = ""
        profiles = output.split("All User Profile")[1:]
        seen_ssids = set()
        
        for profile in profiles:
            lines = profile.splitlines()
            ssid_line = next((line for line in lines if "SSID name" in line), "").strip()
            auth_line = next((line for line in lines if "Authentication" in line), "").strip()
            cipher_line = next((line for line in lines if "Cipher" in line), "").strip()
            key_line = next((line for line in lines if "Key Content" in line), "").strip()
            
            ssid = ssid_line.split(":")[-1].strip().replace('"', '') if ssid_line else "N/A"
            auth = auth_line.split(":")[-1].strip() if auth_line else "N/A"
            cipher = cipher_line.split(":")[-1].strip() if cipher_line else "N/A"
            key = key_line.split(":")[-1].strip() if key_line else "Not found"
            
            if key != "Not found" and ssid not in seen_ssids:
                seen_ssids.add(ssid)
                parsed += self.format_bold('Wifi') + f": {ssid}\n"
                parsed += self.format_bold('Password') + f": {key}\n"
                parsed += self.format_bold('Authentication') + f": {auth}\n"
                parsed += self.format_bold('Encryption') + f": {cipher}\n"
                parsed += "-"*40 + "\n"
        
        return parsed
    
    def format_bold(self, label):
        return label
    
    def search_wifi(self, *args):
        search_term = self.search_entry.get().strip().lower()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a Wi-Fi name to search.")
            return
        
        wifi_data = self.output_area.get(1.0, tk.END).strip()
        if not wifi_data:
            messagebox.showwarning("Warning", "No Wi-Fi data to search.")
            return
        
        lines = wifi_data.splitlines()
        filtered_output = ""
        found = False
        
        for i in range(0, len(lines), 5):
            wifi_name = lines[i].split(":")[-1].strip().lower()
            if search_term in wifi_name:
                found = True
                filtered_output += "\n".join(lines[i:i+5]) + "\n"
                filtered_output += "-"*40 + "\n"
        
        if found:
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(tk.END, filtered_output)
        else:
            messagebox.showinfo("Search Results", f"Wi-Fi name '{search_term}' not found.")
    
    def on_search_entry_return(self, event):
        self.search_wifi()
    
    def restart_scan(self):
        self.output_area.delete(1.0, tk.END)
        threading.Thread(target=self.display_wifi_passwords, daemon=True).start()
    
    def save_to_note(self):
        wifi_data = self.output_area.get(1.0, tk.END)
        if not wifi_data.strip():
            messagebox.showwarning("Warning", "No Wi-Fi data to save.")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(wifi_data)
                messagebox.showinfo("Success", f"Wi-Fi data saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WifiPasswordViewer(root)
    root.mainloop()
