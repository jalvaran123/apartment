# Apartment Management - Next.js Frontend

This is the Next.js frontend for the Apartment Management system with a modern side drawer UI.

## Features

- **SideFormDrawer Component**: Reusable slide-in drawer component with Framer Motion animations
- **Baselane-style UI**: Clean, modern interface with smooth animations
- **Form Integration**: Seamless integration with Django backend API

## Installation

```bash
cd frontend
npm install
```

## Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Project Structure

```
frontend/
├── app/
│   ├── properties/
│   │   └── page.tsx          # Example Properties page
│   ├── globals.css
│   └── layout.tsx
├── components/
│   ├── ui/
│   │   └── SideFormDrawer.tsx # Main drawer component
│   └── forms/
│       └── PropertyForm.tsx  # Example form component
├── package.json
└── tsconfig.json
```

## Usage Example

```tsx
import SideFormDrawer from '@/components/ui/SideFormDrawer';
import PropertyForm from '@/components/forms/PropertyForm';

const [isDrawerOpen, setIsDrawerOpen] = useState(false);

<button onClick={() => setIsDrawerOpen(true)}>Add Property</button>

<SideFormDrawer
  isOpen={isDrawerOpen}
  title="Add Property"
  onClose={() => setIsDrawerOpen(false)}
  onSubmit={handleAddProperty}
>
  <PropertyForm />
</SideFormDrawer>
```

