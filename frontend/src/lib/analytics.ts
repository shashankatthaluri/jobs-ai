/**
 * Analytics utility for tracking user behavior in Jobs AI.
 * Uses PostHog for event tracking.
 */

import { posthog } from './posthog'

// User identification
export const analytics = {
    /**
     * Identify a user after login/signup
     */
    identify: (userId: string, traits?: Record<string, any>) => {
        posthog.identify(userId, traits)
    },

    /**
     * Reset user identity on logout
     */
    reset: () => {
        posthog.reset()
    },

    // ============================================
    // AUTH EVENTS
    // ============================================

    signupStarted: () => {
        posthog.capture('signup_started')
    },

    signupCompleted: (method: 'email' | 'google') => {
        posthog.capture('signup_completed', { method })
    },

    loginCompleted: (method: 'email' | 'google') => {
        posthog.capture('login_completed', { method })
    },

    logout: () => {
        posthog.capture('logout')
        posthog.reset()
    },

    // ============================================
    // CORE FEATURE EVENTS
    // ============================================

    resumeUploadStarted: () => {
        posthog.capture('resume_upload_started')
    },

    resumeUploaded: (fileType: string, fileSize: number) => {
        posthog.capture('resume_uploaded', {
            file_type: fileType,
            file_size_bytes: fileSize
        })
    },

    analysisStarted: (hasJobUrl: boolean, hasCompanyUrl: boolean) => {
        posthog.capture('analysis_started', {
            has_job_url: hasJobUrl,
            has_company_url: hasCompanyUrl
        })
    },

    analysisCompleted: (matchScore: number, durationMs: number) => {
        posthog.capture('analysis_completed', {
            match_score: matchScore,
            duration_ms: durationMs
        })
    },

    analysisError: (errorType: string) => {
        posthog.capture('analysis_error', { error_type: errorType })
    },

    tailoringStarted: () => {
        posthog.capture('tailoring_started')
    },

    tailoringCompleted: (durationMs: number) => {
        posthog.capture('tailoring_completed', { duration_ms: durationMs })
    },

    // ============================================
    // RESULTS & EXPORT EVENTS
    // ============================================

    resumeViewed: (section: string) => {
        posthog.capture('resume_section_viewed', { section })
    },

    resumeDownloaded: (format: 'pdf' | 'docx') => {
        posthog.capture('resume_downloaded', { format })
    },

    coverLetterViewed: () => {
        posthog.capture('cover_letter_viewed')
    },

    coldEmailViewed: () => {
        posthog.capture('cold_email_viewed')
    },

    contentCopied: (type: 'resume' | 'cover_letter' | 'cold_email') => {
        posthog.capture('content_copied', { content_type: type })
    },

    // ============================================
    // MONETIZATION EVENTS
    // ============================================

    pricingPageViewed: () => {
        posthog.capture('pricing_page_viewed')
    },

    planSelected: (planName: string, price: number) => {
        posthog.capture('plan_selected', {
            plan_name: planName,
            price
        })
    },

    checkoutStarted: (planName: string, productId: string) => {
        posthog.capture('checkout_started', {
            plan_name: planName,
            product_id: productId
        })
    },

    checkoutCompleted: (planName: string) => {
        posthog.capture('checkout_completed', { plan_name: planName })
    },

    // ============================================
    // ENGAGEMENT EVENTS
    // ============================================

    featureUsed: (featureName: string) => {
        posthog.capture('feature_used', { feature_name: featureName })
    },

    faqExpanded: (question: string) => {
        posthog.capture('faq_expanded', { question })
    },

    externalLinkClicked: (destination: string) => {
        posthog.capture('external_link_clicked', { destination })
    }
}
