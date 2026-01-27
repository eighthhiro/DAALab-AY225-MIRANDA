import time
import os
from typing import List, Tuple

class SortingAnalyzer:
    def __init__(self):
        self.data = []
        self.last_sorted_data = None
        self.last_algorithm_name = None
    
    def greet(self):
        """Display welcome message"""
        print("=" * 60)
        print("Welcome to SDA! (Sorting in Descending Algorithms)")
        print("=" * 60)
        print()
    
    def load_data(self) -> bool:
        """Load data from a text file"""
        while True:
            file_path = input("Enter the name or path to your .txt file: ").strip()
            
            if not os.path.exists(file_path):
                print(f"Error: File '{file_path}' not found. Please try again.\n")
                continue
            
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    # Try to parse numbers from the file
                    self.data = [int(x.strip()) for x in content.replace(',', ' ').split() if x.strip().isdigit() or (x.strip()[0] == '-' and x.strip()[1:].isdigit())]
                    
                    if not self.data:
                        print("Error: No valid numbers found in the file. Please try again.\n")
                        continue
                    
                    print(f"\nSuccessfully loaded {len(self.data)} numbers from the file.")
                    print(f"Preview: {self.data[:10]}{'...' if len(self.data) > 10 else ''}\n")
                    return True
                    
            except Exception as e:
                print(f"Error reading file: {e}. Please try again.\n")
    
    def bubble_sort(self, arr: List[int]) -> List[int]:
        """Bubble sort implementation"""
        arr = arr.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] < arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    
    def insertion_sort(self, arr: List[int]) -> List[int]:
        """Insertion sort implementation"""
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
        """Merge sort implementation"""
        arr = arr.copy()
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid])
        right = self.merge_sort(arr[mid:])
        
        return self._merge(left, right)
    
    def _merge(self, left: List[int], right: List[int]) -> List[int]:
        """Helper function for merge sort"""
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
    
    def execute_sort(self, name: str, sort_func) -> Tuple[List[int], float]:
        """Execute a sorting algorithm and measure time"""
        print(f"\nLoading... (Running {name})")
        start_time = time.time()
        sorted_data = sort_func(self.data)
        end_time = time.time()
        elapsed_time = end_time - start_time
        return sorted_data, elapsed_time
    
    def display_result(self, name: str, sorted_data: List[int], elapsed_time: float):
        """Display sorting result"""
        print(f"\n{name} Result:")
        print("-" * 60)
        print(f"Sorted Data: {sorted_data[:20]}{'...' if len(sorted_data) > 20 else ''}")
        print(f"Time Taken: {elapsed_time:.6f} seconds")
        print("-" * 60)
    
    def run_single_sort(self, choice: int):
        """Run a single sorting algorithm"""
        algorithms = {
            1: ("Bubble Sort", self.bubble_sort),
            2: ("Insertion Sort", self.insertion_sort),
            3: ("Merge Sort", self.merge_sort)
        }
        
        name, sort_func = algorithms[choice]
        sorted_data, elapsed_time = self.execute_sort(name, sort_func)
        self.display_result(name, sorted_data, elapsed_time)
        
        # Store the last sorted data for download option
        self.last_sorted_data = sorted_data
        self.last_algorithm_name = name
    
    def run_all_sorts(self):
        """Run all sorting algorithms and rank them"""
        print("\nRunning all sorting algorithms...\n")
        
        algorithms = [
            ("Bubble Sort", self.bubble_sort),
            ("Insertion Sort", self.insertion_sort),
            ("Merge Sort", self.merge_sort)
        ]
        
        results = []
        
        for name, sort_func in algorithms:
            sorted_data, elapsed_time = self.execute_sort(name, sort_func)
            self.display_result(name, sorted_data, elapsed_time)
            results.append((name, elapsed_time))
        
        # Rank by time (fastest to slowest)
        results.sort(key=lambda x: x[1])
        
        print("\n" + "=" * 60)
        print("PERFORMANCE RANKING (Fastest to Slowest)")
        print("=" * 60)
        for rank, (name, elapsed_time) in enumerate(results, 1):
            print(f"{rank}. {name}: {elapsed_time:.6f} seconds")
        print("=" * 60)
        
        # Store the last sorted data for download option
        self.last_sorted_data = sorted_data
        self.last_algorithm_name = "All Algorithms"
    
    def download_sorted_data(self):
        """Download the last sorted data to a text file"""
        if self.last_sorted_data is None:
            print("\nNo sorted data available. Please run a sorting algorithm first.")
            return
        
        print("\n" + "=" * 60)
        print("DOWNLOAD SORTED DATA")
        print("=" * 60)
        
        default_filename = "sorted_data.txt"
        filename = input(f"Enter filename (default: {default_filename}): ").strip()
        
        if not filename:
            filename = default_filename
        
        # Add .txt extension if not present
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        try:
            with open(filename, 'w') as file:
                # Write each number on a new line
                for num in self.last_sorted_data:
                    file.write(f"{num}\n")
            
            print(f"\n✓ Successfully saved {len(self.last_sorted_data)} numbers to '{filename}'")
            print(f"  Algorithm used: {self.last_algorithm_name}")
            print("=" * 60)
            
        except Exception as e:
            print(f"\nError saving file: {e}")
            print("=" * 60)
    
    def display_menu(self):
        """Display the menu"""
        print("\n" + "=" * 60)
        print("MENU")
        print("=" * 60)
        print("1. Bubble Sort")
        print("2. Insertion Sort")
        print("3. Merge Sort")
        print("4. Run All Algorithms")
        print("5. Download Sorted Data")
        print("6. Load New File")
        print("7. Exit")
        print("=" * 60)
    
    def run(self):
        """Main program loop"""
        self.greet()
        
        if not self.load_data():
            return
        
        while True:
            self.display_menu()
            
            try:
                choice = input("\nEnter your choice (1-7): ").strip()
                
                if choice == '7':
                    print("\nThank you for using our program!")
                    print("Goodbye!\n")
                    break
                elif choice == '6':
                    if self.load_data():
                        continue
                elif choice == '5':
                    self.download_sorted_data()
                elif choice == '4':
                    self.run_all_sorts()
                elif choice in ['1', '2', '3']:
                    self.run_single_sort(int(choice))
                else:
                    print("\nInvalid choice. Please enter a number between 1 and 7.")
                    
            except Exception as e:
                print(f"\nError: {e}. Please try again.")


if __name__ == "__main__":
    analyzer = SortingAnalyzer()
    analyzer.run()