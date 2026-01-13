# SDA - Sorting in Descending Algorithms

A Python application for analyzing and comparing sorting algorithm performance with both command-line and graphical interfaces.

## Overview

This project provides tools to sort numerical data in descending order using three different sorting algorithms: Bubble Sort, Insertion Sort, and Merge Sort. You can analyze their performance, compare execution times, and export the sorted results.

## Files

### sorting-cli.py
Command-line interface version of the sorting analyzer.

**Features:**
- Interactive text-based menu system
- Load numerical data from .txt files
- Run individual sorting algorithms or compare all three
- View performance rankings (fastest to slowest)
- Export sorted data to text files
- Real-time execution time measurements

**Usage:**
```bash
python sorting-cli.py
```

Follow the on-screen prompts to:
1. Load your data file (numbers separated by spaces, commas, or newlines)
2. Select a sorting algorithm (1-3) or run all algorithms (4)
3. View results and performance metrics
4. Download sorted data (5)
5. Load a new file (6) or exit (7)

### sorting-gui.py
Graphical user interface version with the same functionality in a modern, user-friendly window.

**Features:**
- Modern graphical interface with intuitive controls
- File browser for easy data loading
- Live data preview panel
- Scrollable results display
- Progress indicators during sorting
- Performance comparison visualization
- File save dialog for exports
- Multi-threaded processing (UI remains responsive during sorting)

**Usage:**
```bash
python sorting-gui.py
```

Use the interface to:
1. Click "Load File" to browse and select your data file
2. View a preview of your loaded data
3. Click any sorting algorithm button to run it
4. View detailed results in the results panel
5. Click "Download Sorted Data" to save the output

## Requirements

**For sorting-cli.py:**
- Python 3.6 or higher
- No external dependencies (uses only standard library)

**For sorting-gui.py:**
- Python 3.6 or higher
- tkinter (usually included with Python)

## Input File Format

Both programs accept text files containing numbers in any of these formats:
- Space-separated: `45 23 67 12 89`
- Comma-separated: `45, 23, 67, 12, 89`
- Line-separated:
  ```
  45
  23
  67
  12
  89
  ```
- Mixed formats work too!

Negative numbers are supported: `-5 10 -3 20`

## Sorting Algorithms

1. **Bubble Sort**: Simple comparison-based algorithm. Best for small datasets or educational purposes.
   
2. **Insertion Sort**: Efficient for small datasets or nearly sorted data.
   
3. **Merge Sort**: Divide-and-conquer algorithm. Most efficient for large datasets.

All algorithms sort numbers in **descending order** (largest to smallest).

## Output

Both programs provide:
- Sorted data preview
- Execution time in seconds (6 decimal precision)
- Performance ranking when running all algorithms
- Option to export results to a text file (one number per line)

## Example

**Input file (numbers.txt):**
```
45 23 67 12 89 34 56 78
```

**Output:**
```
Sorted Data: [89, 78, 67, 56, 45, 34, 23, 12]
Time Taken: 0.000023 seconds
```

## Tips

- **Small datasets (< 100 items)**: All algorithms perform similarly
- **Medium datasets (100-1000 items)**: Merge Sort starts to show advantages
- **Large datasets (> 1000 items)**: Merge Sort significantly outperforms others
- Use the CLI version for automation or scripting
- Use the GUI version for interactive exploration and visualization

## License

This project is provided as-is for educational and practical use.