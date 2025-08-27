# AI Chatbot Frontend

A modern Vue.js frontend for the AI Chatbot application with a corporate design system.

## Features

- **Modern Vue.js 3** with Composition API
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Pinia** for state management
- **Vue Router** for navigation
- **Component-based architecture**
- **Responsive design**
- **Real-time chat interface**
- **Modern corporate UI/UX**

## Tech Stack

- Vue 3.4+
- TypeScript
- Vite
- Tailwind CSS
- Pinia
- Vue Router
- Axios
- Chart.js
- Headless UI

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Start development server:
```bash
npm run dev
```

4. Build for production:
```bash
npm run build
```

## Project Structure

```
src/
├── components/          # Reusable components
│   ├── BaseButton.vue
│   ├── BaseInput.vue
│   ├── BaseModal.vue
│   ├── BaseCard.vue
│   ├── BaseLayout.vue
│   └── ...
├── views/              # Page components
│   ├── Dashboard.vue
│   ├── Login.vue
│   ├── ChatHistory.vue
│   └── ...
├── stores/             # Pinia stores
│   ├── auth.ts
│   └── ...
├── services/           # API services
│   └── api.ts
├── types/              # TypeScript types
│   └── auth.ts
├── composables/        # Vue composables
│   └── useToast.ts
└── router/             # Vue Router config
    └── index.ts
```

## Development

The frontend is designed to work with the existing FastAPI backend. Make sure the backend is running on `http://localhost:8000` before starting the frontend.

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run test` - Run tests

## Design System

The application uses a modern corporate design system with:

- **Primary Colors**: Blue-based palette
- **Typography**: Inter font family
- **Components**: Consistent button, input, and card styles
- **Spacing**: 8px grid system
- **Shadows**: Soft, medium, and strong variants
- **Animations**: Smooth transitions and micro-interactions

## API Integration

The frontend communicates with the FastAPI backend through:

- RESTful API endpoints
- Session-based authentication
- Real-time chat streaming
- File upload handling
- Error handling with user feedback

## Contributing

1. Follow the existing code style
2. Use TypeScript for all new code
3. Write tests for new features
4. Update documentation as needed
