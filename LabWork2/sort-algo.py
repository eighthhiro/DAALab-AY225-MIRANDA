import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import time
from typing import List
import threading

class ModernSortingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Comparison - Simple vs Divide & Conquer")
        self.root.geometry("1000x650")
        self.root.resizable(True, True)
        
        # Data storage
        self.data = []
        self.full_data = []  # Store the complete loaded dataset
        self.last_sorted_data = None
        self.is_sorting = False
        
        # Modern dark theme colors
        self.colors = {
            'bg': '#0F1419',
            'surface': '#1A1F26',
            'surface_light': '#252B33',
            'primary': '#3B82F6',
            'primary_hover': '#2563EB',
            'success': '#10B981',
            'warning': '#F59E0B',
            'text': '#E5E7EB',
            'text_dim': '#9CA3AF',
            'border': '#374151',
            'accent': '#8B5CF6',
            'danger': '#EF4444'
        }
        
        self.root.configure(bg=self.colors['bg'])
        self.setup_styles()
        self.create_widgets()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure progressbar
        style.configure(
            "Modern.Horizontal.TProgressbar",
            troughcolor=self.colors['surface'],
            background=self.colors['primary'],
            borderwidth=0,
            thickness=4
        )
        
        # Configure combobox
        style.configure(
            "TCombobox",
            fieldbackground=self.colors['surface_light'],
            background=self.colors['surface_light'],
            foreground=self.colors['text'],
            arrowcolor=self.colors['text'],
            borderwidth=0,
            relief="flat"
        )
        
        style.map('TCombobox',
            fieldbackground=[('readonly', self.colors['surface_light'])],
            selectbackground=[('readonly', self.colors['primary'])],
            selectforeground=[('readonly', self.colors['text'])]
        )
    
    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg=self.colors['surface'], height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="Sorting Algorithm Analyzer",
            font=("Segoe UI", 22, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=30, pady=20)
        
        # Main content area
        content = tk.Frame(self.root, bg=self.colors['bg'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Controls (300px width)
        left_panel = tk.Frame(content, bg=self.colors['bg'], width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        left_panel.pack_propagate(False)
        
        self.create_control_panel(left_panel)
        
        # Right panel - Results
        right_panel = tk.Frame(content, bg=self.colors['bg'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_results_panel(right_panel)
        
        # Footer with status
        footer = tk.Frame(self.root, bg=self.colors['surface'], height=40)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        self.status_label = tk.Label(
            footer,
            text="Ready to load data",
            font=("Segoe UI", 9),
            bg=self.colors['surface'],
            fg=self.colors['text_dim'],
            anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT, padx=20, fill=tk.X, expand=True)
        
        self.data_count_label = tk.Label(
            footer,
            text="",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['primary'],
            anchor=tk.E
        )
        self.data_count_label.pack(side=tk.RIGHT, padx=20)
    
    def create_control_panel(self, parent):
        # Load data section
        load_section = self.create_section(parent, "Data Source")
        
        self.file_label = tk.Label(
            load_section,
            text="No file loaded",
            font=("Segoe UI", 9),
            bg=self.colors['surface'],
            fg=self.colors['text_dim'],
            wraplength=250,
            justify=tk.LEFT
        )
        self.file_label.pack(anchor=tk.W, padx=15, pady=(0, 12))
        
        self.create_button(
            load_section,
            "📁  Load Data File",
            self.load_file,
            self.colors['primary']
        ).pack(fill=tk.X, padx=15, pady=(0, 12))
        
        # Dataset size selector with improved styling
        tk.Label(
            load_section,
            text="Dataset Size",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['text'],
            anchor=tk.W
        ).pack(anchor=tk.W, padx=15, pady=(0, 8))
        
        # Custom styled frame for dropdown
        dropdown_frame = tk.Frame(load_section, bg=self.colors['surface_light'], bd=0)
        dropdown_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Dropdown for dataset size
        self.size_var = tk.StringVar(value="All")
        size_options = ["All", "1,000", "5,000", "10,000", "20,000", "50,000", "100,000"]
        
        self.size_dropdown = ttk.Combobox(
            dropdown_frame,
            textvariable=self.size_var,
            values=size_options,
            state="readonly",
            font=("Segoe UI", 10),
            width=25
        )
        self.size_dropdown.pack(fill=tk.X, padx=8, pady=8)
        self.size_dropdown.bind("<<ComboboxSelected>>", self.on_size_change)
        
        # Algorithms section
        algo_section = self.create_section(parent, "Sorting Algorithms", top_margin=15)
        
        btn = self.create_button(
            algo_section,
            "Bubble Sort",
            lambda: self.run_sort(1),
            self.colors['surface_light'],
            hover_color=self.colors['border']
        )
        btn.pack(fill=tk.X, padx=15, pady=3)
        
        btn = self.create_button(
            algo_section,
            "Insertion Sort",
            lambda: self.run_sort(2),
            self.colors['surface_light'],
            hover_color=self.colors['border']
        )
        btn.pack(fill=tk.X, padx=15, pady=3)
        
        btn = self.create_button(
            algo_section,
            "Merge Sort",
            lambda: self.run_sort(3),
            self.colors['surface_light'],
            hover_color=self.colors['border']
        )
        btn.pack(fill=tk.X, padx=15, pady=3)
        
        # Run all button
        self.create_button(
            algo_section,
            "▶  Run All & Compare",
            lambda: self.run_sort(4),
            self.colors['accent']
        ).pack(fill=tk.X, padx=15, pady=(12, 15))
        
        # Export section
        export_section = self.create_section(parent, "Export", top_margin=15)
        
        self.create_button(
            export_section,
            "💾  Save Sorted Data",
            self.download_sorted_data,
            self.colors['success']
        ).pack(fill=tk.X, padx=15, pady=(0, 15))
    
    def create_section(self, parent, title, top_margin=0):
        section = tk.Frame(parent, bg=self.colors['surface'], relief=tk.FLAT)
        section.pack(fill=tk.X, pady=(top_margin, 0))
        
        tk.Label(
            section,
            text=title,
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['text'],
            anchor=tk.W
        ).pack(anchor=tk.W, padx=15, pady=(15, 12))
        
        return section
    
    def create_button(self, parent, text, command, bg_color, hover_color=None):
        if hover_color is None:
            hover_color = bg_color
        
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10),
            bg=bg_color,
            fg=self.colors['text'],
            activebackground=hover_color,
            activeforeground=self.colors['text'],
            cursor="hand2",
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=12
        )
        
        # Hover effects
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
        
        return btn
    
    def create_results_panel(self, parent):
        # Results header with progress
        header = tk.Frame(parent, bg=self.colors['surface'])
        header.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            header,
            text="Results",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=15, pady=12)
        
        # Right side container for progress bar and clear button
        right_container = tk.Frame(header, bg=self.colors['surface'])
        right_container.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=15)
        
        # Progress bar (70%)
        progress_frame = tk.Frame(right_container, bg=self.colors['surface'])
        progress_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.progress = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            style="Modern.Horizontal.TProgressbar"
        )
        self.progress.pack(fill=tk.X, pady=12)
        
        # Spacer
        tk.Frame(right_container, bg=self.colors['surface'], width=10).pack(side=tk.LEFT)
        
        # Clear button (30%)
        clear_btn_frame = tk.Frame(right_container, bg=self.colors['surface'])
        clear_btn_frame.pack(side=tk.LEFT)
        
        self.create_button(
            clear_btn_frame,
            "🗑️  Clear",
            self.clear_results,
            self.colors['surface_light'],
            hover_color=self.colors['border']
        ).pack(pady=6)
        
        # Main results container with two columns
        results_container = tk.Frame(parent, bg=self.colors['bg'])
        results_container.pack(fill=tk.BOTH, expand=True)
        
        # Left column - Statistics (40%)
        left_column = tk.Frame(results_container, bg=self.colors['bg'])
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        # Statistics label
        tk.Label(
            left_column,
            text="Statistics",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            anchor=tk.W
        ).pack(anchor=tk.W, pady=(0, 8))
        
        # Statistics text area
        stats_frame = tk.Frame(left_column, bg=self.colors['border'], bd=1)
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        self.stats_text = scrolledtext.ScrolledText(
            stats_frame,
            font=("Consolas", 10),
            wrap=tk.WORD,
            bg=self.colors['surface'],
            fg=self.colors['text'],
            insertbackground=self.colors['primary'],
            selectbackground=self.colors['primary'],
            selectforeground=self.colors['text'],
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=15,
            state=tk.DISABLED,
            width=35
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for statistics
        self.stats_text.tag_config("header", foreground=self.colors['primary'], font=("Consolas", 11, "bold"))
        self.stats_text.tag_config("success", foreground=self.colors['success'])
        self.stats_text.tag_config("warning", foreground=self.colors['warning'])
        self.stats_text.tag_config("danger", foreground=self.colors['danger'])
        self.stats_text.tag_config("dim", foreground=self.colors['text_dim'])
        
        # Right column - Sorted Data (60%)
        right_column = tk.Frame(results_container, bg=self.colors['bg'])
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Sorted data label
        tk.Label(
            right_column,
            text="Sorted Data Output",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            anchor=tk.W
        ).pack(anchor=tk.W, pady=(0, 8))
        
        # Sorted data text area
        data_frame = tk.Frame(right_column, bg=self.colors['border'], bd=1)
        data_frame.pack(fill=tk.BOTH, expand=True)
        
        self.data_text = scrolledtext.ScrolledText(
            data_frame,
            font=("Consolas", 10),
            wrap=tk.WORD,
            bg=self.colors['surface'],
            fg=self.colors['text'],
            insertbackground=self.colors['primary'],
            selectbackground=self.colors['primary'],
            selectforeground=self.colors['text'],
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=15,
            state=tk.DISABLED
        )
        self.data_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for data output
        self.data_text.tag_config("header", foreground=self.colors['primary'], font=("Consolas", 11, "bold"))
        self.data_text.tag_config("dim", foreground=self.colors['text_dim'])
    
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                self.full_data = [
                    int(x.strip()) 
                    for x in content.replace(',', ' ').split() 
                    if x.strip().lstrip('-').isdigit()
                ]
                
                if not self.full_data:
                    messagebox.showerror("Error", "No valid numbers found in the file.")
                    return
                
                # Apply size filter
                self.apply_size_filter()
                
                # Update UI
                filename = file_path.split('/')[-1]
                self.file_label.config(
                    text=f"✓ {filename}",
                    fg=self.colors['success']
                )
                
                self.update_data_count_label()
                self.status_label.config(text="Data loaded successfully")
                
                self.append_result(
                    f"Loaded {len(self.full_data):,} numbers from {filename}\n",
                    "success"
                )
                self.append_result(
                    f"Using {len(self.data):,} numbers for sorting\n",
                    "dim"
                )
                self.append_result(
                    f"Preview (first 20): {str(self.data[:20])}{'...' if len(self.data) > 20 else ''}\n\n",
                    "dim"
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {e}")
    
    def on_size_change(self, event=None):
        """Handle dataset size selection change"""
        if not self.full_data:
            messagebox.showwarning("Warning", "Please load a data file first.")
            self.size_var.set("All")
            return
        
        self.apply_size_filter()
        self.update_data_count_label()
        
        self.append_result(
            f"\nDataset size changed to: {self.size_var.get()}\n",
            "success"
        )
        self.append_result(
            f"Using {len(self.data):,} numbers for sorting\n\n",
            "dim"
        )
        self.status_label.config(text=f"Dataset size set to {self.size_var.get()}")
    
    def apply_size_filter(self):
        """Apply the selected dataset size filter"""
        size_str = self.size_var.get()
        
        if size_str == "All":
            self.data = self.full_data.copy()
        else:
            # Parse the size (remove commas)
            size = int(size_str.replace(",", ""))
            
            if len(self.full_data) >= size:
                self.data = self.full_data[:size]
            else:
                self.data = self.full_data.copy()
                messagebox.showinfo(
                    "Info", 
                    f"File contains only {len(self.full_data):,} numbers. Using all available data."
                )
    
    def update_data_count_label(self):
        """Update the data count label with current dataset info"""
        if self.size_var.get() == "All":
            self.data_count_label.config(text=f"{len(self.data):,} numbers loaded")
        else:
            self.data_count_label.config(
                text=f"{len(self.data):,} of {len(self.full_data):,} numbers"
            )
    
    def bubble_sort(self, arr: List[int]) -> List[int]:
        """
        Bubble Sort - O(n²)
        Classic exchange sort with optimized early exit
        Sorts in DESCENDING order
        """
        arr = arr.copy()
        n = len(arr)
        for i in range(n - 1):
            swapped = False
            for j in range(n - 1 - i):
                if arr[j] < arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            if not swapped:
                break
        return arr
    
    def insertion_sort(self, arr: List[int]) -> List[int]:
        """
        Insertion Sort - O(n²)
        Builds the final sorted array one item at a time
        Sorts in DESCENDING order
        """
        arr = arr.copy()
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            # Changed comparison for descending order
            while j >= 0 and arr[j] < key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr
    
    def merge_sort(self, arr: List[int]) -> List[int]:
        """
        Merge Sort - O(n log n)
        Divide and conquer algorithm
        Sorts in DESCENDING order
        """
        arr = arr.copy()
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid])
        right = self.merge_sort(arr[mid:])
        
        return self._merge(left, right)
    
    def _merge(self, left: List[int], right: List[int]) -> List[int]:
        """Merge two sorted arrays in descending order"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            # Changed comparison for descending order
            if left[i] >= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def run_sort(self, choice: int):
        if not self.data:
            messagebox.showwarning("Warning", "Please load a data file first.")
            return
        
        if self.is_sorting:
            messagebox.showinfo("Info", "Sorting is already in progress.")
            return
        
        thread = threading.Thread(target=self._execute_sort, args=(choice,))
        thread.daemon = True
        thread.start()
    
    def _execute_sort(self, choice: int):
        self.is_sorting = True
        self.progress.start(10)
        
        try:
            if choice == 4:
                self._run_all_sorts()
            else:
                algorithms = {
                    1: ("Bubble Sort", self.bubble_sort, "O(n²)"),
                    2: ("Insertion Sort", self.insertion_sort, "O(n²)"),
                    3: ("Merge Sort", self.merge_sort, "O(n log n)")
                }
                
                name, sort_func, complexity = algorithms[choice]
                self.status_label.config(text=f"Running {name}...")
                
                start_time = time.time()
                sorted_data = sort_func(self.data)
                elapsed_time = time.time() - start_time
                
                self.last_sorted_data = sorted_data
                
                # Statistics column
                self.append_result(f"\n{name}\n", "header")
                self.append_result(f"Complexity: {complexity}\n", "dim")
                self.append_result(f"Time: {elapsed_time:.6f} seconds\n", "success")
                self.append_result(f"Dataset size: {len(sorted_data):,} numbers\n\n", "dim")
                
                # Sorted data column
                self.clear_data_output()
                self.append_data_output(f"{name}\n", "header")
                self.append_data_output(f"Descending Order ({len(sorted_data):,} numbers)\n\n", "dim")
                self.append_data_output(self._format_dataset(sorted_data))
                
                self.status_label.config(text=f"{name} completed")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error during sorting: {e}")
            self.status_label.config(text="Error occurred")
        finally:
            self.is_sorting = False
            self.progress.stop()
    
    def _format_dataset(self, data: List[int], items_per_line: int = 10) -> str:
        """Format the dataset for display with a specified number of items per line"""
        lines = []
        for i in range(0, len(data), items_per_line):
            chunk = data[i:i + items_per_line]
            lines.append(', '.join(map(str, chunk)))
        return '\n'.join(lines)
    
    def _run_all_sorts(self):
        self.status_label.config(text="Running all algorithms...")
        
        algorithms = [
            ("Bubble Sort", self.bubble_sort, "O(n²)"),
            ("Insertion Sort", self.insertion_sort, "O(n²)"),
            ("Merge Sort", self.merge_sort, "O(n log n)")
        ]
        
        results = []
        
        # Statistics column
        self.append_result("\n═══ Performance Comparison ═══\n", "header")
        self.append_result(f"Dataset size: {len(self.data):,} numbers\n\n", "dim")
        
        for name, sort_func, complexity in algorithms:
            start_time = time.time()
            sorted_data = sort_func(self.data)
            elapsed_time = time.time() - start_time
            results.append((name, elapsed_time, complexity))
            
            # Color code based on complexity
            if "O(n²)" in complexity:
                tag = "warning"
            else:
                tag = "success"
            
            self.append_result(f"{name} ({complexity}):\n", tag)
            self.append_result(f"  Time: {elapsed_time:.6f} seconds\n\n")
        
        # Rank by time
        results.sort(key=lambda x: x[1])
        
        self.append_result("═══ Ranking (Fastest to Slowest) ═══\n", "header")
        for rank, (name, elapsed_time, complexity) in enumerate(results, 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
            self.append_result(f"{medal} {rank}. {name}\n")
            self.append_result(f"   {elapsed_time:.6f}s ({complexity})\n\n", "dim")
        
        # Performance analysis
        self.append_result("═══ Performance Gap Analysis ═══\n", "header")
        fastest = results[0]
        slowest = results[-1]
        
        speedup = slowest[1] / fastest[1] if fastest[1] > 0 else 0
        
        self.append_result(f"Fastest: {fastest[0]}\n", "success")
        self.append_result(f"Slowest: {slowest[0]}\n", "danger")
        self.append_result(f"\nSpeedup: {speedup:.2f}x faster\n", "warning")
        self.append_result(f"Time difference: {slowest[1] - fastest[1]:.6f}s\n\n", "dim")
        
        # Display complete sorted dataset in right column
        self.last_sorted_data = sorted_data
        self.clear_data_output()
        self.append_data_output("Comparison Complete\n", "header")
        self.append_data_output(f"Descending Order ({len(sorted_data):,} numbers)\n\n", "dim")
        self.append_data_output(self._format_dataset(sorted_data))
        
        self.status_label.config(text="All algorithms completed")
    
    def append_result(self, text: str, tag=None):
        """Append to statistics text box"""
        self.stats_text.config(state=tk.NORMAL)
        if tag:
            self.stats_text.insert(tk.END, text, tag)
        else:
            self.stats_text.insert(tk.END, text)
        self.stats_text.see(tk.END)
        self.stats_text.config(state=tk.DISABLED)
    
    def append_data_output(self, text: str, tag=None):
        """Append to sorted data output text box"""
        self.data_text.config(state=tk.NORMAL)
        if tag:
            self.data_text.insert(tk.END, text, tag)
        else:
            self.data_text.insert(tk.END, text)
        self.data_text.see(tk.END)
        self.data_text.config(state=tk.DISABLED)
    
    def clear_data_output(self):
        """Clear the data output text area"""
        self.data_text.config(state=tk.NORMAL)
        self.data_text.delete(1.0, tk.END)
        self.data_text.config(state=tk.DISABLED)
    
    def download_sorted_data(self):
        if self.last_sorted_data is None:
            messagebox.showwarning("Warning", "No sorted data available. Run a sorting algorithm first.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="sorted_data.txt"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w') as file:
                for num in self.last_sorted_data:
                    file.write(f"{num}\n")
            
            messagebox.showinfo("Success", f"Saved {len(self.last_sorted_data):,} numbers successfully!")
            self.status_label.config(text="Data exported successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {e}")
    
    def clear_results(self):
        """Clear both results text areas"""
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.config(state=tk.DISABLED)
        
        self.data_text.config(state=tk.NORMAL)
        self.data_text.delete(1.0, tk.END)
        self.data_text.config(state=tk.DISABLED)
        
        self.status_label.config(text="Results cleared")


def main():
    root = tk.Tk()
    app = ModernSortingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()