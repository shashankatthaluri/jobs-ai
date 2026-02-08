'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Check, Zap, Users, Sparkles, ChevronDown, Quote } from 'lucide-react'
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

const testimonials = [
    {
        quote: "Finally, a tool that doesn't make up fake accomplishments. My resume is 100% me, just articulated better.",
        name: "Sarah Chen",
        role: "Software Engineer",
        company: "Landed at Google",
    },
    {
        quote: "The cold emails actually sound human. Got 3 responses in my first week—that never happened before.",
        name: "Marcus Johnson",
        role: "Product Manager",
        company: "Transitioning from Startup",
    },
    {
        quote: "As a career coach, I use this for every client. The company research alone saves me hours.",
        name: "Dr. Emily Rodriguez",
        role: "Career Coach",
        company: "Rodriguez Career Services",
    },
]

const faqs = [
    {
        question: 'What counts as an analysis?',
        answer: 'One analysis includes generating a tailored resume, cover letter, and cold email for a single job application. All three outputs are created together for optimal alignment.',
    },
    {
        question: 'Do unused credits roll over?',
        answer: 'Monthly subscription credits reset each billing cycle. However, purchased credit packs never expire—use them whenever you need them.',
    },
    {
        question: 'Can I upgrade or downgrade anytime?',
        answer: "Absolutely! You can change your plan at any time from your account settings. Upgrades take effect immediately, and downgrades apply at the end of your current billing cycle.",
    },
    {
        question: 'Is my data secure?',
        answer: 'Your privacy is paramount. We use industry-standard encryption (AES-256), never share your resume data, and never use it for AI training. You can delete your data anytime.',
    },
    {
        question: 'What makes this different from ChatGPT?',
        answer: "Unlike generic AI, we specialize in job applications. Our agents research companies in real-time, enforce factual accuracy (no hallucinations), and optimize for both ATS and human readers.",
    },
]

function FAQItem({ question, answer, isOpen, onClick }: { question: string; answer: string; isOpen: boolean; onClick: () => void }) {
    return (
        <div className="border-b border-cloud last:border-b-0">
            <button
                onClick={onClick}
                className="w-full py-5 flex items-center justify-between text-left group"
            >
                <span className="font-display text-lg font-semibold text-navy group-hover:text-gold-dark transition-colors">
                    {question}
                </span>
                <ChevronDown
                    className={`w-5 h-5 text-stone transition-transform duration-300 ${isOpen ? 'rotate-180 text-gold' : ''}`}
                />
            </button>
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.3 }}
                        className="overflow-hidden"
                    >
                        <p className="pb-5 text-stone leading-relaxed">
                            {answer}
                        </p>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    )
}

export default function PricingSection() {
    const { user } = useAuth()
    const [openFaq, setOpenFaq] = useState<number | null>(null)

    const handleCheckout = async (tier: PricingTier) => {
        if (!tier.polarProductId) {
            if (user) {
                window.location.href = '/upload'
            } else {
                window.location.href = '/signup'
            }
            return
        }
        const polarUrl = `https://polar.sh/api/v1/checkouts/custom/?productId=${tier.polarProductId}`
        window.open(polarUrl, '_blank')
    }

    return (
        <>
            {/* ═══════════════════════════════════════════════════════════════════
                TESTIMONIALS SECTION
                Social proof before the pricing ask
                ═══════════════════════════════════════════════════════════════════ */}
            <section className="bg-ivory border-y border-cloud py-20 md:py-24">
                <div className="container-editorial">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                        className="text-center mb-16"
                    >
                        <span className="text-caption text-gold mb-4 block">Testimonials</span>
                        <h2 className="headline-section">
                            Trusted by job seekers worldwide
                        </h2>
                    </motion.div>

                    <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
                        {testimonials.map((testimonial, index) => (
                            <motion.div
                                key={testimonial.name}
                                initial={{ opacity: 0, y: 30 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ duration: 0.5, delay: index * 0.1 }}
                                className="bg-white p-8 shadow-subtle relative"
                            >
                                <Quote className="absolute top-6 right-6 w-8 h-8 text-gold/20" />
                                <p className="text-charcoal mb-6 leading-relaxed italic">
                                    "{testimonial.quote}"
                                </p>
                                <div className="border-t border-cloud pt-4">
                                    <div className="font-semibold text-navy">{testimonial.name}</div>
                                    <div className="text-sm text-stone">{testimonial.role}</div>
                                    <div className="text-sm text-gold-dark font-medium mt-1">{testimonial.company}</div>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ═══════════════════════════════════════════════════════════════════
                PRICING SECTION
                Tier cards and credit packs
                ═══════════════════════════════════════════════════════════════════ */}
            <section id="pricing" className="bg-cream py-20 md:py-28">
                <div className="container-editorial">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                        className="text-center mb-16"
                    >
                        <span className="text-caption text-gold mb-4 block">Pricing</span>
                        <h2 className="headline-section mb-6">
                            Invest in Your Career
                        </h2>
                        <p className="text-lg text-stone max-w-2xl mx-auto">
                            Stop sending generic resumes. Start speaking their language.
                        </p>
                    </motion.div>

                    {/* Pricing Cards */}
                    <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto mb-16">
                        {tiers.map((tier, index) => (
                            <motion.div
                                key={tier.name}
                                initial={{ opacity: 0, y: 30 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ duration: 0.5, delay: index * 0.1 }}
                                className={`relative rounded-sm overflow-hidden ${tier.highlight
                                    ? 'bg-navy text-cream shadow-editorial'
                                    : 'bg-white border border-cloud'
                                    }`}
                            >
                                {tier.highlight && (
                                    <div className="absolute top-0 right-0 bg-gold text-navy text-xs font-bold px-3 py-1">
                                        POPULAR
                                    </div>
                                )}

                                <div className="p-8">
                                    <div className={`w-12 h-12 rounded-sm flex items-center justify-center mb-6 ${tier.highlight ? 'bg-cream/10 text-gold' : 'bg-cream text-navy'
                                        }`}>
                                        {tier.icon}
                                    </div>

                                    <h3 className={`font-display text-2xl font-bold mb-2 ${tier.highlight ? 'text-cream' : 'text-navy'
                                        }`}>
                                        {tier.name}
                                    </h3>
                                    <p className={`text-sm mb-6 ${tier.highlight ? 'text-mist' : 'text-stone'}`}>
                                        {tier.description}
                                    </p>

                                    <div className="flex items-baseline gap-1 mb-8">
                                        <span className={`font-display text-4xl font-bold ${tier.highlight ? 'text-cream' : 'text-navy'
                                            }`}>
                                            {tier.price}
                                        </span>
                                        <span className={tier.highlight ? 'text-mist' : 'text-stone'}>
                                            {tier.period}
                                        </span>
                                    </div>

                                    <button
                                        onClick={() => handleCheckout(tier)}
                                        className={`w-full py-3 font-medium rounded-sm transition-all duration-300 mb-8 ${tier.highlight
                                            ? 'bg-gold text-navy hover:bg-gold-light'
                                            : 'bg-navy text-cream hover:bg-navy-light'
                                            }`}
                                    >
                                        {tier.cta}
                                    </button>

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

                    {/* Credit Pack */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="max-w-2xl mx-auto text-center"
                    >
                        <div className="bg-navy-light rounded-sm p-8">
                            <h3 className="font-display text-2xl font-bold text-cream mb-2">
                                Need More Credits?
                            </h3>
                            <p className="text-mist mb-6">
                                One-time purchase. Credits never expire.
                            </p>
                            <div className="inline-flex items-center gap-6 bg-navy rounded-sm p-4">
                                <div className="text-left">
                                    <div className="text-cream font-display text-xl font-bold">10 Credits</div>
                                    <div className="text-mist text-sm">Pay once, use anytime</div>
                                </div>
                                <div className="text-gold font-display text-2xl font-bold">$5</div>
                                <button
                                    onClick={() => window.open('https://polar.sh/api/v1/checkouts/custom/?productId=e413d327-665b-4378-97df-1abe915b46bb', '_blank')}
                                    className="px-5 py-2.5 bg-gold text-navy font-medium rounded-sm hover:bg-gold-light transition-colors"
                                >
                                    Buy Credits
                                </button>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </section>

            {/* ═══════════════════════════════════════════════════════════════════
                FAQ SECTION
                Accordion style for better UX
                ═══════════════════════════════════════════════════════════════════ */}
            <section className="bg-ivory py-20 md:py-24">
                <div className="container-editorial">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                        className="max-w-3xl mx-auto"
                    >
                        <div className="text-center mb-12">
                            <span className="text-caption text-gold mb-4 block">FAQ</span>
                            <h2 className="font-display text-3xl font-bold text-navy">
                                Common Questions
                            </h2>
                        </div>

                        <div className="bg-white rounded-sm shadow-subtle p-8">
                            {faqs.map((faq, index) => (
                                <FAQItem
                                    key={faq.question}
                                    question={faq.question}
                                    answer={faq.answer}
                                    isOpen={openFaq === index}
                                    onClick={() => setOpenFaq(openFaq === index ? null : index)}
                                />
                            ))}
                        </div>
                    </motion.div>
                </div>
            </section>
        </>
    )
}
