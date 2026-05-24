# 🚌 RouteDesk — Terminal Operations Management System

<p align="center">
  <img src="src/assets/icon.png" width="100" alt="RouteDesk Logo" />
</p>

<p align="center">
  <b>A modern, offline-first desktop ticketing and operations management software for bus terminals.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PyQt6-Framework-41CD52?style=flat&logo=qt&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=flat&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/Next.js-15-black?style=flat&logo=next.js&logoColor=white" />
  <img src="https://img.shields.io/badge/TailwindCSS-v4-06B6D4?style=flat&logo=tailwindcss&logoColor=white" />
</p>

---

## 📌 About

**RouteDesk** is a fully offline-capable desktop management application built for local bus terminals, transportation agencies, and VIP shuttle services. It provides an integrated terminal operations ecosystem covering trip scheduling, dynamic seat layout management, ticket sales, and customer records.

The project also includes a **corporate marketing website** and a **remote admin panel** — all living within the same repository.

---

## 🗂️ Project Structure

```
RouteDesk/
│
├── src/                        # Desktop application (PyQt6)
│   ├── assets/                 # Icons and images
│   ├── components/             # Shared components (e.g., Sidebar)
│   ├── database/               # SQLite database manager
│   ├── styles/                 # QSS theme files
│   ├── ui/                     # All screen modules
│   └── main.py                 # Application entry point
│
├── website/                    # Corporate website (Next.js 15)
│   ├── src/
│   │   ├── app/
│   │   │   ├── admin/          # Hidden admin management panel (/admin)
│   │   │   ├── api/admin/      # Login / Logout API routes
│   │   │   ├── gizlilik/       # Privacy Policy page
│   │   │   ├── hizmet-sartlari/ # Terms of Service page
│   │   │   ├── cerez-politikasi/ # Cookie Policy page
│   │   │   └── page.tsx        # Landing page
│   │   ├── components/         # Hero, Features, Pricing, Contact, etc.
│   │   ├── lib/db.ts           # better-sqlite3 database connector
│   │   └── middleware.ts       # Admin authentication middleware
│   └── package.json
│
├── screenshots/                # Application screenshots
├── docs/                       # Additional documentation
└── README.md
```

---

## 🖥️ Desktop Application Features

### 🔐 Authentication
- Dynamic operator registration and login system (SQLite-backed)
- Auto-redirect to registration screen on first launch
- Password-protected sessions

### ✈️ Trip Management
- Full trip creation with company, driver, plate, platform, route, and price
- Automatic trip code generation
- Status management: Planned / Boarding / Delayed / Cancelled
- Live search and filter

### 🎫 Quick Ticket Sales
- 3-step sales workflow: Passenger Info → Trip Selection → Seat & Payment
- Auto-fill customer data by phone number lookup
- Multiple payment methods: Cash / Credit Card / Bank Transfer
- Turkish-localized "Yes/No" confirmation dialogs (Evet/Hayır)

### 💺 Dynamic Seat Layout
- Support for 2+2 / 2+1 / 3+1 bus configurations
- Real-time occupied/available seat visualization
- Click on any seat to view passenger information

### 📋 Control Panel (Dashboard)
- Today's ticket sales, active trips, and occupancy rate statistics
- Live Departure Board
- Recent ticket transaction feed
- One-click ticket cancellation

### 👥 Customer Management
- Customer registration, listing, and search
- Auto-fill on ticket form via phone number lookup

### ⚙️ System Settings
- Company name, terminal name, printer preference configuration
- Database backup and restore (SQLite file export)
- CSV data export

### 🔧 Remote Maintenance Mode
- Activate/deactivate maintenance mode from the web admin panel
- While maintenance is active, the desktop app refuses to open and displays an informational message to the operator

---

## 🌐 Corporate Website

The project includes a fully isolated Next.js 15 website, completely separate from the desktop application codebase.

### Sections
| Section | Description |
|---|---|
| **Hero** | Application mission statement and CTA |
| **Features** | 6 core module highlights |
| **Platform Showcase** | Real application screenshots in UI frames |
| **Workflow** | 5-step operational process walkthrough |
| **Why Desktop** | Advantages of native desktop over web-based tools |
| **Use Cases** | Industry-specific usage scenarios |
| **Pricing** | Starter / Business / Enterprise licensing tiers |
| **Contact** | Formspree AJAX-powered demo request form (no page redirect) |
| **Legal Pages** | Privacy Policy (KVKK), Terms of Service, Cookie Policy |

### Technical Highlights
- **Framework:** Next.js 15 (App Router)
- **Styling:** Tailwind CSS v4
- **Icons:** Lucide React
- **Form:** Formspree AJAX (seamless, no redirect)
- **Custom scrollbar:** Webkit-styled scrollbar matching the dark theme
- **Favicon:** Application's own `.ico` / `.png` icon across all pages

---

## 🔒 Admin Management Panel (`/admin`)

Hidden from the public website — accessible only to authorized administrators via the `/admin` route.

### Tabs & Capabilities
| Tab | Functions |
|---|---|
| **Trip Management** | List all trips, update status, delete |
| **Ticket Cancellations** | List recent tickets and cancel/delete |
| **Customers** | List registered customers and delete |
| **Operators** | List system operators and delete (with ID reset) |
| **System Maintenance** | Remotely lock/unlock the desktop application |

### Security
- Route protection via Next.js Middleware
- `httpOnly` cookie-based session (8-hour expiry)
- `sameSite: strict` CSRF protection
- All destructive actions confirmed via custom themed modals (no native browser `alert`/`confirm`/`prompt`)

### Live Database Connection
The admin panel connects directly to the desktop application's SQLite database (`routedesk.db`) via `better-sqlite3`. Every action performed in the admin panel (trip deletion, ticket cancellation, maintenance mode toggle) is instantly reflected in the desktop application.

---

## 🚀 Getting Started

### Desktop Application

```bash
# Install dependencies
pip install PyQt6

# Run the application
python src/main.py
```

### Website (Development)

```bash
cd website
npm install
npm run dev
# Open: http://localhost:3000
```

### Admin Panel
```
http://localhost:3000/admin
```

---

## 💻 Tech Stack

### Desktop
| Technology | Purpose |
|---|---|
| Python 3.10+ | Primary language |
| PyQt6 | GUI framework |
| SQLite | Local database |
| ctypes (Windows) | AppUserModelID — custom taskbar icon |

### Website & Admin
| Technology | Purpose |
|---|---|
| Next.js 15 | React framework (App Router) |
| Tailwind CSS v4 | Styling system |
| Lucide React | Icon library |
| better-sqlite3 | Admin panel DB connector |
| Formspree | Contact form API |

---

## 📸 Screenshots

| Control Panel | Trip Management | Ticket Sales |
|---|---|---|
| ![Dashboard](screenshots/media__1779578497908.png) | ![Trips](screenshots/media__1779577956914.png) | ![Tickets](screenshots/media__1779577969553.png) |

---

## 👤 Developer

**İbrahim Can Düven**  
📧 ibrahimcanduven1@gmail.com  
📍 Balıkesir, Turkey

---

## 📄 License

This project is developed for private use. Unauthorized copying or distribution is not permitted.

---

<p align="center">Made with ❤️ for professional transit operations</p>
