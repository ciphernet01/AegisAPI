# AegisAPI Frontend

React + TypeScript dashboard for the Zombie API Discovery and Defence Platform.

## Quick Start

### Prerequisites
- Node.js >= 18.0.0
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

Dashboard will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/        # Reusable UI components
│   ├── pages/            # Page components (routes)
│   ├── hooks/            # Custom React hooks
│   ├── services/         # API client & utilities
│   ├── types/            # TypeScript type definitions
│   ├── styles/           # Global & component styles
│   ├── App.tsx           # Main app component
│   └── main.tsx          # Entry point
├── tests/                # Unit & integration tests
├── public/               # Static assets
├── vite.config.ts        # Vite configuration
└── tsconfig.json         # TypeScript configuration
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run test` - Run tests
- `npm run test:ui` - Run tests with UI
- `npm run test:coverage` - Generate coverage report
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier
- `npm run type-check` - Check TypeScript types

## Key Features

- **API Inventory Dashboard** - Visual overview of all discovered APIs
- **Risk Heatmap** - Color-coded security risk visualization
- **Advanced Filtering** - Search and filter APIs by status, risk level, owner
- **Remediation Tracking** - Monitor security gap fixes
- **Decommissioning Workflows** - Guided UI for API shutdown
- **Real-time Alerts** - Notifications for new/high-risk APIs
- **Compliance Reports** - Export audit-ready reports

## State Management

Uses Zustand for global state management. Store configurations are in `src/services/store.ts`.

## API Integration

All backend API calls are handled through `src/services/apiClient.ts`. 

Environment variables:
- `VITE_API_URL` - Backend API base URL (default: http://localhost:8000)

## Testing

Uses Vitest for unit tests and React Testing Library for component tests.

```bash
npm run test
npm run test:coverage
```

## Code Style

- **Formatter**: Prettier
- **Linter**: ESLint
- **Language**: TypeScript with strict mode enabled

Run checks before committing:

```bash
npm run lint
npm run format:check
npm run type-check
```

## Troubleshooting

### Port Already in Use
If port 3000 is busy, Vite will use the next available port.

### API Integration Issues
Check that backend is running on `VITE_API_URL` and CORS is properly configured.

### Build Errors
Clear node_modules and reinstall:
```bash
rm -rf node_modules
npm install
npm run build
```

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on:
- Branching strategy
- Commit message format
- Pull request process
- Code style standards
