'use client'

import { useEffect, useState } from 'react'
import { Zap, Sparkles, Users } from 'lucide-react'
import Link from 'next/link'
import { getCredits, type CreditsInfo } from '@/lib/api'
import { useAuth } from '@/context/AuthContext'

/**
 * Displays user's remaining credits in the header.
 * Shows tier badge and credit count with visual feedback.
 */
export default function CreditsDisplay() {
    const { user } = useAuth()
    const [credits, setCredits] = useState<CreditsInfo | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(false)

    useEffect(() => {
        if (!user) {
            setLoading(false)
            return
        }

        const fetchCredits = async () => {
            try {
                const data = await getCredits()
                setCredits(data)
                setError(false)
            } catch (err) {
                console.error('Failed to fetch credits:', err)
                setError(true)
            } finally {
                setLoading(false)
            }
        }

        fetchCredits()
    }, [user])

    // Don't show anything if not logged in
    if (!user) return null

    // Loading state
    if (loading) {
        return (
            <div className="flex items-center gap-2 px-3 py-1.5 bg-cloud/50 rounded-sm animate-pulse">
                <div className="w-4 h-4 bg-mist rounded-sm" />
                <div className="w-8 h-4 bg-mist rounded-sm" />
            </div>
        )
    }

    // Error state - show upgrade link
    if (error || !credits) {
        return (
            <Link
                href="/#pricing"
                className="flex items-center gap-2 px-3 py-1.5 bg-gold/10 text-gold-dark hover:bg-gold/20 transition-colors rounded-sm text-sm font-medium"
            >
                <Sparkles className="w-4 h-4" />
                Upgrade
            </Link>
        )
    }

    // Determine tier icon and styling
    const getTierConfig = () => {
        switch (credits.tier) {
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
    const isLow = credits.credits_remaining <= 1 && credits.tier === 'free'

    return (
        <div className="flex items-center gap-2">
            {/* Credit Counter */}
            <Link
                href="/#pricing"
                className={`flex items-center gap-2 px-3 py-1.5 rounded-sm text-sm font-medium transition-all hover:scale-105 ${isLow
                        ? 'bg-amber-100 text-amber-700 hover:bg-amber-200'
                        : `${tierConfig.bgColor} ${tierConfig.textColor}`
                    }`}
                title={`${credits.credits_remaining} / ${credits.tier_limit} credits remaining this month`}
            >
                {tierConfig.icon}
                <span className="font-semibold">{credits.credits_remaining}</span>
                <span className="text-xs opacity-70">/ {credits.tier_limit}</span>
            </Link>

            {/* Upgrade prompt for free users with low credits */}
            {isLow && (
                <Link
                    href="/#pricing"
                    className="hidden sm:flex items-center gap-1 px-2 py-1 text-xs text-gold-dark hover:text-gold font-medium transition-colors"
                >
                    Upgrade →
                </Link>
            )}
        </div>
    )
}
