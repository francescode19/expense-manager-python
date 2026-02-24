# expense-manager-python

A simple desktop application built with Python and Tkinter. It allows users to create, view, analyze, and export their personal expenses. All data is stored locally using SQLite, and users can visualize monthly spending trends through charts generated with Matplotlib.

## Technologies used:

### Core application
- Python 3  
- Tkinter (GUI)  
- SQLite (local database)

### Additional libraries
- Matplotlib (monthly expense charts)  
- CSV module (data export)  
- datetime (date handling)

## Architecture:

### Application flow
- The user interacts with a Tkinter-based graphical interface.
- Inputs (item name, amount, date, category) are validated before being saved.
- Data is stored in a local SQLite database through dedicated helper functions.
- Users can view all expenses in a table, delete entries, calculate the total spent, or generate a monthly spending chart.
- Expenses can be exported to a CSV file for external use.

### Internal communication
- The GUI communicates with the database through a separate module (`db.py`), keeping the code organized and easy to maintain.

## Features:

### Expense management
- Add new expenses with:
  - Item name  
  - Amount  
  - Date (auto-filled with today’s date)  
  - Category  

### Expense control
- View all expenses in a table  
- Delete selected entries  
- Calculate the total amount spent  

### Data visualization
- Generate a monthly spending chart using Matplotlib  
- Visualize spending trends over time  

### Data export
- Export all expenses to a CSV file  
- Includes ID, item name, amount, date, and category  

## Future Improvements:

- UI enhancements: improve layout, spacing, and overall design  
- Custom categories: allow users to create and manage their own categories  
- Search & filters: filter expenses by date range, category, or amount 
- Settings panel: choose currency, default date format, export location  
- Multi-language support: English/Italian toggle  

## About this project:

This project was created as a personal exercise to learn and practice Python application development.  
It helped me understand how to:

- build a GUI using Tkinter  
- structure an application using classes  
- interact with a local SQLite database  
- generate charts with Matplotlib  
- export data in CSV format  
- organize a small but complete desktop application  
