'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import {
    Upload,
    Link as LinkIcon,
    FileText,
    Globe,
    Zap,
    Loader2,
    ArrowLeft,
    Terminal,
    Cpu,
    PenTool,
    CheckCircle2
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useJob } from '@/context/JobContext';
import { analyzeApplication, tailorApplication, AnalysisResponse } from '@/lib/api';
import SkillGapConfirmation from '@/components/SkillGapConfirmation';

// Processing steps for step 1 (analysis)
const ANALYSIS_STEPS = [
    { id: 'extract', label: 'CV Extraction', icon: FileText },
    { id: 'analyze', label: 'JD Intelligence', icon: Terminal },
    { id: 'research', label: 'Deep Company Research', icon: Globe },
];

// Processing steps for step 2 (tailoring)
const TAILORING_STEPS = [
    { id: 'tailor', label: 'Resume Optimization', icon: Cpu },
    { id: 'write', label: 'Asset Generation', icon: PenTool },
];

type FlowStep = 'input' | 'analyzing' | 'skill-gap' | 'tailoring';

export default function UploadPage() {
    const router = useRouter();
    const { setResults, setError } = useJob();

    // Form state
    const [file, setFile] = useState<File | null>(null);
    const [jobDescription, setJobDescription] = useState('');
    const [jobUrl, setJobUrl] = useState('');
    const [companyUrl, setCompanyUrl] = useState(''); // Changed from companyName

    // Flow state
    const [flowStep, setFlowStep] = useState<FlowStep>('input');
    const [currentStepIdx, setCurrentStepIdx] = useState(0);
    const [error, setLocalError] = useState<string | null>(null);

    // Analysis results (stored between steps)
    const [analysisResult, setAnalysisResult] = useState<AnalysisResponse | null>(null);
    const [confirmedSkills, setConfirmedSkills] = useState<string[]>([]);

    // Animate through steps during processing
    useEffect(() => {
        if (flowStep === 'analyzing') {
            const interval = setInterval(() => {
                setCurrentStepIdx(prev => (prev < ANALYSIS_STEPS.length - 1 ? prev + 1 : prev));
            }, 4000);
            return () => clearInterval(interval);
        } else if (flowStep === 'tailoring') {
            setCurrentStepIdx(0);
            const interval = setInterval(() => {
                setCurrentStepIdx(prev => (prev < TAILORING_STEPS.length - 1 ? prev + 1 : prev));
            }, 3000);
            return () => clearInterval(interval);
        } else {
            setCurrentStepIdx(0);
        }
    }, [flowStep]);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const selectedFile = e.target.files[0];
            if (selectedFile.type !== 'application/pdf') {
                setLocalError('Please upload a PDF file.');
                return;
            }
            setFile(selectedFile);
            setLocalError(null);
        }
    };

    // Step 1: Analyze
    const handleAnalyze = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!file || (!jobDescription && !jobUrl) || !companyUrl) return;

        setFlowStep('analyzing');
        setLocalError(null);
        // Scroll to top to show loading state
        window.scrollTo({ top: 0, behavior: 'smooth' });

        try {
            const result = await analyzeApplication(file, jobDescription, jobUrl, companyUrl);
            setAnalysisResult(result);
            setFlowStep('skill-gap');
        } catch (err: any) {
            setLocalError(err.message || 'Analysis failed.');
            setFlowStep('input');
        }
    };

    // Toggle skill confirmation
    const handleToggleSkill = (skill: string) => {
        setConfirmedSkills(prev =>
            prev.includes(skill)
                ? prev.filter(s => s !== skill)
                : [...prev, skill]
        );
    };

    // Step 2: Tailor with confirmed skills
    const handleTailor = async () => {
        if (!analysisResult) return;

        setFlowStep('tailoring');
        setLocalError(null);

        try {
            const result = await tailorApplication({
                master_cv: analysisResult.master_cv,
                job_analysis: analysisResult.job_analysis,
                company_intel: analysisResult.company_intel,
                confirmed_skills: {
                    confirmed_missing_skills: confirmedSkills
                }
            });

            // Convert to the format expected by results page
            setResults({
                master_cv: analysisResult.master_cv,
                job_analysis: analysisResult.job_analysis,
                company_intel: analysisResult.company_intel,
                tailored_resume: {
                    resume_markdown: result.resume_markdown,
                    matched_skills: result.matched_skills,
                    keywords_used: result.keywords_used,
                    relevance_summary: ''
                },
                writing: {
                    cover_letter: { content: result.cover_letter, word_count: result.cover_letter.split(' ').length },
                    cold_email: { content: result.cold_email, word_count: result.cold_email.split(' ').length },
                    company_summary: { content: result.company_summary, word_count: result.company_summary.split(' ').length }
                },
                warnings: analysisResult.cv_warnings
            });

            // Scroll to top before navigation
            window.scrollTo(0, 0);
            router.push('/results');
        } catch (err: any) {
            setLocalError(err.message || 'Tailoring failed.');
            setFlowStep('skill-gap');
        }
    };

    const isFormValid = file && (jobDescription || jobUrl) && companyUrl;

    // ============================================================
    // RENDER: Processing States
    // ============================================================

    if (flowStep === 'analyzing' || flowStep === 'tailoring') {
        const steps = flowStep === 'analyzing' ? ANALYSIS_STEPS : TAILORING_STEPS;
        const title = flowStep === 'analyzing' ? 'Analyzing Your Application...' : 'Tailoring Your Documents...';
        const subtitle = flowStep === 'analyzing'
            ? 'Our agents are parsing your CV and researching the company.'
            : 'Generating your personalized resume, cover letter, and email.';

        return (
            <div className="max-w-4xl mx-auto px-6 py-20 flex flex-col items-center justify-center min-h-[70vh]">
                <div className="absolute inset-0 bg-gold/5 -z-10 animate-pulse"></div>

                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="w-24 h-24 rounded-3xl bg-gold/20 flex items-center justify-center mb-12 border border-gold/30 relative"
                >
                    <Loader2 className="w-12 h-12 text-gold animate-spin" />
                    <div className="absolute inset-0 rounded-3xl border-2 border-gold border-t-transparent animate-[spin_3s_linear_infinite]"></div>
                </motion.div>

                <h1 className="font-display text-4xl font-bold mb-4 text-navy text-center">{title}</h1>
                <p className="text-slate text-lg mb-16 text-center max-w-md">{subtitle}</p>

                <div className="w-full max-w-2xl space-y-4">
                    {steps.map((step, idx) => {
                        const isActive = idx === currentStepIdx;
                        const isCompleted = idx < currentStepIdx;
                        const Icon = step.icon;

                        return (
                            <div
                                key={step.id}
                                className={`flex items-center gap-4 p-4 rounded-2xl transition-all duration-500 border
                                    ${isActive ? 'bg-gold/10 border-gold/30 scale-105 shadow-lg' :
                                        isCompleted ? 'bg-cream-dark border-cloud opacity-60' :
                                            'bg-transparent border-transparent opacity-30'}`}
                            >
                                <div className={`w-10 h-10 rounded-xl flex items-center justify-center
                                    ${isCompleted ? 'bg-green-100 text-green-600' : 'bg-cream-dark text-navy'}`}>
                                    {isCompleted ? <CheckCircle2 className="w-6 h-6" /> : <Icon className="w-6 h-6" />}
                                </div>
                                <div className="flex-1">
                                    <p className={`font-semibold ${isActive ? 'text-navy' : 'text-stone'}`}>
                                        {step.label}
                                    </p>
                                    {isActive && (
                                        <p className="text-xs text-gold animate-pulse mt-1 uppercase tracking-widest font-bold">
                                            Processing...
                                        </p>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        );
    }

    // ============================================================
    // RENDER: Skill Gap Confirmation
    // ============================================================

    if (flowStep === 'skill-gap' && analysisResult) {
        return (
            <div className="max-w-3xl mx-auto px-6 py-12">
                <Link href="/upload" onClick={() => setFlowStep('input')} className="inline-flex items-center gap-2 text-stone hover:text-navy transition-colors mb-8 group">
                    <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
                    Back to Form
                </Link>

                <div className="bg-white rounded-2xl shadow-editorial p-8 border border-cloud">
                    <SkillGapConfirmation
                        skillGap={analysisResult.skill_gap}
                        confirmedSkills={confirmedSkills}
                        onToggleSkill={handleToggleSkill}
                        onConfirm={handleTailor}
                        isProcessing={false}
                    />
                </div>

                {error && (
                    <motion.p
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="mt-6 p-6 rounded-2xl bg-red-50 border border-red-200 text-red-700 text-center font-medium"
                    >
                        {error}
                    </motion.p>
                )}
            </div>
        );
    }

    // ============================================================
    // RENDER: Input Form
    // ============================================================

    return (
        <div className="max-w-6xl mx-auto px-6 py-12">
            <Link href="/" className="inline-flex items-center gap-2 text-stone hover:text-navy transition-colors mb-12 group">
                <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
                Back to Home
            </Link>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
                {/* Left Column: Context */}
                <div className="lg:col-span-5 space-y-8">
                    <div>
                        <h1 className="font-display text-5xl font-bold text-navy mb-4 tracking-tight leading-none">
                            Career<br />Studio
                        </h1>
                        <p className="text-slate text-lg leading-relaxed">
                            Upload your master CV and provide the opportunity details.
                            We'll analyze the match and let you confirm your skills before tailoring.
                        </p>
                    </div>

                    <div className="space-y-4">
                        <div className="card-editorial p-6 border-gold/20 bg-gold/5">
                            <h4 className="font-semibold text-navy mb-1 flex items-center gap-2">
                                <ShieldCheck className="w-4 h-4 text-green-600" /> Factual Integrity
                            </h4>
                            <p className="text-sm text-stone">Original dates and metrics preserved. No hallucinations.</p>
                        </div>
                        <div className="card-editorial p-6">
                            <h4 className="font-semibold text-navy mb-1 flex items-center gap-2">
                                <Sparkles className="w-4 h-4 text-gold" /> Skill Confirmation
                            </h4>
                            <p className="text-sm text-stone">You'll see what skills are needed and confirm what you have.</p>
                        </div>
                    </div>
                </div>

                {/* Right Column: Form */}
                <div className="lg:col-span-7">
                    <form onSubmit={handleAnalyze} className="space-y-8">
                        {/* CV Upload */}
                        <div className="card-editorial relative overflow-hidden">
                            <div className="absolute top-0 left-0 w-1 h-full bg-gold"></div>
                            <label className="block text-sm font-bold text-navy uppercase tracking-widest mb-4">
                                1. Master Resume (PDF)
                            </label>
                            <div className={`group relative border-2 border-dashed rounded-2xl p-10 transition-all flex flex-col items-center justify-center text-center
                                ${file ? 'border-gold/50 bg-gold/5' : 'border-cloud hover:border-gold/40 bg-cream'}`}>
                                <input type="file" accept=".pdf" onChange={handleFileChange} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" />
                                <div className={`w-16 h-16 rounded-2xl flex items-center justify-center mb-6 transition-all
                                    ${file ? 'bg-gold text-white scale-110' : 'bg-cream-dark text-stone group-hover:bg-cloud'}`}>
                                    <Upload className="w-8 h-8" />
                                </div>
                                {file ? (
                                    <div>
                                        <p className="font-bold text-navy text-lg">{file.name}</p>
                                        <p className="text-sm text-stone mt-1">Ready for extraction</p>
                                    </div>
                                ) : (
                                    <>
                                        <p className="font-bold text-navy text-lg">Drop your Master CV here</p>
                                        <p className="text-sm text-stone mt-2">Maximum file size 10MB • PDF only</p>
                                    </>
                                )}
                            </div>
                        </div>

                        {/* Company URL */}
                        <div className="card-editorial">
                            <label className="block text-sm font-bold text-navy uppercase tracking-widest mb-4 flex items-center gap-2">
                                <Globe className="w-4 h-4 text-gold" /> 2. Company Website
                            </label>
                            <input
                                type="url"
                                placeholder="e.g., stripe.com, openai.com, spacex.com"
                                value={companyUrl}
                                onChange={(e) => setCompanyUrl(e.target.value)}
                                className="w-full px-4 py-3 rounded-xl border border-cloud bg-cream focus:border-gold focus:outline-none text-navy placeholder:text-stone"
                                required
                            />
                            <p className="text-xs text-stone mt-2">We'll research the company deeply from their website</p>
                        </div>

                        {/* Job Description */}
                        <div className="card-editorial">
                            <label className="block text-sm font-bold text-navy uppercase tracking-widest mb-4 flex items-center gap-2">
                                <Zap className="w-4 h-4 text-gold" /> 3. Job Description
                            </label>
                            <textarea
                                placeholder="Paste the job requirements here..."
                                value={jobDescription}
                                onChange={(e) => setJobDescription(e.target.value)}
                                className="w-full px-4 py-3 rounded-xl border border-cloud bg-cream focus:border-gold focus:outline-none text-navy placeholder:text-stone min-h-[180px] text-sm resize-none"
                            />

                            <div className="flex items-center gap-4 my-6">
                                <div className="flex-grow h-px bg-cloud"></div>
                                <span className="text-xs font-bold text-stone uppercase tracking-widest shrink-0">OR PROVIDE URL</span>
                                <div className="flex-grow h-px bg-cloud"></div>
                            </div>

                            <div className="relative">
                                <LinkIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-stone" />
                                <input
                                    type="url"
                                    placeholder="https://linkedin.com/jobs/view/..."
                                    value={jobUrl}
                                    onChange={(e) => setJobUrl(e.target.value)}
                                    className="w-full pl-12 pr-4 py-3 rounded-xl border border-cloud bg-cream focus:border-gold focus:outline-none text-navy placeholder:text-stone"
                                />
                            </div>
                        </div>

                        {/* Submit */}
                        <button
                            type="submit"
                            disabled={!isFormValid}
                            className="btn-gold w-full h-16 text-lg font-semibold flex items-center justify-center gap-4 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            Analyze & Match Skills <Cpu className="w-6 h-6" />
                        </button>

                        {error && (
                            <motion.p
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="p-6 rounded-2xl bg-red-50 border border-red-200 text-red-700 text-center font-medium"
                            >
                                {error}
                            </motion.p>
                        )}
                    </form>
                </div>
            </div>
        </div>
    );
}

function ShieldCheck({ className }: { className?: string }) {
    return (
        <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            <path d="m9 12 2 2 4-4" />
        </svg>
    );
}

function Sparkles({ className }: { className?: string }) {
    return (
        <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z" />
            <path d="M5 3v4" />
            <path d="M19 17v4" />
            <path d="M3 5h4" />
            <path d="M17 19h4" />
        </svg>
    );
}
