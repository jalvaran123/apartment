// CURSOR PATCH: Main landing page component converted from Django template with Terminal Industries-style animations, Framer Motion, and optimized images
'use client'

import { useEffect, useRef, useState } from 'react'
import { motion, useScroll, useTransform } from 'framer-motion'
import { Reveal } from '@/lib/scrollReveal'
import { OptimizedImage } from '@/components/OptimizedImage'
import ScrollSection from '@/components/ScrollSection'
import Link from 'next/link'

const heroHeadlines = [
  'We have reimagined the future of living',
  'through modern apartment design.',
  'Elevating lifestyles by creating exceptional spaces.',
]

// Scroll section items - Terminal Industries-style split-screen layout
const scrollSectionItems = [
  {
    id: 'user-login',
    title: 'User Login System',
    description:
      'Secure user and admin authentication with robust password protection. Multi-level access control ensures that tenants, property managers, and administrators each have appropriate system permissions.',
    // imagePath: '/images/user-login.jpg', // Add later
  },
  {
    id: 'tenant-management',
    title: 'Tenant Management',
    description:
      'Add, view, and edit tenant profiles with comprehensive information tracking. Manage lease agreements, contact details, move-in dates, and tenant history in one centralized location.',
    // imagePath: '/images/tenant-management.jpg', // Add later
  },
  {
    id: 'property-dashboard',
    title: 'Property Dashboard',
    description:
      'Manage apartment listings, unit availability, and property details from a unified dashboard. Track occupancy rates, maintenance status, and property performance metrics at a glance.',
    // imagePath: '/images/property-dashboard.jpg', // Add later
  },
  {
    id: 'payment-tracking',
    title: 'Payment Tracking',
    description:
      'Record and monitor rent payments with automated reminders and payment history. Generate invoices, track late payments, and maintain comprehensive financial records for each property and tenant.',
    // imagePath: '/images/payment-tracking.jpg', // Add later
  },
  {
    id: 'maintenance-requests',
    title: 'Maintenance Requests',
    description:
      'Handle service issues efficiently with a streamlined request system. Track work orders, assign tasks to maintenance staff, and monitor completion status. Keep tenants informed with real-time updates.',
    // isVideo: true,
    // imagePath: '/videos/maintenance.mp4', // Add later
  },
]

export default function Home() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [headerScrolled, setHeaderScrolled] = useState(false)
  const heroCarouselRef = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll({
    target: heroCarouselRef,
    offset: ['start start', 'end start'],
  })
  const heroProgress = useTransform(scrollYProgress, [0, 1], [0, 1])

  useEffect(() => {
    const handleScroll = () => {
      setHeaderScrolled(window.scrollY > 10)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <main className="min-h-screen bg-white">
      {/* Header Navigation */}
      <header
        className={`fixed top-0 left-0 w-full z-[1000] transition-all duration-500 ${
          headerScrolled || mobileMenuOpen
            ? 'bg-white/95 backdrop-blur-xl border-b border-black/5'
            : ''
        } h-[60px] lg:h-[80px]`}
      >
        <nav className="container mx-auto px-6 lg:px-20 h-full flex items-center justify-between">
          <motion.a
            href="#"
            className="text-2xl font-medium text-black no-underline h-[26px] font-primary"
            whileHover={{ opacity: 0.7 }}
            transition={{ duration: 0.2 }}
          >
            Monterde Apartment
          </motion.a>

          <ul className="hidden lg:flex gap-8 list-none">
            {['Home', 'About Us', 'Contact Us'].map((item) => (
              <li key={item}>
                <a
                  href={`#${item.toLowerCase().replace(' ', '')}`}
                  className="text-[15px] font-normal leading-[1.4] tracking-[0.02em] text-black no-underline transition-colors duration-300 hover:text-[#666]"
                >
                  {item}
                </a>
              </li>
            ))}
          </ul>

          <button
            className="lg:hidden block relative z-50 h-10 w-10 bg-transparent border-0 cursor-pointer text-black"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            <motion.span
              className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-5 h-0.5 bg-current"
              animate={{ rotate: mobileMenuOpen ? 45 : 0 }}
              transition={{ duration: 0.3 }}
            >
              <motion.span
                className="absolute top-0 left-0 w-5 h-0.5 bg-current"
                animate={{
                  top: mobileMenuOpen ? 0 : -6,
                  rotate: mobileMenuOpen ? -90 : 0,
                }}
                transition={{ duration: 0.3 }}
              />
              <motion.span
                className="absolute top-0 left-0 w-5 h-0.5 bg-current"
                animate={{
                  top: mobileMenuOpen ? 0 : 6,
                  rotate: mobileMenuOpen ? 90 : 0,
                }}
                transition={{ duration: 0.3 }}
              />
            </motion.span>
          </button>
        </nav>
      </header>

      {/* Mobile Menu */}
      <motion.div
        className={`fixed inset-0 bg-white z-[990] transform transition-transform duration-500 pt-[60px] ${
          mobileMenuOpen ? 'translate-y-0' : '-translate-y-full'
        }`}
        initial={false}
        animate={{ y: mobileMenuOpen ? 0 : '-100%' }}
      >
        <nav className="flex flex-col items-center justify-center h-full">
          <ul className="flex flex-col items-center gap-6 list-none">
            {['Home', 'About Us', 'Contact Us'].map((item) => (
              <li key={item}>
                <a
                  href={`#${item.toLowerCase().replace(' ', '')}`}
                  className="font-primary text-[40px] font-medium leading-[1.25] tracking-[-0.005em] text-black no-underline transition-opacity duration-300 hover:opacity-70"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {item}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </motion.div>

      {/* Hero Video Carousel */}
      <section
        ref={heroCarouselRef}
        className="relative h-[400vh] bg-white"
        id="heroCarousel"
      >
        <div className="sticky top-0 h-screen w-full overflow-hidden">
          {/* Hero Background - Video with fallback image */}
          <div className="absolute inset-0 left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 h-full w-auto max-w-none md:h-auto md:w-full">
            <video
              autoPlay
              loop
              muted
              playsInline
              className="absolute inset-0 h-full w-full object-cover md:h-auto md:w-full"
              preload="auto"
            >
              <source
                src="https://a.storyblok.com/f/337048/x/f0f51ea10f/vid_3-1_prerender_1.mp4"
                type="video/mp4"
              />
            </video>
            {/* Fallback image */}
            <OptimizedImage
              src="/sia/Apt1.png"
              alt="Apartment hero"
              fill
              priority
              objectFit="cover"
              className="absolute inset-0 h-full w-full object-cover"
            />
          </div>

          <div className="absolute inset-0 z-10 bg-black/60" />

          {/* Hero Headlines */}
          <div className="absolute inset-0 z-20 flex flex-col items-center justify-center text-center text-white">
            {heroHeadlines.map((headline, index) => {
              const start = index * 0.15
              const end = start + 0.25
              const opacity = useTransform(
                heroProgress,
                [start, start + 0.1, end - 0.1, end],
                [0, 1, 1, 0]
              )
              const y = useTransform(
                heroProgress,
                [start, start + 0.1],
                [40, 0]
              )

              return (
                <motion.h2
                  key={index}
                  className="absolute w-full max-w-[80ch] px-4 text-[clamp(48px,8vw,120px)] font-medium leading-[1.05] tracking-[-0.02em]"
                  style={{ opacity, y }}
                >
                  {headline}
                </motion.h2>
              )
            })}
          </div>

          {/* Scroll Indicator */}
          <motion.div
            className="absolute bottom-10 left-1/2 -translate-x-1/2 z-30"
            initial={{ opacity: 1, y: 0 }}
            animate={{ y: [0, -10, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <p className="font-body text-sm uppercase tracking-[0.1em] text-white/80">
              Scroll to explore
            </p>
          </motion.div>
        </div>
      </section>

      {/* Notch Separator */}
      <div className="bg-white">
        <div className="h-12 w-full bg-black clip-path-[path('M_0_0_L_1_0_L_1_0.2_C_0.75_0.5,0.25_0.5,0_0.2_Z')]" />
      </div>

      {/* Value Proposition */}
      <section className="bg-white text-black py-[clamp(120px,15vw,200px)]">
        <div className="container mx-auto px-6 lg:px-20">
          <Reveal direction="fade" delay={0.1}>
            <h2 className="text-center font-primary text-[clamp(40px,6vw,80px)] font-medium leading-[1.1] tracking-[-0.015em]">
              Imagine your home as an{' '}
              <span className="font-semibold">intelligent</span>{' '}
              <span className="font-semibold">sanctuary</span> perfectly
              connecting comfort to community.
            </h2>
          </Reveal>
        </div>
      </section>

      {/* Terminal Industries-style Scroll Section */}
      <ScrollSection items={scrollSectionItems} />

      {/* Testimonial Full Width */}
      <section className="relative w-full overflow-hidden">
        <OptimizedImage
          src="/sia/Apt1.png"
          alt="Testimonial background"
          fill
          objectFit="cover"
          className="absolute inset-0"
        />
        <div className="absolute inset-0 bg-black/60" />
        <div className="container mx-auto relative text-center text-white py-[clamp(80px,12vw,160px)]">
          <Reveal direction="up" delay={0.2}>
            <blockquote className="max-w-[900px] mx-auto font-primary text-[clamp(24px,4vw,48px)] font-medium leading-[1.3]">
              "This is not just an apartment, it's a lifestyle revolution. The
              attention to detail and smart technology integration is unlike
              anything we've experienced in modern living."
            </blockquote>
            <footer className="mt-6">
              <p className="text-lg font-normal mt-2 opacity-80">
                Alexandra Martinez
              </p>
              <p className="text-lg font-normal mt-2 opacity-80">
                Resident, LuxeLiving Downtown
              </p>
            </footer>
          </Reveal>
        </div>
      </section>

      {/* How It Works Hero */}
      <section className="bg-white relative overflow-hidden py-[clamp(96px,10vw,192px)]">
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-1 h-1 bg-[rgba(204,255,0,0.2)] rounded-full shadow-[0_0_15rem_5rem_rgba(204,255,0,0.2)]" />
        <div className="container mx-auto relative z-10 flex flex-col items-center text-center">
          <Reveal direction="up" delay={0}>
            <p className="text-[#666] font-medium uppercase tracking-[0.05em] text-[13px] mb-6">
              Experience The Difference
            </p>
          </Reveal>
          <Reveal direction="up" delay={0.15}>
            <h2 className="font-primary font-medium text-[clamp(40px,6vw,72px)] leading-[1.1] tracking-[-0.015em] max-w-[60ch] mb-12">
              Revolutionary living spaces that transform your lifestyle from
              entry to rooftop
            </h2>
          </Reveal>
          <Reveal direction="up" delay={0.3}>
            <Link
              href="/auth/login/"
              className="text-black font-medium uppercase tracking-[0.05em] text-[13px] underline underline-offset-2 transition-colors duration-300 hover:text-[#666]"
            >
              SCHEDULE A TOUR
            </Link>
          </Reveal>
        </div>
      </section>

      {/* CTA Future Section */}
      <section className="bg-white py-[clamp(120px,15vw,200px)]">
        <div className="container mx-auto px-6 lg:px-20">
          <Reveal direction="fade" delay={0.1}>
            <h1 className="text-center font-primary text-[clamp(48px,8vw,120px)] font-medium leading-[1.05] tracking-[-0.02em] text-black mb-12">
              The home of the future starts today.
            </h1>
          </Reveal>
          <div className="text-center mt-12">
            <Reveal direction="up" delay={0.2}>
              <motion.a
                href="/auth/login/"
                className="inline-block px-16 py-6 bg-[#673ab7] text-white no-underline rounded-[50px] font-semibold text-xl transition-all duration-300 will-change-transform"
                whileHover={{
                  y: -4,
                  boxShadow: '0 10px 30px rgba(103, 58, 183, 0.3)',
                }}
                whileTap={{ scale: 0.98 }}
              >
                Get Started Now
              </motion.a>
            </Reveal>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-[#1a1a1a] text-white py-[clamp(80px,10vw,100px)] pb-10">
        <div className="container mx-auto px-6 lg:px-20">
          <div className="grid grid-cols-[repeat(auto-fit,minmax(200px,1fr))] gap-10 pb-16 md:grid-cols-[repeat(12,1fr)] lg:grid-cols-[repeat(12,1fr)]">
            <div className="hidden lg:block lg:col-span-5" />
            <div className="col-span-6 md:col-span-2">
              <h6 className="font-primary text-xs font-medium uppercase tracking-[0.1em] text-white/60 mb-6">
                Living
              </h6>
              <ul className="list-none flex flex-col gap-4">
                {['Floor Plans', 'Amenities', 'Virtual Tour'].map((item) => (
                  <li key={item}>
                    <a
                      href={`#${item.toLowerCase().replace(' ', '-')}`}
                      className="text-[15px] font-normal leading-[1.75] text-white no-underline transition-colors duration-300 hover:text-white/70"
                    >
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
            <div className="col-span-6 md:col-span-2">
              <h6 className="font-primary text-xs font-medium uppercase tracking-[0.1em] text-white/60 mb-6">
                Company
              </h6>
              <ul className="list-none flex flex-col gap-4">
                {['About Us', 'Community', 'Contact'].map((item) => (
                  <li key={item}>
                    <a
                      href={`#${item.toLowerCase().replace(' ', '-')}`}
                      className="text-[15px] font-normal leading-[1.75] text-white no-underline transition-colors duration-300 hover:text-white/70"
                    >
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
            <div className="col-span-12 md:col-span-3">
              <h6 className="font-primary text-xs font-medium uppercase tracking-[0.1em] text-white/60 mb-6">
                VISIT US
              </h6>
              <ul className="list-none flex flex-col gap-4">
                <li>
                  <Link
                    href="/auth/login/"
                    className="text-[15px] font-normal leading-[1.75] text-white no-underline transition-colors duration-300 hover:text-white/70"
                  >
                    Schedule your private tour today.
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-white/20 pt-10 flex flex-col gap-8 items-center md:flex-row md:justify-between md:items-center">
            <a
              href="#"
              className="font-primary text-[19px] font-medium text-white no-underline h-6"
            >
              Monterde Apartment
            </a>
            <p className="text-xs text-white/50 text-center">
              Copyright Monterde Apartment © 2025 All Rights Reserved
            </p>
          </div>
        </div>
      </footer>
    </main>
  )
}

