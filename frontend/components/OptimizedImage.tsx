// CURSOR PATCH: Optimized image wrapper for better performance with lazy loading and blur placeholders
'use client'

import Image from 'next/image'
import { useState } from 'react'

interface OptimizedImageProps {
  src: string
  alt: string
  width?: number
  height?: number
  priority?: boolean
  className?: string
  fill?: boolean
  objectFit?: 'cover' | 'contain' | 'fill' | 'none' | 'scale-down'
}

export function OptimizedImage({
  src,
  alt,
  width,
  height,
  priority = false,
  className = '',
  fill = false,
  objectFit = 'cover',
}: OptimizedImageProps) {
  const [isLoading, setIsLoading] = useState(true)

  if (fill) {
    return (
      <div className={`relative ${className}`}>
        {isLoading && (
          <div className="absolute inset-0 bg-gray-200 animate-pulse" />
        )}
        <Image
          src={src}
          alt={alt}
          fill
          priority={priority}
          className={`object-${objectFit} ${isLoading ? 'opacity-0' : 'opacity-100'} transition-opacity duration-500`}
          onLoad={() => setIsLoading(false)}
          onError={() => setIsLoading(false)}
          sizes="100vw"
          unoptimized={src.startsWith('http')}
        />
      </div>
    )
  }

  return (
    <div className={`relative ${className}`}>
      {isLoading && (
        <div className="absolute inset-0 bg-gray-200 animate-pulse" />
      )}
      <Image
        src={src}
        alt={alt}
        width={width || 1920}
        height={height || 1080}
        priority={priority}
        className={`object-${objectFit} ${isLoading ? 'opacity-0' : 'opacity-100'} transition-opacity duration-500`}
        onLoad={() => setIsLoading(false)}
        onError={() => setIsLoading(false)}
        loading={priority ? undefined : 'lazy'}
      />
    </div>
  )
}

