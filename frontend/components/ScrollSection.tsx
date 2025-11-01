// CURSOR PATCH: Terminal Industries-style scroll section with split-screen layout and smooth content transitions
'use client'

import { useRef } from 'react'
import { motion, useScroll, useTransform } from 'framer-motion'
import { OptimizedImage } from './OptimizedImage'

interface ScrollSectionItem {
  id: string
  title: string
  description: string
  imagePath?: string
  isVideo?: boolean
}

interface ScrollSectionProps {
  items: ScrollSectionItem[]
}

export default function ScrollSection({ items }: ScrollSectionProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ['start start', 'end end'],
  })

  return (
    <section
      ref={containerRef}
      className="relative bg-white will-change-transform"
      style={{ height: `${items.length * 100}vh` }}
      aria-label="Feature showcase"
    >
      {/* Sticky container for split-screen */}
      <div className="sticky top-0 h-screen overflow-hidden">
        <div className="container mx-auto h-full px-6 lg:px-20">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-16 h-full items-center">
            {/* Left: Text Content */}
            <div className="flex flex-col justify-center h-full py-20 lg:py-0 lg:min-h-[500px]">
              <div className="relative h-[400px] lg:h-[500px]">
                {items.map((item, index) => {
                  // Calculate opacity and position for each item based on scroll
                  const sectionStart = index / items.length
                  const sectionEnd = (index + 1) / items.length
                  const sectionMid = (sectionStart + sectionEnd) / 2
                  const fadeWindow = 0.15 // Fade in/out window

                  const opacity = useTransform(
                    scrollYProgress,
                    (progress) => {
                      if (progress < sectionStart - fadeWindow) return 0
                      if (progress > sectionEnd + fadeWindow) return 0
                      if (
                        progress >= sectionStart - fadeWindow &&
                        progress <= sectionStart
                      ) {
                        return (progress - (sectionStart - fadeWindow)) / fadeWindow
                      }
                      if (progress >= sectionStart && progress <= sectionEnd) return 1
                      if (progress >= sectionEnd && progress <= sectionEnd + fadeWindow) {
                        return 1 - (progress - sectionEnd) / fadeWindow
                      }
                      return 0
                    }
                  )

                  const y = useTransform(scrollYProgress, (progress) => {
                    const distanceFromMid = Math.abs(progress - sectionMid)
                    if (distanceFromMid > 0.1) {
                      return progress < sectionMid ? 30 : -30
                    }
                    return 0
                  })

                  return (
                    <motion.div
                      key={item.id}
                      className="absolute inset-0 flex flex-col justify-center"
                      style={{
                        opacity,
                        y,
                      }}
                    >
                      <motion.h2
                        className="font-primary text-[clamp(32px,5vw,64px)] font-medium leading-[1.1] tracking-[-0.02em] text-black mb-6"
                        initial={{ opacity: 0 }}
                        style={{ opacity: 1 }}
                      >
                        {item.title}
                      </motion.h2>
                      <motion.p
                        className="font-body text-[clamp(16px,2vw,20px)] font-normal leading-[1.6] text-[#666] max-w-[600px]"
                        initial={{ opacity: 0 }}
                        style={{ opacity: 1 }}
                      >
                        {item.description}
                      </motion.p>
                    </motion.div>
                  )
                })}
              </div>
            </div>

            {/* Right: Media Content */}
            <div className="flex items-center justify-center h-full py-20 lg:py-0">
              <div className="relative w-full h-[400px] lg:h-[600px] rounded-2xl overflow-hidden bg-gray-100">
                {items.map((item, index) => {
                  const sectionStart = index / items.length
                  const sectionEnd = (index + 1) / items.length
                  const sectionMid = (sectionStart + sectionEnd) / 2
                  const fadeWindow = 0.12

                  const opacity = useTransform(scrollYProgress, (progress) => {
                    const distanceFromMid = Math.abs(progress - sectionMid)
                    if (distanceFromMid > fadeWindow) return 0
                    return 1 - distanceFromMid / fadeWindow
                  })

                  const scale = useTransform(scrollYProgress, (progress) => {
                    const distanceFromMid = Math.abs(progress - sectionMid)
                    if (distanceFromMid > 0.15) return 0.92
                    return 1
                  })

                  return (
                    <motion.div
                      key={item.id}
                      className="absolute inset-0"
                      style={{
                        opacity,
                        scale,
                      }}
                    >
                      {item.isVideo ? (
                        // Video placeholder - will be replaced later
                        <div className="bg-gradient-to-br from-gray-200 to-gray-300 h-full w-full rounded-2xl flex items-center justify-center">
                          <div className="text-center">
                            <div className="text-4xl mb-2">🎬</div>
                            <span className="text-gray-500 text-sm font-medium">
                              Video: {item.title}
                            </span>
                          </div>
                        </div>
                      ) : item.imagePath ? (
                        // Image from public folder
                        <OptimizedImage
                          src={item.imagePath}
                          alt={item.title}
                          fill
                          objectFit="cover"
                          className="rounded-2xl"
                        />
                      ) : (
                        // Placeholder div with subtle gradient
                        <div className="bg-gradient-to-br from-gray-200 to-gray-300 h-full w-full rounded-2xl flex items-center justify-center">
                          <div className="text-center px-6">
                            <div className="text-4xl mb-3">📸</div>
                            <span className="text-gray-500 text-sm font-medium">
                              {item.title}
                            </span>
                            <p className="text-gray-400 text-xs mt-2">
                              Image placeholder
                            </p>
                          </div>
                        </div>
                      )}
                    </motion.div>
                  )
                })}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

