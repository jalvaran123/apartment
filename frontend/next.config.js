// CURSOR PATCH: Added image optimization config for external images and PWA support
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: [
      'a.storyblok.com',
      'localhost',
      '127.0.0.1',
    ],
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.storyblok.com',
      },
    ],
  },
  // Proxy API requests to Django backend in development
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL
          ? `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`
          : 'http://127.0.0.1:8000/api/:path*',
      },
    ];
  },
};

module.exports = nextConfig;

