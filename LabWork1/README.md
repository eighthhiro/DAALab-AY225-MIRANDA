# LabWork1: Classic vs Optimized Bubble Sort

## Overview

This program compares two implementations of the bubble sort algorithm:

- **Classic Bubble Sort**: Always performs n-1 passes through the array, regardless of whether the data becomes sorted earlier
- **Optimized Bubble Sort**: Includes an early exit mechanism that stops when no swaps occur in a pass, indicating the array is already sorted

The GUI displays detailed performance metrics including execution time, number of passes performed, and a side-by-side comparison showing when the optimization provides benefits.

**Key Insight**: The optimized version excels with nearly-sorted data but may actually be slower on completely randomized data due to the overhead of checking the swap flag on every pass.

## How to Execute

1. **Run the program**:
   ```bash
   python sorting_gui_bubble_variants.py
   ```

2. **Load your data**:
   - Click "Load Data File" and select a `.txt` file containing numbers (separated by spaces, commas, or newlines)

3. **Choose a sorting method**:
   - **Classic Bubble Sort**: Run the traditional implementation
   - **Optimized Bubble Sort**: Run the early-exit version
   - **Compare Both**: Run both algorithms and see detailed performance analysis

4. **View results**:
   - Left panel: Statistics (time, passes, analysis)
   - Right panel: Sorted data in descending order

5. **Export** (optional):
   - Click "Save Sorted Data" to export results to a text file

## Dataset Format

Your input file should contain integers separated by spaces, commas, or newlines:
```
42 17 93 8 56
21 99 3 71 44
```