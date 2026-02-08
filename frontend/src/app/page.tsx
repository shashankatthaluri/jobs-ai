'use client';

import Link from 'next/link';
import { motion, type Variants } from 'framer-motion';

/* ═══════════════════════════════════════════════════════════════════════════
   JOBS AI — LANDING PAGE
   Editorial Luxury Aesthetic
   ═══════════════════════════════════════════════════════════════════════════ */

export default function LandingPage() {

  // Animation variants with proper typing
  const fadeUp: Variants = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.7 } }
  };

  const stagger: Variants = {
    visible: { transition: { staggerChildren: 0.15 } }
  };

  return (
    <div className="bg-cream">

      {/* ═══════════════════════════════════════════════════════════════════
          HERO SECTION
          Editorial asymmetric layout with bold typography
          ═══════════════════════════════════════════════════════════════════ */}
      <section className="relative overflow-hidden">

        {/* Decorative elements */}
        <div className="absolute top-20 right-[10%] w-64 h-64 border border-gold/20 rounded-full"></div>
        <div className="absolute top-40 right-[15%] w-32 h-32 border border-gold/10 rounded-full"></div>
        <div className="absolute bottom-20 left-[5%] w-px h-32 bg-gradient-to-b from-gold to-transparent"></div>

        <div className="container-editorial section-padding">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center min-h-[80vh]">

            {/* Left: Main Content */}
            <motion.div
              className="lg:col-span-7 relative z-10"
              initial="hidden"
              animate="visible"
              variants={stagger}
            >
              {/* Eyebrow */}
              <motion.div variants={fadeUp} className="mb-8">
                <span className="badge-gold">
                  <span className="w-2 h-2 rounded-full bg-gold"></span>
                  Precision Resume Engineering
                </span>
              </motion.div>

              {/* Headline */}
              <motion.h1 variants={fadeUp} className="headline-display mb-8">
                Your career.{' '}
                <span className="relative inline-block">
                  Perfected
                  <span className="absolute -bottom-2 left-0 w-full h-1 bg-gold"></span>
                </span>.
              </motion.h1>

              {/* Subheadline */}
              <motion.p variants={fadeUp} className="text-editorial max-w-xl mb-12">
                We don't generate resumes. We engineer them with surgical precision—
                amplifying your truth for systems that scan, and humans who decide.
              </motion.p>

              {/* CTAs */}
              <motion.div variants={fadeUp} className="flex flex-wrap gap-4">
                <Link href="/upload" className="btn-gold inline-flex items-center gap-3 group">
                  Begin Your Session
                  <svg
                    className="w-5 h-5 transition-transform group-hover:translate-x-1"
                    fill="none" stroke="currentColor" viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
                </Link>
                <Link href="#approach" className="btn-secondary">
                  Our Approach
                </Link>
              </motion.div>

              {/* Trust indicator */}
              <motion.div variants={fadeUp} className="mt-16 pt-8 border-t border-cloud">
                <div className="flex items-center gap-8">
                  <div>
                    <div className="font-display text-4xl font-semibold text-navy">0%</div>
                    <div className="text-sm text-stone mt-1">Hallucination rate</div>
                  </div>
                  <div className="w-px h-12 bg-cloud"></div>
                  <div>
                    <div className="font-display text-4xl font-semibold text-navy">100%</div>
                    <div className="text-sm text-stone mt-1">Factual integrity</div>
                  </div>
                  <div className="w-px h-12 bg-cloud"></div>
                  <div>
                    <div className="font-display text-4xl font-semibold text-navy">13</div>
                    <div className="text-sm text-stone mt-1">Specialized agents</div>
                  </div>
                </div>
              </motion.div>
            </motion.div>

            {/* Right: Visual Element */}
            <motion.div
              className="lg:col-span-5 relative"
              initial={{ opacity: 0, x: 40 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.3 }}
            >
              <div className="relative">
                {/* Abstract document visualization */}
                <div className="relative bg-white shadow-editorial p-8 border border-cloud">
                  {/* Header */}
                  <div className="flex items-start justify-between mb-8">
                    <div>
                      <div className="h-3 w-32 bg-navy rounded-sm mb-2"></div>
                      <div className="h-2 w-24 bg-mist rounded-sm"></div>
                    </div>
                    <div className="w-8 h-8 bg-gold/20 flex items-center justify-center">
                      <div className="w-4 h-4 bg-gold rounded-sm"></div>
                    </div>
                  </div>

                  {/* Content lines */}
                  <div className="space-y-4 mb-8">
                    <div className="flex items-center gap-3">
                      <div className="w-2 h-2 bg-gold rounded-full"></div>
                      <div className="h-2 flex-1 bg-cloud rounded-sm"></div>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="w-2 h-2 bg-gold rounded-full"></div>
                      <div className="h-2 w-4/5 bg-cloud rounded-sm"></div>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="w-2 h-2 bg-gold rounded-full"></div>
                      <div className="h-2 w-3/4 bg-cloud rounded-sm"></div>
                    </div>
                  </div>

                  {/* Section */}
                  <div className="pt-6 border-t border-cloud">
                    <div className="h-2 w-20 bg-navy-muted rounded-sm mb-4"></div>
                    <div className="space-y-2">
                      <div className="h-2 w-full bg-cream-dark rounded-sm"></div>
                      <div className="h-2 w-5/6 bg-cream-dark rounded-sm"></div>
                      <div className="h-2 w-4/5 bg-cream-dark rounded-sm"></div>
                    </div>
                  </div>

                  {/* Floating accent */}
                  <div className="absolute -bottom-4 -right-4 w-24 h-24 bg-gold/10 -z-10"></div>
                </div>

                {/* Floating badge */}
                <div className="absolute -left-6 top-1/2 -translate-y-1/2 bg-navy text-cream px-4 py-3 shadow-medium">
                  <div className="text-xs uppercase tracking-wider text-mist mb-1">Status</div>
                  <div className="text-sm font-semibold flex items-center gap-2">
                    <span className="w-2 h-2 bg-success rounded-full"></span>
                    ATS Optimized
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════════
          APPROACH SECTION
          Philosophy and methodology
          ═══════════════════════════════════════════════════════════════════ */}
      <section id="approach" className="bg-ivory border-y border-cloud">
        <div className="container-editorial section-padding">

          {/* Section Header */}
          <div className="max-w-3xl mb-20">
            <span className="text-caption text-gold mb-4 block">Our Approach</span>
            <h2 className="headline-section mb-6">
              Truth, amplified.<br />
              Never fabricated.
            </h2>
            <p className="text-editorial">
              Every AI tool promises optimization. We deliver something different:
              precision without invention. Your experience, presented in its most
              compelling form—but always, uncompromisingly, your truth.
            </p>
          </div>

          {/* Feature Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">

            {/* Feature 1 */}
            <motion.div
              className="card-editorial group cursor-pointer"
              whileHover={{ y: -4 }}
              transition={{ duration: 0.3 }}
            >
              <div className="w-12 h-12 bg-navy flex items-center justify-center mb-6">
                <svg className="w-6 h-6 text-cream" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                    d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="font-display text-xl font-semibold mb-3 text-navy">
                Factual Locking
              </h3>
              <p className="text-slate leading-relaxed">
                Every claim verified against your master CV. If you didn't do it,
                we don't write it. Zero hallucinations, absolute integrity.
              </p>
            </motion.div>

            {/* Feature 2 */}
            <motion.div
              className="card-editorial group cursor-pointer"
              whileHover={{ y: -4 }}
              transition={{ duration: 0.3 }}
            >
              <div className="w-12 h-12 bg-gold flex items-center justify-center mb-6">
                <svg className="w-6 h-6 text-navy" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <h3 className="font-display text-xl font-semibold mb-3 text-navy">
                Live Intelligence
              </h3>
              <p className="text-slate leading-relaxed">
                Real-time company research finds their current pain points,
                so your cover letter speaks their exact language.
              </p>
            </motion.div>

            {/* Feature 3 */}
            <motion.div
              className="card-editorial group cursor-pointer"
              whileHover={{ y: -4 }}
              transition={{ duration: 0.3 }}
            >
              <div className="w-12 h-12 bg-navy flex items-center justify-center mb-6">
                <svg className="w-6 h-6 text-cream" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="font-display text-xl font-semibold mb-3 text-navy">
                ATS Engineering
              </h3>
              <p className="text-slate leading-relaxed">
                Keyword injection that passes automated scans without
                compromising readability for the humans who follow.
              </p>
            </motion.div>

            {/* Feature 4 */}
            <motion.div
              className="card-editorial group cursor-pointer"
              whileHover={{ y: -4 }}
              transition={{ duration: 0.3 }}
            >
              <div className="w-12 h-12 border-2 border-navy flex items-center justify-center mb-6 group-hover:bg-navy transition-colors">
                <svg className="w-6 h-6 text-navy group-hover:text-cream transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                    d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="font-display text-xl font-semibold mb-3 text-navy">
                Cold Outreach
              </h3>
              <p className="text-slate leading-relaxed">
                High-conversion emails to hiring managers. Human tone,
                clear value proposition, compelling call-to-action.
              </p>
            </motion.div>

            {/* Feature 5 */}
            <motion.div
              className="card-editorial group cursor-pointer"
              whileHover={{ y: -4 }}
              transition={{ duration: 0.3 }}
            >
              <div className="w-12 h-12 border-2 border-navy flex items-center justify-center mb-6 group-hover:bg-navy transition-colors">
                <svg className="w-6 h-6 text-navy group-hover:text-cream transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </div>
              <h3 className="font-display text-xl font-semibold mb-3 text-navy">
                Cover Letters
              </h3>
              <p className="text-slate leading-relaxed">
                Personalized, concise, and impactful. Three paragraphs that
                connect your story to their needs.
              </p>
            </motion.div>

            {/* Feature 6 - Accent */}
            <motion.div
              className="card-accent group cursor-pointer"
              whileHover={{ y: -4 }}
              transition={{ duration: 0.3 }}
            >
              <div className="w-12 h-12 bg-gold flex items-center justify-center mb-6">
                <svg className="w-6 h-6 text-navy" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                    d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="font-display text-xl font-semibold mb-3">
                One Click. Everything.
              </h3>
              <p className="text-mist leading-relaxed">
                Resume, cover letter, cold email—crafted together,
                aligned perfectly, ready instantly.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════════
          PROCESS SECTION
          How it works
          ═══════════════════════════════════════════════════════════════════ */}
      <section id="process" className="bg-cream">
        <div className="container-editorial section-padding">

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">

            {/* Left: Content */}
            <div>
              <span className="text-caption text-gold mb-4 block">The Process</span>
              <h2 className="headline-section mb-8">
                Three minutes to<br />
                transformation.
              </h2>

              {/* Steps */}
              <div className="space-y-8">

                {/* Step 1 */}
                <div className="flex gap-6">
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 bg-navy text-cream font-display text-xl font-semibold 
                                    flex items-center justify-center">
                      1
                    </div>
                  </div>
                  <div>
                    <h3 className="font-display text-xl font-semibold mb-2 text-navy">
                      Upload Your Master CV
                    </h3>
                    <p className="text-slate">
                      Your complete career history in PDF. We extract every detail,
                      preserving exact dates, titles, and achievements.
                    </p>
                  </div>
                </div>

                {/* Connector */}
                <div className="ml-6 w-px h-8 bg-gradient-to-b from-gold to-cloud"></div>

                {/* Step 2 */}
                <div className="flex gap-6">
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 bg-gold text-navy font-display text-xl font-semibold 
                                    flex items-center justify-center">
                      2
                    </div>
                  </div>
                  <div>
                    <h3 className="font-display text-xl font-semibold mb-2 text-navy">
                      Provide the Opportunity
                    </h3>
                    <p className="text-slate">
                      Paste the job description or link. Our agents analyze requirements,
                      research the company, identify what matters.
                    </p>
                  </div>
                </div>

                {/* Connector */}
                <div className="ml-6 w-px h-8 bg-gradient-to-b from-gold to-cloud"></div>

                {/* Step 3 */}
                <div className="flex gap-6">
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 border-2 border-navy text-navy font-display text-xl font-semibold 
                                    flex items-center justify-center">
                      3
                    </div>
                  </div>
                  <div>
                    <h3 className="font-display text-xl font-semibold mb-2 text-navy">
                      Receive Your Arsenal
                    </h3>
                    <p className="text-slate">
                      ATS-optimized resume, personalized cover letter, compelling cold email.
                      Copy, download, apply with confidence.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Right: Pull Quote */}
            <div className="relative">
              <div className="absolute -top-8 -left-8 text-[200px] font-display text-gold/10 leading-none select-none">
                "
              </div>
              <blockquote className="pull-quote relative z-10">
                Every AI tool promises to write your resume. We promise something different:
                to reveal your career in its most compelling truth.
              </blockquote>
              <div className="mt-8 flex items-center gap-4">
                <div className="divider"></div>
                <span className="text-sm text-stone">The Jobs Philosophy</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════════
          CTA SECTION
          Final conversion
          ═══════════════════════════════════════════════════════════════════ */}
      <section className="bg-navy text-cream">
        <div className="container-editorial py-24 md:py-32 text-center">

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="font-display text-4xl md:text-5xl lg:text-6xl font-semibold mb-6 text-cream">
              Your next chapter begins here.
            </h2>
            <p className="text-mist text-lg md:text-xl max-w-2xl mx-auto mb-12">
              Stop compromising. Start with precision. Your career deserves
              nothing less than absolute authenticity, perfectly presented.
            </p>

            <Link
              href="/upload"
              className="btn-gold inline-flex items-center gap-3 text-lg group"
            >
              Begin Your Session
              <svg
                className="w-5 h-5 transition-transform group-hover:translate-x-1"
                fill="none" stroke="currentColor" viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </Link>

            {/* Trust badges */}
            <div className="mt-16 flex flex-wrap justify-center gap-8 text-sm text-mist">
              <div className="flex items-center gap-2">
                <svg className="w-5 h-5 text-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M5 13l4 4L19 7" />
                </svg>
                No account required
              </div>
              <div className="flex items-center gap-2">
                <svg className="w-5 h-5 text-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M5 13l4 4L19 7" />
                </svg>
                Instant results
              </div>
              <div className="flex items-center gap-2">
                <svg className="w-5 h-5 text-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M5 13l4 4L19 7" />
                </svg>
                Your data stays private
              </div>
            </div>
          </motion.div>
        </div>
      </section>

    </div>
  );
}
