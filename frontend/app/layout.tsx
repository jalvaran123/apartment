// CURSOR PATCH: Updated with proper metadata, fonts, and PWA support for landing page
import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Monterde Apartment | Reinventing the Future of Living',
  description: 'Modern apartment living with intelligent design and exceptional spaces. Experience the future of living today.',
  themeColor: '#673ab7',
  manifest: '/manifest.json',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="antialiased">{children}</body>
    </html>
  )
}

