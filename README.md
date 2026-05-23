# RouteDesk - Terminal Operations Management System

RouteDesk is a professional, Python and PyQt6 based desktop application designed specifically for bus terminal and transportation company operations. It handles dynamic real-time ticket sales, trip management, dynamic pricing, and operator session management.

## Key Features & Implementations

### 1. Robust Operator Authentication & Security
- **Dynamic Registration/Login System:** Replaced the static operator profile with a fully functional `LoginWindow`. If no operators exist in the database, it seamlessly redirects the user to create an initial account. Upon successful login, the operator's actual name dynamically populates the sidebar profile.
- **Secure Access:** Direct execution of the application will not bypass authentication. It halts operation until a valid session is established.

### 2. Intelligent Trip & Status Management
- **Trip Status Updates:** Added a functional toolbar in the Trip Management section. Terminal operators can easily select a trip from the schedule and update its live status (e.g., *Planlandı, Yolcu Alımında, Rötarlı, İptal Edildi*). 
- **Real-Time Data Sync:** Implemented `showEvent` lifecycle hooks across all primary GUI components. Navigating between tabs (e.g., from creating a trip to selling tickets) will instantly load the freshest database records without requiring an application restart.

### 3. Dynamic Seat Layouts & Interactive Ticketing
- **Classic Grid Switching:** Implemented an automatic grid generation system that actively listens to the chosen bus layout (2+2 Standard, 2+1 VIP, 3+1 Special) and perfectly draws the correct seating grid logic with aisles.
- **Live Ticket Price Calculation:** When selecting a trip and entering seat numbers in the "Ticket Sales" module, the application live-fetches the actual price mapped to that specific trip code from the database. It instantly calculates and updates the total preview price in real-time as the operator types.
- **Visual Color Indicators:** Provides clear visual status updates on seat reservation (Gray: Available, Blue: Selected, Red: Occupied, Orange: Reserved) driven dynamically by SQLite ticket records.

### 4. Advanced Dashboard Analytics & Modifications
- **Live Revenue Calculation:** The dashboard doesn't rely on mock data. It directly sums the exact prices of all recorded tickets to display a highly accurate "Daily Revenue" (Günlük Hasılat).
- **Dynamic Occupancy:** Shows genuine ticket vs. capacity metrics (e.g., "12/46") within both the trip tables and dashboard counters.
- **Ticket Cancellation (Refund):** Included a direct "Cancel Selected Ticket" button right under the Recent Ticket Activity feed. Deleting a ticket instantly removes it from the database and rolls back revenue/occupancy metrics safely.

### 5. Native Windows Integration & UI Polish
- **Centralized Application Startup:** Windows will automatically calculate the screen's available geometry and center both the Login and Main Application windows perfectly upon launch.
- **Windows Taskbar Identity (`AppUserModelID`):** Implemented `ctypes.windll.shell32` hooks to give RouteDesk a dedicated Windows identity. This prevents the application from grouping under the generic Python executable logo in the taskbar, forcing it to display the custom RouteDesk logo.
- **Custom Desktop Shortcut Generation:** Converted the base `.png` graphical asset into a proper Windows `.ico` structure and programmatically generated a `RouteDesk.lnk` desktop shortcut that points directly to the virtual environment `pythonw.exe`, hiding the background terminal and mimicking a standard `.exe` installation.
- **Corporate & Legal Submenu:** Transformed the reporting section into a specialized "Contact Us" branch containing company contact information and explicit references to KVKK (Data Protection) and Highway Transportation Regulations.

## Architecture
- **Language:** Python 3
- **GUI Framework:** PyQt6
- **Database:** SQLite3 (Local file-based system)
- **Styling:** Custom QSS (Qt Style Sheets) implementation with dark mode support.
