import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import time
from typing import List
import threading

class ModernSortingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Analyzer")
        self.root.geometry("1000x650")
        self.root.resizable(True, True)
        
        # Data storage
        self.data = []
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
            'text': '#E5E7EB',
            'text_dim': '#9CA3AF',
            'border': '#374151',
            'accent': '#8B5CF6'
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
        ).pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Algorithms section
        algo_section = self.create_section(parent, "Sorting Algorithms", top_margin=15)
        
        algorithms = [
            ("Bubble Sort", 1),
            ("Insertion Sort", 2),
            ("Merge Sort", 3)
        ]
        
        for text, choice in algorithms:
            btn = self.create_button(
                algo_section,
                text,
                lambda c=choice: self.run_sort(c),
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
        
        # Results text area
        text_frame = tk.Frame(parent, bg=self.colors['border'], bd=1)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = scrolledtext.ScrolledText(
            text_frame,
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
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for formatting
        self.results_text.tag_config("header", foreground=self.colors['primary'], font=("Consolas", 11, "bold"))
        self.results_text.tag_config("success", foreground=self.colors['success'])
        self.results_text.tag_config("dim", foreground=self.colors['text_dim'])
    
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
                self.data = [
                    int(x.strip()) 
                    for x in content.replace(',', ' ').split() 
                    if x.strip().lstrip('-').isdigit()
                ]
                
                if not self.data:
                    messagebox.showerror("Error", "No valid numbers found in the file.")
                    return
                
                # Update UI
                filename = file_path.split('/')[-1]
                self.file_label.config(
                    text=f"✓ {filename}",
                    fg=self.colors['success']
                )
                
                self.data_count_label.config(text=f"{len(self.data):,} numbers loaded")
                self.status_label.config(text="Data loaded successfully")
                
                self.append_result(
                    f"Loaded {len(self.data):,} numbers from {filename}\n",
                    "success"
                )
                self.append_result(
                    f"Preview (first 20): {str(self.data[:20])}{'...' if len(self.data) > 20 else ''}\n\n",
                    "dim"
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {e}")
    
    def bubble_sort(self, arr: List[int]) -> List[int]:
        arr = arr.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] < arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    
    def insertion_sort(self, arr: List[int]) -> List[int]:
        arr = arr.copy()
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] < key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr
    
    def merge_sort(self, arr: List[int]) -> List[int]:
        arr = arr.copy()
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid])
        right = self.merge_sort(arr[mid:])
        
        return self._merge(left, right)
    
    def _merge(self, left: List[int], right: List[int]) -> List[int]:
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
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
                    1: ("Bubble Sort", self.bubble_sort),
                    2: ("Insertion Sort", self.insertion_sort),
                    3: ("Merge Sort", self.merge_sort)
                }
                
                name, sort_func = algorithms[choice]
                self.status_label.config(text=f"Running {name}...")
                
                start_time = time.time()
                sorted_data = sort_func(self.data)
                elapsed_time = time.time() - start_time
                
                self.last_sorted_data = sorted_data
                
                self.append_result(f"\n{name}\n", "header")
                self.append_result(f"Time: {elapsed_time:.6f} seconds\n", "success")
                self.append_result(f"Dataset size: {len(sorted_data):,} numbers\n\n", "dim")
                
                # Display entire sorted dataset
                self.append_result("Complete Sorted Dataset:\n", "header")
                self.append_result(self._format_dataset(sorted_data))
                self.append_result("\n\n")
                
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
            ("Bubble Sort", self.bubble_sort),
            ("Insertion Sort", self.insertion_sort),
            ("Merge Sort", self.merge_sort)
        ]
        
        results = []
        self.append_result("\nPerformance Comparison\n", "header")
        
        for name, sort_func in algorithms:
            start_time = time.time()
            sorted_data = sort_func(self.data)
            elapsed_time = time.time() - start_time
            results.append((name, elapsed_time))
            
            self.append_result(f"{name}: ", "dim")
            self.append_result(f"{elapsed_time:.6f}s\n", "success")
        
        # Rank by time
        results.sort(key=lambda x: x[1])
        
        self.append_result("\nRanking (Fastest to Slowest)\n", "header")
        for rank, (name, elapsed_time) in enumerate(results, 1):
            self.append_result(f"{rank}. {name}: {elapsed_time:.6f}s\n")
        
        # Display complete sorted dataset from the last algorithm
        self.last_sorted_data = sorted_data
        self.append_result(f"\nComplete Sorted Dataset ({len(sorted_data):,} numbers):\n", "header")
        self.append_result(self._format_dataset(sorted_data))
        self.append_result("\n\n")
        
        self.status_label.config(text="All algorithms completed")
    
    def append_result(self, text: str, tag=None):
        self.results_text.config(state=tk.NORMAL)
        if tag:
            self.results_text.insert(tk.END, text, tag)
        else:
            self.results_text.insert(tk.END, text)
        self.results_text.see(tk.END)
        self.results_text.config(state=tk.DISABLED)
    
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
        """Clear the results text area"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.status_label.config(text="Results cleared")



def main():
    root = tk.Tk()
    app = ModernSortingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()