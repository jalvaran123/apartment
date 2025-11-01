// CURSOR PATCH: Scroll reveal utility using IntersectionObserver and Framer Motion for Terminal Industries-style section reveals
'use client'

import { useEffect, useRef, useState } from 'react'
import { motion, useInView, Variants } from 'framer-motion'

interface RevealProps {
  children: React.ReactNode
  delay?: number
  direction?: 'up' | 'down' | 'left' | 'right' | 'fade'
  className?: string
  staggerChildren?: boolean
}

const directionVariants: Record<string, Variants> = {
  up: {
    hidden: { opacity: 0, y: 40 },
    visible: { opacity: 1, y: 0 },
  },
  down: {
    hidden: { opacity: 0, y: -40 },
    visible: { opacity: 1, y: 0 },
  },
  left: {
    hidden: { opacity: 0, x: -40 },
    visible: { opacity: 1, x: 0 },
  },
  right: {
    hidden: { opacity: 0, x: 40 },
    visible: { opacity: 1, x: 0 },
  },
  fade: {
    hidden: { opacity: 0 },
    visible: { opacity: 1 },
  },
}

export function Reveal({
  children,
  delay = 0,
  direction = 'up',
  className = '',
  staggerChildren = false,
}: RevealProps) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: '-100px' })

  const variants = directionVariants[direction] || directionVariants.up

  const containerVariants: Variants = staggerChildren
    ? {
        visible: {
          transition: {
            staggerChildren: 0.1,
            delayChildren: delay,
          },
        },
      }
    : {
        visible: {
          transition: {
            delay,
          },
        },
      }

  return (
    <motion.div
      ref={ref}
      initial="hidden"
      animate={isInView ? 'visible' : 'hidden'}
      variants={staggerChildren ? containerVariants : variants}
      className={className}
      transition={{
        duration: 0.6,
        ease: [0.4, 0, 0.2, 1],
      }}
    >
      {staggerChildren ? (
        <motion.div variants={variants}>{children}</motion.div>
      ) : (
        children
      )}
    </motion.div>
  )
}

export function useReveal() {
  const [isVisible, setIsVisible] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
        }
      },
      { threshold: 0.1 }
    )

    if (ref.current) {
      observer.observe(ref.current)
    }

    return () => {
      if (ref.current) {
        observer.unobserve(ref.current)
      }
    }
  }, [])

  return { ref, isVisible }
}

