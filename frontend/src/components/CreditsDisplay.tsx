'use client'

import { useEffect, useState } from 'react'
import { Zap, Sparkles, Users } from 'lucide-react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { getCredits, type CreditsInfo } from '@/lib/api'
import { useAuth } from '@/context/AuthContext'

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

    useEffect(() => {
        if (!user) {
            setLoading(false)
            return
        }

        const fetchCredits = async () => {
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
            }
        }

        fetchCredits()
    }, [user, pathname])

    // Don't show anything if not logged in
    if (!user) return null

    // Loading state
    if (loading) {
        return (
            <div className="flex items-center gap-2 px-3 py-1.5 bg-cloud/50 rounded-sm animate-pulse">
                <div className="w-4 h-4 bg-mist rounded-sm" />
                <div className="w-12 h-4 bg-mist rounded-sm" />
            </div>
        )
    }

    // Use defaults if credits is still null
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
            return 'bg-red-100 text-red-700 hover:bg-red-200'
        }
        if (isLow && displayCredits.tier === 'free') {
            return 'bg-amber-100 text-amber-700 hover:bg-amber-200'
        }
        return `${tierConfig.bgColor} ${tierConfig.textColor}`
    }

    return (
        <div className="flex items-center gap-2">
            {/* Credit Counter - Shows USED / TOTAL */}
            <Link
                href="/#pricing"
                className={`flex items-center gap-2 px-3 py-1.5 rounded-sm text-sm font-medium transition-all hover:scale-105 ${getDisplayStyle()}`}
                title={`${creditsUsed} of ${displayCredits.tier_limit} credits used this month (${displayCredits.credits_remaining} remaining)`}
            >
                {tierConfig.icon}
                <span className="font-semibold">{creditsUsed}</span>
                <span className="text-xs opacity-70">/ {displayCredits.tier_limit} used</span>
            </Link>

            {/* Upgrade prompt for users with low or no credits */}
            {(isLow || isExhausted) && (
                <Link
                    href="/#pricing"
                    className="hidden sm:flex items-center gap-1 px-2 py-1 text-xs text-gold-dark hover:text-gold font-medium transition-colors"
                >
                    {isExhausted ? 'Get More →' : 'Upgrade →'}
                </Link>
            )}
        </div>
    )
}
