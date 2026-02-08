'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Check, Zap, Users, Sparkles } from 'lucide-react'
import Link from 'next/link'
import { useAuth } from '@/context/AuthContext'

interface PricingTier {
    name: string
    price: string
    period: string
    description: string
    features: string[]
    cta: string
    highlight?: boolean
    icon: React.ReactNode
    polarProductId?: string
}

const tiers: PricingTier[] = [
    {
        name: 'Free',
        price: '$0',
        period: 'forever',
        description: 'Perfect for trying out Jobs AI',
        icon: <Sparkles className="w-6 h-6" />,
        features: [
            '3 resume analyses per month',
            'Company voice mirroring',
            'ATS-optimized output',
            'Cover letter generation',
            'Cold email templates',
        ],
        cta: 'Get Started',
    },
    {
        name: 'Pro',
        price: '$9',
        period: '/month',
        description: 'For active job seekers',
        icon: <Zap className="w-6 h-6" />,
        highlight: true,
        features: [
            '30 resume analyses per month',
            'Everything in Free',
            'Priority processing',
            'PDF export',
            'Email support',
        ],
        cta: 'Upgrade to Pro',
        polarProductId: '72a37199-b2a2-490c-a26d-0b75604d13aa',
    },
    {
        name: 'Team',
        price: '$29',
        period: '/month',
        description: 'For career coaches & power users',
        icon: <Users className="w-6 h-6" />,
        features: [
            '100 resume analyses per month',
            'Everything in Pro',
            'Bulk processing',
            'Usage analytics',
            'Priority support',
        ],
        cta: 'Upgrade to Team',
        polarProductId: '6c45e5f4-15ca-4fbb-8ba7-91a4bbcccc6e',
    },
]

export default function PricingPage() {
    const { user } = useAuth()
    const [billingPeriod, setBillingPeriod] = useState<'monthly' | 'yearly'>('monthly')

    const handleCheckout = async (tier: PricingTier) => {
        if (!tier.polarProductId) {
            // Free tier - just go to signup
            if (user) {
                window.location.href = '/upload'
            } else {
                window.location.href = '/signup'
            }
            return
        }

        // For paid tiers, redirect to Polar checkout
        const polarUrl = `https://polar.sh/api/v1/checkouts/custom/?productId=${tier.polarProductId}`
        window.open(polarUrl, '_blank')
    }

    return (
        <div className="bg-cream min-h-screen">
            {/* Hero Section */}
            <section className="container-editorial py-16 md:py-24 text-center">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                >
                    <span className="inline-block px-4 py-1.5 bg-gold/10 text-gold-dark text-xs font-semibold uppercase tracking-widest mb-6">
                        Pricing
                    </span>
                    <h1 className="font-display text-4xl md:text-5xl font-bold text-navy mb-6">
                        Invest in Your Career
                    </h1>
                    <p className="text-lg text-stone max-w-2xl mx-auto mb-8">
                        Stop sending generic resumes. Start speaking their language.
                        Choose the plan that fits your job search intensity.
                    </p>

                    {/* Billing Toggle - Future enhancement */}
                    {/* <div className="flex items-center justify-center gap-4 mb-12">
            <span className={billingPeriod === 'monthly' ? 'text-navy font-medium' : 'text-stone'}>Monthly</span>
            <button 
              onClick={() => setBillingPeriod(billingPeriod === 'monthly' ? 'yearly' : 'monthly')}
              className="relative w-14 h-8 bg-cloud rounded-full transition-colors"
            >
              <div className={`absolute top-1 w-6 h-6 bg-navy rounded-full transition-transform ${billingPeriod === 'yearly' ? 'translate-x-7' : 'translate-x-1'}`} />
            </button>
            <span className={billingPeriod === 'yearly' ? 'text-navy font-medium' : 'text-stone'}>
              Yearly <span className="text-gold text-sm">(Save 20%)</span>
            </span>
          </div> */}
                </motion.div>
            </section>

            {/* Pricing Cards */}
            <section className="container-editorial pb-24">
                <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
                    {tiers.map((tier, index) => (
                        <motion.div
                            key={tier.name}
                            initial={{ opacity: 0, y: 30 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                            className={`relative rounded-sm overflow-hidden ${tier.highlight
                                ? 'bg-navy text-cream shadow-editorial'
                                : 'bg-white border border-cloud'
                                }`}
                        >
                            {/* Popular Badge */}
                            {tier.highlight && (
                                <div className="absolute top-0 right-0 bg-gold text-navy text-xs font-bold px-3 py-1">
                                    POPULAR
                                </div>
                            )}

                            <div className="p-8">
                                {/* Icon */}
                                <div className={`w-12 h-12 rounded-sm flex items-center justify-center mb-6 ${tier.highlight ? 'bg-cream/10 text-gold' : 'bg-cream text-navy'
                                    }`}>
                                    {tier.icon}
                                </div>

                                {/* Name & Description */}
                                <h3 className={`font-display text-2xl font-bold mb-2 ${tier.highlight ? 'text-cream' : 'text-navy'
                                    }`}>
                                    {tier.name}
                                </h3>
                                <p className={`text-sm mb-6 ${tier.highlight ? 'text-mist' : 'text-stone'}`}>
                                    {tier.description}
                                </p>

                                {/* Price */}
                                <div className="flex items-baseline gap-1 mb-8">
                                    <span className={`font-display text-4xl font-bold ${tier.highlight ? 'text-cream' : 'text-navy'
                                        }`}>
                                        {tier.price}
                                    </span>
                                    <span className={tier.highlight ? 'text-mist' : 'text-stone'}>
                                        {tier.period}
                                    </span>
                                </div>

                                {/* CTA Button */}
                                <button
                                    onClick={() => handleCheckout(tier)}
                                    className={`w-full py-3 font-medium rounded-sm transition-all duration-300 mb-8 ${tier.highlight
                                        ? 'bg-gold text-navy hover:bg-gold-light'
                                        : 'bg-navy text-cream hover:bg-navy-light'
                                        }`}
                                >
                                    {tier.cta}
                                </button>

                                {/* Features */}
                                <ul className="space-y-3">
                                    {tier.features.map((feature) => (
                                        <li key={feature} className="flex items-start gap-3">
                                            <Check className={`w-5 h-5 flex-shrink-0 mt-0.5 ${tier.highlight ? 'text-gold' : 'text-gold-dark'
                                                }`} />
                                            <span className={`text-sm ${tier.highlight ? 'text-mist' : 'text-charcoal'}`}>
                                                {feature}
                                            </span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </section>

            {/* Credit Pack Section */}
            <section className="bg-navy-light py-16">
                <div className="container-editorial text-center">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="max-w-2xl mx-auto"
                    >
                        <h2 className="font-display text-3xl font-bold text-cream mb-4">
                            Need More Credits?
                        </h2>
                        <p className="text-mist mb-8">
                            Purchase a one-time credit pack. Credits never expire.
                        </p>
                        <div className="inline-flex items-center gap-8 bg-navy rounded-sm p-6">
                            <div className="text-left">
                                <div className="text-cream font-display text-2xl font-bold">10 Credits</div>
                                <div className="text-mist text-sm">One-time purchase</div>
                            </div>
                            <div className="text-gold font-display text-3xl font-bold">$5</div>
                            <button
                                onClick={() => window.open('https://polar.sh/api/v1/checkouts/custom/?productId=e413d327-665b-4378-97df-1abe915b46bb', '_blank')}
                                className="px-6 py-3 bg-gold text-navy font-medium rounded-sm hover:bg-gold-light transition-colors"
                            >
                                Buy Credits
                            </button>
                        </div>
                    </motion.div>
                </div>
            </section>

            {/* FAQ Section */}
            <section className="container-editorial py-24">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    className="max-w-3xl mx-auto"
                >
                    <h2 className="font-display text-3xl font-bold text-navy text-center mb-12">
                        Frequently Asked Questions
                    </h2>

                    <div className="space-y-6">
                        <div className="card-editorial p-6">
                            <h3 className="font-display text-lg font-semibold text-navy mb-2">
                                What counts as one analysis?
                            </h3>
                            <p className="text-stone">
                                One analysis = one job description + your resume tailored for that specific role.
                                This includes company voice mirroring, ATS optimization, cover letter, and cold email.
                            </p>
                        </div>

                        <div className="card-editorial p-6">
                            <h3 className="font-display text-lg font-semibold text-navy mb-2">
                                Do unused credits roll over?
                            </h3>
                            <p className="text-stone">
                                For subscriptions (Pro, Team), credits reset monthly. For credit packs,
                                credits never expire — use them whenever you need.
                            </p>
                        </div>

                        <div className="card-editorial p-6">
                            <h3 className="font-display text-lg font-semibold text-navy mb-2">
                                Can I cancel anytime?
                            </h3>
                            <p className="text-stone">
                                Yes! Cancel your subscription anytime. You'll keep access until the end of
                                your billing period. No questions asked.
                            </p>
                        </div>

                        <div className="card-editorial p-6">
                            <h3 className="font-display text-lg font-semibold text-navy mb-2">
                                Is my data secure?
                            </h3>
                            <p className="text-stone">
                                Absolutely. We never store your resume permanently. Your data is processed
                                securely and deleted after generation. We never share or sell your information.
                            </p>
                        </div>
                    </div>
                </motion.div>
            </section>

            {/* Final CTA */}
            <section className="bg-cream-dark py-16">
                <div className="container-editorial text-center">
                    <h2 className="font-display text-2xl md:text-3xl font-bold text-navy mb-4">
                        Ready to Land Your Dream Job?
                    </h2>
                    <p className="text-stone mb-8">
                        Join thousands of job seekers who've improved their applications with Jobs AI.
                    </p>
                    <Link
                        href={user ? '/upload' : '/signup'}
                        className="inline-flex px-8 py-4 bg-navy text-cream font-medium rounded-sm hover:bg-navy-light transition-colors"
                    >
                        Start Free Trial
                    </Link>
                </div>
            </section>
        </div>
    )
}
