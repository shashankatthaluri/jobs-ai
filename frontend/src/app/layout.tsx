import type { Metadata } from "next";
import { Playfair_Display, Source_Serif_4, DM_Sans } from "next/font/google";
import "./globals.css";
import { JobProvider } from "@/context/JobContext";
import { AuthProvider } from "@/context/AuthContext";
import Header from "@/components/Header";
import Link from 'next/link';
import { Suspense } from 'react';
import { PostHogProvider } from "@/lib/posthog";

/* ═══════════════════════════════════════════════════════════════════════════
   TYPOGRAPHY CONFIGURATION
   Editorial luxury font stack
   ═══════════════════════════════════════════════════════════════════════════ */

const playfair = Playfair_Display({
  variable: "--font-playfair",
  subsets: ["latin"],
  display: "swap",
});

const sourceSerif = Source_Serif_4({
  variable: "--font-source-serif",
  subsets: ["latin"],
  display: "swap",
});

const dmSans = DM_Sans({
  variable: "--font-dm-sans",
  subsets: ["latin"],
  display: "swap",
});

/* ═══════════════════════════════════════════════════════════════════════════
   METADATA
   ═══════════════════════════════════════════════════════════════════════════ */

export const metadata: Metadata = {
  title: "Jobs | The Art of Career Precision",
  description: "Transform your resume with surgical precision. AI-powered ATS optimization that respects your truth.",
};

/* ═══════════════════════════════════════════════════════════════════════════
   ROOT LAYOUT
   ═══════════════════════════════════════════════════════════════════════════ */

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        suppressHydrationWarning
        className={`${playfair.variable} ${sourceSerif.variable} ${dmSans.variable} font-sans antialiased`}
      >
        <Suspense fallback={null}>
          <PostHogProvider>
            <AuthProvider>
              <JobProvider>
                <div className="min-h-screen flex flex-col">

                  {/* ─── Navigation ─────────────────────────────────────────── */}
                  <Header />
                  {/* ─── Main Content ───────────────────────────────────────── */}
                  <main className="flex-1">
                    {children}
                  </main>

                  {/* ─── Footer ─────────────────────────────────────────────── */}
                  <footer className="bg-navy text-cream">
                    <div className="container-editorial py-16 md:py-20">

                      {/* Main Footer Content */}
                      <div className="grid grid-cols-1 md:grid-cols-12 gap-12 mb-16">

                        {/* Brand Column */}
                        <div className="md:col-span-5">
                          <div className="flex items-center gap-3 mb-6">
                            <div className="w-10 h-10 bg-cream flex items-center justify-center">
                              <span className="font-display font-bold text-navy text-lg">J</span>
                            </div>
                            <span className="font-display text-2xl font-semibold">Jobs</span>
                          </div>
                          <p className="text-mist leading-relaxed max-w-md mb-6">
                            Precision instruments for career advancement. We believe your resume
                            should be as exceptional as your experience.
                          </p>
                          <div className="w-16 h-0.5 bg-gold" />
                        </div>

                        {/* Quick Links */}
                        <div className="md:col-span-3">
                          <h4 className="text-sm font-medium tracking-wide uppercase mb-6 text-mist">
                            Navigation
                          </h4>
                          <ul className="space-y-3">
                            <li>
                              <Link href="#approach" className="text-cloud hover:text-gold transition-colors">
                                Our Approach
                              </Link>
                            </li>
                            <li>
                              <Link href="#process" className="text-cloud hover:text-gold transition-colors">
                                The Process
                              </Link>
                            </li>
                            <li>
                              <Link href="/upload" className="text-cloud hover:text-gold transition-colors">
                                Begin Session
                              </Link>
                            </li>
                          </ul>
                        </div>

                        {/* Contact / CTA */}
                        <div className="md:col-span-4">
                          <h4 className="text-sm font-medium tracking-wide uppercase mb-6 text-mist">
                            Ready to transform?
                          </h4>
                          <p className="text-cloud mb-6">
                            Your next career move deserves precision.
                          </p>
                          <Link
                            href="/upload"
                            className="inline-flex items-center gap-2 px-6 py-3 bg-gold text-navy font-semibold
                                 transition-all duration-300 hover:bg-gold-light"
                          >
                            Start Now
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                            </svg>
                          </Link>
                        </div>
                      </div>

                      {/* Bottom Bar */}
                      <div className="pt-8 border-t border-navy-light flex flex-col md:flex-row justify-between items-center gap-4">
                        <p className="text-sm text-mist">
                          © 2026 Jobs AI. Crafted with precision.
                        </p>
                        <div className="flex gap-6 text-sm text-mist">
                          <a href="#" className="hover:text-gold transition-colors">Privacy</a>
                          <a href="#" className="hover:text-gold transition-colors">Terms</a>
                        </div>
                      </div>
                    </div>
                  </footer>

                </div>
              </JobProvider>
            </AuthProvider>
          </PostHogProvider>
        </Suspense>
      </body>
    </html>
  );
}
