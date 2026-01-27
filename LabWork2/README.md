# LabWork2: Sorting Algorithm Performance Analysis

## Overview

This program implements and compares three fundamental sorting algorithms to demonstrate the performance gap between simple sorts and divide-and-conquer approaches:

1. **Bubble Sort** - O(n²): Exchange-based sorting with optimized early exit
2. **Insertion Sort** - O(n²): Builds the sorted array one element at a time
3. **Merge Sort** - O(n log n): Recursive divide-and-conquer algorithm

All algorithms are implemented manually (no built-in sorting functions) and sort data in **descending order**. The program provides detailed performance metrics, rankings, and speedup analysis.

**Key Learning**: Visualizes why O(n log n) algorithms dramatically outperform O(n²) algorithms on large datasets.

## How to Execute

1. **Run the program**:
   ```bash
   python sorting_comparison_gui.py
   ```

2. **Load your data**:
   - Click "Load Data File" and select a `.txt` file containing numbers (separated by spaces, commas, or newlines)

3. **Choose your analysis**:
   - **Individual Algorithm**: Click any algorithm button to run it solo
   - **Run All & Compare**: Execute all three algorithms and see comprehensive performance analysis

4. **View results**:
   - Left panel: Performance statistics, rankings, and speedup analysis
   - Right panel: Complete sorted dataset in descending order

5. **Export** (optional):
   - Click "Save Sorted Data" to export the sorted results

## Dataset Format

Your input file should contain integers:
```
150 42 89 17 203
95 8 176 33 61
```

## Performance Expectations

- **Small datasets** (<100 elements): Minimal difference between algorithms
- **Medium datasets** (1,000-10,000 elements): Noticeable O(n log n) advantage
- **Large datasets** (>10,000 elements): Massive performance gap (10x-100x+ speedup)