import tkinter as tk
from tkinter import filedialog, scrolledtext
from pathlib import Path

class LogAnalyzer:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Log Analyzer")
        self.root.geometry("800x600")
        self.chosen_file = ""

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the user interface."""
        # Header frame
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X)

        title = tk.Label(
            header_frame,
            text="Log Analyzer",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title.pack(pady=10)

        # File selection frame
        file_frame = tk.Frame(self.root, bg="#ecf0f1", height=80)
        file_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(
            file_frame,
            text="Select a log file to analyze:",
            font=("Arial", 10),
            bg="#ecf0f1"
        ).pack(anchor=tk.W, padx=10, pady=5)

        button_frame = tk.Frame(file_frame, bg="#ecf0f1")
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        self.select_btn = tk.Button(
            button_frame,
            text="Select File",
            command=self.select_file,
            bg="#3498db",
            fg="white",
            padx=15,
            pady=8,
            font=("Arial", 10),
            cursor="hand2"
        )
        self.select_btn.pack(side=tk.LEFT)

        self.analyze_btn = tk.Button(
            button_frame,
            text="Analyze Log",
            command=self.analyze_log,
            bg="#27ae60",
            fg="white",
            padx=15,
            pady=8,
            font=("Arial", 10),
            state=tk.DISABLED,
            cursor="hand2"
        )
        self.analyze_btn.pack(side=tk.LEFT, padx=5)

        self.file_label = tk.Label(
            file_frame,
            text="No file selected",
            font=("Arial", 9),
            bg="#ecf0f1",
            fg="#7f8c8d"
        )
        self.file_label.pack(anchor=tk.W, padx=10, pady=5)

        # Status frame
        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        self.status_label.pack(fill=tk.X, padx=10, pady=5)

        # Results frame with scrolled text
        results_frame = tk.Frame(self.root)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            font=("Courier New", 9),
            bg="#2c3e50",
            fg="#ecf0f1",
            padx=10,
            pady=10
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # Configure tags for styling
        self.results_text.tag_config("error_header", foreground="#e74c3c", font=("Courier New", 10, "bold"))
        self.results_text.tag_config("warning_header", foreground="#f39c12", font=("Courier New", 10, "bold"))
        self.results_text.tag_config("error_line", foreground="#e74c3c")
        self.results_text.tag_config("warning_line", foreground="#f39c12")
        self.results_text.tag_config("info", foreground="#95a5a6")
        self.results_text.tag_config("failed_login", foreground="#00d0ff", font=("Courier New", 9, "bold"))

    def select_file(self) -> None:
        """Handle file selection."""
        self.chosen_file = filedialog.askopenfilename(
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if self.chosen_file:
            file_path = Path(self.chosen_file)
            display_name = f"{file_path.name} ({file_path.parent})"
            self.file_label.config(text=f"Selected: {display_name}", fg="#2c3e50")
            self.analyze_btn.config(state=tk.NORMAL)
            self.status_label.config(text="")
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            self.results_text.config(state=tk.DISABLED)

    def analyze_log(self) -> None:
        """Analyze the selected log file."""
        if not self.chosen_file:
            return

        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)

        errors = []
        warnings = []
        error_keywords = ["failed login", "suspicious activity", "unauthorized access", "repeated 404", "unusual traffic", "malware detected", "data breach", "ddos attack", "sql injection", "xss attack", "authentication failure", "permission denied", "access violation", "admin"]

        try:
            with open(self.chosen_file, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()
                for line in lines:
                    if "ERROR" in line:
                        errors.append(line.strip())
                    elif "WARNING" in line:
                        warnings.append(line.strip())

            # Display results
            self.results_text.insert(tk.END, "ERRORS\n", "error_header")
            self.results_text.insert(tk.END, "=" * 80 + "\n", "info")

            if errors:
                for error in errors:
                    if any(keyword in error.lower() for keyword in error_keywords):
                        self.results_text.insert(tk.END, f"  {error}\n", "failed_login")
                    else:
                        self.results_text.insert(tk.END, f"  {error}\n", "error_line")
            else:
                self.results_text.insert(tk.END, "  No errors found\n", "info")

            self.results_text.insert(tk.END, "\n\nWARNINGS\n", "warning_header")
            self.results_text.insert(tk.END, "=" * 80 + "\n", "info")

            if warnings:
                for warning in warnings:
                    if any(keyword in warning.lower() for keyword in error_keywords):
                        self.results_text.insert(tk.END, f"  {warning}\n", "failed_login")
                    else:
                        self.results_text.insert(tk.END, f"  {warning}\n", "warning_line")
            else:
                self.results_text.insert(tk.END, "  No warnings found\n", "info")

            # Update status
            error_count = len(errors)
            warning_count = len(warnings)
            self.status_label.config(
                text=f"✓ Analysis complete: {error_count} error(s), {warning_count} warning(s)",
                fg="#27ae60"
            )

        except Exception as e:
            self.results_text.insert(tk.END, f"Error reading file: {str(e)}", "error_header")
            self.status_label.config(text="✗ Error analyzing file", fg="#e74c3c")

        self.results_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = LogAnalyzer(root)
    root.mainloop()

