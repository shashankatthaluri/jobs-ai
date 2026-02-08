'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function PricingPage() {
    const router = useRouter()

    useEffect(() => {
        // Redirect to landing page pricing section
        router.replace('/#pricing')
    }, [router])

    return (
        <div className="min-h-screen bg-cream flex items-center justify-center">
            <div className="text-center">
                <div className="w-8 h-8 border-2 border-navy border-t-transparent rounded-full animate-spin mx-auto mb-4" />
                <p className="text-stone">Redirecting to pricing...</p>
            </div>
        </div>
    )
}
