'use client'

import { useEffect, useState } from 'react'
import { Zap, Sparkles, Users, Loader2 } from 'lucide-react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { getCredits, type CreditsInfo } from '@/lib/api'
import { useAuth } from '@/context/AuthContext'
import { motion, AnimatePresence } from 'framer-motion'

/**
 * Displays user's credits usage in the header.
 * Shows tier badge and credits used out of total.
 * Format: "2 / 3 used" or "5 / 30 used"
 */
export default function CreditsDisplay() {
    const { user } = useAuth()
    const pathname = usePathname()
    const [credits, setCredits] = useState<CreditsInfo | null>(null)
    const [loading, setLoading] = useState(true)
    const [isRefreshing, setIsRefreshing] = useState(false)

    useEffect(() => {
        if (!user) {
            setLoading(false)
            return
        }

        const fetchCredits = async () => {
            if (credits) setIsRefreshing(true)
            try {
                const data = await getCredits()
                setCredits(data)
            } catch (err) {
                console.error('Failed to fetch credits:', err)
                // Fallback to default free tier if API fails
                setCredits({
                    credits_remaining: 3,
                    credits_used_this_month: 0,
                    tier: 'free',
                    tier_limit: 3
                })
            } finally {
                setLoading(false)
                setIsRefreshing(false)
            }
        }

        fetchCredits()
    }, [user, pathname])

    // Don't show anything if not logged in
    if (!user) return null

    // Initial loading state
    if (loading && !credits) {
        return (
            <div className="flex items-center gap-2 px-3 py-1.5 bg-cloud/50 rounded-sm animate-pulse min-w-[100px]">
                <div className="w-4 h-4 bg-mist rounded-sm" />
                <div className="w-12 h-4 bg-mist rounded-sm" />
            </div>
        )
    }

    // Use defaults if credits is still null (shouldn't happen with fallback)
    const displayCredits = credits || {
        credits_remaining: 3,
        credits_used_this_month: 0,
        tier: 'free',
        tier_limit: 3
    }

    // Calculate used credits
    const creditsUsed = displayCredits.tier_limit - displayCredits.credits_remaining
    const isLow = displayCredits.credits_remaining <= 1
    const isExhausted = displayCredits.credits_remaining === 0

    // Determine tier icon and styling
    const getTierConfig = () => {
        switch (displayCredits.tier) {
            case 'pro':
                return {
                    icon: <Zap className="w-4 h-4" />,
                    bgColor: 'bg-gold/10',
                    textColor: 'text-gold-dark',
                    label: 'Pro'
                }
            case 'team':
                return {
                    icon: <Users className="w-4 h-4" />,
                    bgColor: 'bg-navy/10',
                    textColor: 'text-navy',
                    label: 'Team'
                }
            default:
                return {
                    icon: <Sparkles className="w-4 h-4" />,
                    bgColor: 'bg-cloud',
                    textColor: 'text-charcoal',
                    label: 'Free'
                }
        }
    }

    const tierConfig = getTierConfig()

    // Determine style based on credits state
    const getDisplayStyle = () => {
        if (isExhausted) {
            return 'bg-red-50 text-red-600 border border-red-100'
        }
        if (isLow && displayCredits.tier === 'free') {
            return 'bg-amber-50 text-amber-700 border border-amber-100'
        }
        return `${tierConfig.bgColor} ${tierConfig.textColor} border border-transparent`
    }

    return (
        <div className="flex items-center gap-2">
            <AnimatePresence mode="wait">
                <motion.div
                    key={`${displayCredits.credits_remaining}-${isRefreshing}`}
                    initial={{ opacity: 0, y: -5 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 5 }}
                    transition={{ duration: 0.2 }}
                >
                    <Link
                        href="/#pricing"
                        className={`flex items-center gap-2 px-3 py-1.5 rounded-sm text-sm font-medium transition-all hover:scale-105 shadow-sm ${getDisplayStyle()}`}
                        title={`${creditsUsed} of ${displayCredits.tier_limit} credits used this month (${displayCredits.credits_remaining} remaining)`}
                    >
                        {isRefreshing ? (
                            <Loader2 className="w-4 h-4 animate-spin opacity-50" />
                        ) : (
                            tierConfig.icon
                        )}
                        <span className="font-bold">{creditsUsed}</span>
                        <span className="text-[11px] opacity-70 uppercase tracking-wider">/ {displayCredits.tier_limit} used</span>
                    </Link>
                </motion.div>
            </AnimatePresence>

            {/* Upgrade prompt - Premium styling */}
            {(isLow || isExhausted) && !isRefreshing && (
                <motion.div
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                >
                    <Link
                        href="/#pricing"
                        className="hidden sm:flex items-center gap-1 px-2 py-1 text-xs text-gold-dark hover:text-gold font-bold transition-colors uppercase tracking-widest"
                    >
                        {isExhausted ? 'Refill →' : 'Upgrade →'}
                    </Link>
                </motion.div>
            )}
        </div>
    )
}
