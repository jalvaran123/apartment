'use client';

import React, { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface SideFormDrawerProps {
  isOpen: boolean;
  title: string;
  onClose: () => void;
  onSubmit: (data: any) => void | Promise<void>;
  children: React.ReactNode;
  width?: string;
}

export default function SideFormDrawer({
  isOpen,
  title,
  onClose,
  onSubmit,
  children,
  width = '500px',
}: SideFormDrawerProps) {
  // Prevent body scroll when drawer is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  // Handle ESC key to close
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  const overlayVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1 },
  };

  const drawerVariants = {
    hidden: {
      x: '100%',
      transition: {
        type: 'spring',
        damping: 30,
        stiffness: 300,
      },
    },
    visible: {
      x: 0,
      transition: {
        type: 'spring',
        damping: 30,
        stiffness: 300,
      },
    },
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop/Overlay */}
          <motion.div
            initial="hidden"
            animate="visible"
            exit="hidden"
            variants={overlayVariants}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            aria-hidden="true"
          />

          {/* Side Drawer */}
          <motion.div
            initial="hidden"
            animate="visible"
            exit="hidden"
            variants={drawerVariants}
            className="fixed top-0 right-0 h-full bg-white shadow-2xl z-50 flex flex-col"
            style={{ width: `min(100vw, ${width})` }}
            role="dialog"
            aria-modal="true"
            aria-labelledby="drawer-title"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex items-center justify-between px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-[#9D6DC2] to-[#5A2D82]">
              <h2
                id="drawer-title"
                className="text-xl font-semibold text-white"
              >
                {title}
              </h2>
              <button
                onClick={onClose}
                className="text-white hover:text-gray-200 transition-colors p-1 rounded-full hover:bg-white/20"
                aria-label="Close drawer"
              >
                <svg
                  className="w-6 h-6"
                  fill="none"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Form Content */}
            <div className="flex-1 overflow-y-auto px-6 py-6">
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  const formData = new FormData(e.currentTarget);
                  const data = Object.fromEntries(formData.entries());
                  onSubmit(data);
                }}
                className="space-y-6"
              >
                {children}

                {/* Form Actions */}
                <div className="flex justify-end gap-3 pt-6 border-t border-gray-200 mt-8">
                  <button
                    type="button"
                    onClick={onClose}
                    className="px-6 py-2.5 rounded-lg font-semibold text-gray-700 bg-gray-100 hover:bg-gray-200 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-6 py-2.5 rounded-lg font-semibold text-[#2a2a2a] bg-gradient-to-r from-[#FFA719] to-[#FFCD7B] hover:shadow-lg transition-all transform hover:scale-105"
                  >
                    Save
                  </button>
                </div>
              </form>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

