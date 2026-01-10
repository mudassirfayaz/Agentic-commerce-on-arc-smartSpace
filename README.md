# SmartSpace Frontend

A React-based frontend for SmartSpace - an autonomous pay-per-use API access gateway with USDC payments.

## Features

- **Landing Page**: Modern, responsive landing page similar to api-hub.ai with SmartSpace branding
- **Authentication**: Login and Signup pages with wallet connection option
- **Dashboard**: Main application dashboard with stats, quick actions, and usage tracking
- **Routing**: React Router setup for seamless navigation between pages

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173`

## Project Structure

```
src/
├── pages/
│   ├── LandingPage.jsx      # Main landing page
│   ├── LandingPage.css      # Landing page styles
│   ├── Login.jsx            # Login page
│   ├── Signup.jsx           # Signup page
│   ├── Auth.css             # Authentication pages styles
│   ├── Dashboard.jsx        # Main dashboard
│   └── Dashboard.css        # Dashboard styles
├── App.jsx                  # Main app component with routing
├── main.jsx                 # React entry point
└── index.css                # Global styles and CSS variables
```

## Routes

- `/` - Landing page
- `/login` - Login page
- `/signup` - Signup page
- `/dashboard` - Main dashboard (protected route)

## Technology Stack

- **React 18** - UI framework
- **React Router DOM** - Client-side routing
- **Vite** - Build tool and dev server
- **CSS** - Custom styling with CSS variables

## Next Steps

- Implement actual authentication logic
- Connect to backend API
- Add USDC wallet integration
- Implement API call functionality
- Add usage tracking and analytics
- Create project and agent management pages

## Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Preview Production Build

```bash
npm run preview
```

