# TitanView | Ultra-Large File Viewer

**TitanView** is a high-performance desktop application designed to open, view and search massive text files (2GB, 10GB, 50GB, 100GB+) instantly.

Unlike standard text editors that try to load the entire file into RAM, TitanView uses **Memory Mapping (mmap)** to create a direct window into the file on your hard drive, allowing it to run smoothly on even modest hardware without crashes.

## Key Features

### Performance

* **Instant Loading:** Open multi-gigabyte log files in milliseconds.

* **Memory Efficient:** Uses minimal RAM regardless of total file size.

* **Background Processing:** Search operations run on separate threads, ensuring the UI remains responsive.

### Advanced Search

* **Smart Scan All:** Finds every occurrence of a string across the entire file and lists them in a dedicated History Tab.

* **Context Highlighting:** Clicking a search result instantly jumps to that location and highlights the entire row for immediate context.

* **Navigation:** Standard Next/Previous search buttons for quick traversal within the current view or across the file.

### Bookmarking and Export

* **Floating Action Menu:** Select any text to trigger a popup menu for quick actions.

* **One-Click Bookmarks:** Save specific locations with custom names for future reference.

* **Export Selection:** Save specific chunks of text (e.g., error logs) to a separate file without loading the whole document.

* **Management:** Reorder or bulk-delete bookmarks via the sidebar interface.

### Professional UI

* **Dual Theme Support:** Includes a High Contrast Dark Mode for low eye strain and a Soft Paper Light Mode for high readability.

* **Timeline Scrubber:** A top-mounted slider allows users to navigate through the file structure instantly.

* **Status Bar:** Displays real-time Byte Offset and file position percentage.

## Prerequisites

To run TitanView from the source, you need Python installed.

1. **Python 3.8+**

2. **PyQt6 Library**
