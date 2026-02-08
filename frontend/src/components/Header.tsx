'use client'

import { useState, useRef, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/context/AuthContext'

export default function Header() {
    const { user, loading, signOut } = useAuth()
    const [dropdownOpen, setDropdownOpen] = useState(false)
    const dropdownRef = useRef<HTMLDivElement>(null)
    const router = useRouter()

    // Close dropdown when clicking outside
    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setDropdownOpen(false)
            }
        }
        document.addEventListener('mousedown', handleClickOutside)
        return () => document.removeEventListener('mousedown', handleClickOutside)
    }, [])

    const handleSignOut = async () => {
        await signOut()
        router.push('/')
        router.refresh()
    }

    // Get user initials
    const getInitials = (email: string) => {
        return email.substring(0, 2).toUpperCase()
    }

    return (
        <header className="sticky top-0 z-50 bg-cream/90 backdrop-blur-md border-b border-cloud">
            <nav className="container-editorial">
                <div className="flex items-center justify-between h-20">

                    {/* Logo */}
                    <Link href="/" className="flex items-center gap-3 group">
                        <div className="relative">
                            <div className="w-10 h-10 bg-navy flex items-center justify-center">
                                <span className="font-display font-bold text-cream text-lg">J</span>
                            </div>
                            <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-gold" />
                        </div>
                        <div className="flex flex-col">
                            <span className="font-display text-xl font-semibold text-navy tracking-tight leading-none">
                                Jobs
                            </span>
                            <span className="text-[10px] uppercase tracking-[0.2em] text-stone">
                                Career Studio
                            </span>
                        </div>
                    </Link>

                    {/* Navigation Links */}
                    <div className="hidden md:flex items-center gap-10">
                        <Link href="/#approach" className="nav-link">Approach</Link>
                        <Link href="/#process" className="nav-link">Process</Link>
                        <Link href="/pricing" className="nav-link">Pricing</Link>
                    </div>

                    {/* CTA / User Menu */}
                    <div className="flex items-center gap-4">
                        {loading ? (
                            <div className="w-8 h-8 rounded-full bg-cloud animate-pulse" />
                        ) : user ? (
                            /* Logged in - User dropdown */
                            <div className="relative" ref={dropdownRef}>
                                <button
                                    onClick={() => setDropdownOpen(!dropdownOpen)}
                                    className="flex items-center gap-2 px-3 py-2 rounded-sm hover:bg-cream-dark transition-colors"
                                >
                                    <div className="w-8 h-8 bg-navy rounded-full flex items-center justify-center">
                                        <span className="text-cream text-xs font-medium">
                                            {getInitials(user.email || 'U')}
                                        </span>
                                    </div>
                                    <svg className="w-4 h-4 text-stone" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                    </svg>
                                </button>

                                {/* Dropdown */}
                                {dropdownOpen && (
                                    <div className="absolute right-0 mt-2 w-56 bg-white border border-cloud rounded-sm shadow-editorial py-1">
                                        <div className="px-4 py-2 border-b border-cloud">
                                            <p className="text-sm font-medium text-navy truncate">{user.email}</p>
                                            <p className="text-xs text-stone">Free Plan</p>
                                        </div>

                                        <Link
                                            href="/upload"
                                            className="block px-4 py-2 text-sm text-charcoal hover:bg-cream-dark"
                                            onClick={() => setDropdownOpen(false)}
                                        >
                                            New Analysis
                                        </Link>

                                        <Link
                                            href="/pricing"
                                            className="block px-4 py-2 text-sm text-charcoal hover:bg-cream-dark"
                                            onClick={() => setDropdownOpen(false)}
                                        >
                                            Upgrade Plan
                                        </Link>

                                        <div className="border-t border-cloud mt-1 pt-1">
                                            <button
                                                onClick={handleSignOut}
                                                className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                                            >
                                                Sign Out
                                            </button>
                                        </div>
                                    </div>
                                )}
                            </div>
                        ) : (
                            /* Not logged in */
                            <>
                                <Link
                                    href="/login"
                                    className="hidden sm:inline-flex text-sm text-charcoal hover:text-navy transition-colors"
                                >
                                    Sign In
                                </Link>
                                <Link
                                    href="/signup"
                                    className="hidden sm:inline-flex px-6 py-2.5 bg-navy text-cream text-sm font-medium
                           transition-all duration-300 hover:bg-navy-light"
                                >
                                    Get Started
                                </Link>
                            </>
                        )}

                        {/* Mobile menu button */}
                        <button className="md:hidden p-2 text-navy hover:text-gold transition-colors">
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 6h16M4 12h16M4 18h16" />
                            </svg>
                        </button>
                    </div>
                </div>
            </nav>
        </header>
    )
}
