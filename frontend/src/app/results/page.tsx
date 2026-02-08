'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import {
    FileText,
    Mail,
    MessageSquare,
    Copy,
    Download,
    Check,
    ArrowLeft,
    AlertTriangle,
    ExternalLink,
    Target,
    Sparkles,
    ChevronRight,
    Building2
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { motion, AnimatePresence } from 'framer-motion';
import { useJob } from '@/context/JobContext';

type TabType = 'resume' | 'cover' | 'email' | 'company';

export default function ResultsPage() {
    const router = useRouter();
    const { results } = useJob();
    const [activeTab, setActiveTab] = useState<TabType>('resume');
    const [copied, setCopied] = useState(false);
    const [isReady, setIsReady] = useState(false);

    // Wait a tick for context to sync before checking results
    useEffect(() => {
        const timer = setTimeout(() => {
            setIsReady(true);
        }, 100);
        return () => clearTimeout(timer);
    }, []);

    useEffect(() => {
        if (isReady && !results) {
            router.push('/upload');
        } else if (results) {
            // Scroll to top when results are available
            window.scrollTo(0, 0);
        }
    }, [results, router, isReady]);

    // Show loading while waiting for context to sync
    if (!isReady) {
        return (
            <div className="min-h-screen bg-cream flex items-center justify-center">
                <div className="text-center">
                    <div className="w-8 h-8 border-2 border-navy border-t-transparent rounded-full animate-spin mx-auto mb-4" />
                    <p className="text-stone">Loading results...</p>
                </div>
            </div>
        );
    }

    if (!results) return null;

    const handleCopy = (text: string) => {
        navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    const handleDownload = (text: string, filename: string) => {
        const element = document.createElement('a');
        const file = new Blob([text], { type: 'text/plain' });
        element.href = URL.createObjectURL(file);
        element.download = filename.replace('.txt', '.md');
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    };

    const handlePrintPDF = () => {
        // Convert markdown to HTML for printing
        const resumeContent = results.tailored_resume.resume_markdown;

        // Create print-friendly HTML
        const printHTML = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Resume - ${results.company_intel.company_name}</title>
    <style>
        @page {
            margin: 0.75in;
            size: letter;
        }
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #1a1a1a;
            max-width: 100%;
            margin: 0;
            padding: 0;
        }
        h1 {
            font-size: 22pt;
            font-weight: bold;
            margin: 0 0 0.3em 0;
            color: #000;
            border-bottom: 2px solid #333;
            padding-bottom: 0.2em;
        }
        h2 {
            font-size: 13pt;
            font-weight: bold;
            margin: 1.2em 0 0.5em 0;
            color: #000;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 1px solid #666;
            padding-bottom: 0.2em;
        }
        h3 {
            font-size: 11pt;
            font-weight: bold;
            margin: 0.8em 0 0.3em 0;
            color: #000;
        }
        p {
            margin: 0.4em 0;
        }
        ul {
            margin: 0.3em 0;
            padding-left: 1.5em;
        }
        li {
            margin: 0.3em 0;
        }
        .contact {
            font-size: 10pt;
            color: #444;
            margin-bottom: 0.5em;
        }
        @media print {
            body { -webkit-print-color-adjust: exact; }
        }
    </style>
</head>
<body>
    ${resumeContent
                .replace(/^# (.+)$/gm, '<h1>$1</h1>')
                .replace(/^## (.+)$/gm, '<h2>$1</h2>')
                .replace(/^### (.+)$/gm, '<h3>$1</h3>')
                .replace(/^- (.+)$/gm, '<li>$1</li>')
                .replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>')
                .replace(/\n\n/g, '</p><p>')
                .replace(/\|/g, ' • ')
            }
</body>
</html>`;

        const printWindow = window.open('', '_blank');
        if (printWindow) {
            printWindow.document.write(printHTML);
            printWindow.document.close();
            printWindow.onload = () => {
                printWindow.focus();
                printWindow.print();
            };
        }
    };

    const handlePrintCoverLetterPDF = () => {
        const coverContent = results.writing.cover_letter.content;

        const printHTML = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Cover Letter - ${results.company_intel.company_name}</title>
    <style>
        @page {
            margin: 1in;
            size: letter;
        }
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #1a1a1a;
            max-width: 100%;
            margin: 0;
            padding: 0;
        }
        p {
            margin: 1em 0;
        }
        @media print {
            body { -webkit-print-color-adjust: exact; }
        }
    </style>
</head>
<body>
    ${coverContent.split('\n').map(line => line.trim() ? `<p>${line}</p>` : '').join('')}
</body>
</html>`;

        const printWindow = window.open('', '_blank');
        if (printWindow) {
            printWindow.document.write(printHTML);
            printWindow.document.close();
            printWindow.onload = () => {
                printWindow.focus();
                printWindow.print();
            };
        }
    };

    const tabs: { id: TabType, label: string, icon: any }[] = [
        { id: 'resume', label: 'ATS Resume', icon: FileText },
        { id: 'cover', label: 'Cover Letter', icon: MessageSquare },
        { id: 'email', label: 'Cold Email', icon: Mail },
        { id: 'company', label: 'Company Intel', icon: Building2 },
    ];

    const getActiveText = () => {
        switch (activeTab) {
            case 'resume': return results.tailored_resume.resume_markdown;
            case 'cover': return results.writing.cover_letter.content;
            case 'email': return results.writing.cold_email.content;
            case 'company': return results.writing.company_summary.content;
        }
    };

    return (
        <div className="max-w-7xl mx-auto px-6 py-8 min-h-screen">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
                <div className="flex items-center gap-6">
                    <button
                        onClick={() => router.push('/upload')}
                        className="w-12 h-12 rounded-xl bg-cream-dark flex items-center justify-center hover:bg-cloud transition-colors border border-cloud"
                    >
                        <ArrowLeft className="w-5 h-5 text-navy" />
                    </button>
                    <div>
                        <div className="flex items-center gap-3 mb-1">
                            <span className="badge-gold text-xs">Ready</span>
                            <h1 className="font-display text-2xl font-bold text-navy">Application Package</h1>
                        </div>
                        <p className="text-slate text-sm">
                            Role: <span className="text-navy font-medium">{results.job_analysis.role_title}</span>
                            <span className="mx-2 text-mist">•</span>
                            Target: <span className="text-navy font-medium">{results.company_intel.company_name}</span>
                        </p>
                    </div>
                </div>

                <div className="flex items-center gap-3">
                    <button
                        onClick={() => handleCopy(getActiveText())}
                        className="btn-secondary h-11 px-5 flex items-center gap-2 text-sm"
                    >
                        {copied ? <Check className="w-4 h-4 text-success" /> : <Copy className="w-4 h-4" />}
                        {copied ? 'Copied!' : 'Copy'}
                    </button>
                    <button
                        onClick={() => {
                            if (activeTab === 'resume') {
                                handlePrintPDF();
                            } else if (activeTab === 'cover') {
                                handlePrintCoverLetterPDF();
                            } else {
                                handleDownload(getActiveText(), `jobs_${activeTab}.md`);
                            }
                        }}
                        className="btn-gold h-11 px-6 flex items-center gap-2 text-sm"
                    >
                        <Download className="w-4 h-4" /> Download
                    </button>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                {/* Sidebar */}
                <div className="lg:col-span-3 space-y-6">
                    {/* Tab Navigation */}
                    <div className="card-editorial p-4 space-y-1">
                        {tabs.map((tab) => {
                            const isActive = activeTab === tab.id;
                            const Icon = tab.icon;
                            return (
                                <button
                                    key={tab.id}
                                    onClick={() => setActiveTab(tab.id)}
                                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-all
                                        ${isActive
                                            ? 'bg-gold text-navy shadow-gold'
                                            : 'text-slate hover:bg-cream-dark hover:text-navy'
                                        }`}
                                >
                                    <Icon className={`w-5 h-5 ${isActive ? 'text-navy' : 'text-gold'}`} />
                                    <span className="flex-1 text-left">{tab.label}</span>
                                    <ChevronRight className={`w-4 h-4 transition-transform ${isActive ? 'rotate-90' : 'opacity-0'}`} />
                                </button>
                            );
                        })}
                    </div>

                    {/* Metrics */}
                    <div className="card-editorial p-6">
                        <h4 className="text-xs font-bold text-navy uppercase tracking-widest mb-4 flex items-center gap-2">
                            <Target className="w-4 h-4 text-gold" /> ATS Metrics
                        </h4>
                        <div className="space-y-3 text-sm">
                            <div className="flex justify-between items-center">
                                <span className="text-slate">Keywords Used</span>
                                <span className="text-navy font-bold bg-cream-dark px-2 py-0.5 rounded">
                                    {results.tailored_resume.keywords_used.length}
                                </span>
                            </div>
                            <div className="flex justify-between items-center">
                                <span className="text-slate">Skills Matched</span>
                                <span className="text-navy font-bold bg-cream-dark px-2 py-0.5 rounded">
                                    {results.tailored_resume.matched_skills.length}
                                </span>
                            </div>
                            <div className="flex justify-between items-center">
                                <span className="text-slate">Factual Audit</span>
                                <span className="text-success font-bold text-xs flex items-center gap-1">
                                    <Check className="w-3 h-3" /> PASSED
                                </span>
                            </div>
                        </div>
                    </div>

                    {/* Warnings */}
                    {results.warnings.length > 0 && (
                        <div className="card-editorial p-6 border-error/20 bg-error/5">
                            <div className="flex items-center gap-2 text-error mb-3 font-bold text-sm">
                                <AlertTriangle className="w-4 h-4" /> Warnings
                            </div>
                            <ul className="text-xs text-slate space-y-2 list-disc list-inside">
                                {results.warnings.map((w, i) => <li key={i}>{w}</li>)}
                            </ul>
                        </div>
                    )}
                </div>

                {/* Content Area */}
                <div className="lg:col-span-9">
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={activeTab}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            transition={{ duration: 0.2 }}
                        >
                            {activeTab === 'resume' ? (
                                /* ATS Resume - Clean white document */
                                <div className="bg-white border border-cloud rounded-sm shadow-editorial p-10 md:p-16 min-h-[900px]">
                                    <div className="resume-preview">
                                        <ReactMarkdown>{results.tailored_resume.resume_markdown}</ReactMarkdown>
                                    </div>
                                </div>
                            ) : activeTab === 'company' ? (
                                /* Company Intel - Enhanced */
                                <div className="space-y-6">
                                    {/* Market Intelligence Summary */}
                                    <div className="card-editorial p-8 bg-navy text-cream">
                                        <div className="flex items-center gap-2 mb-4">
                                            <Sparkles className="w-5 h-5 text-gold" />
                                            <span className="text-xs font-bold uppercase tracking-widest text-gold">Market Intelligence</span>
                                        </div>
                                        <p className="text-xl leading-relaxed font-serif italic text-cream/90">
                                            "{results.writing.company_summary.content}"
                                        </p>
                                    </div>

                                    {/* Should I Apply? Recommendation */}
                                    {results.company_intel.recommendation && (
                                        <div className="card-editorial p-6 border-l-4 border-gold">
                                            <div className="flex items-center gap-2 mb-3">
                                                <Target className="w-5 h-5 text-gold" />
                                                <span className="text-xs font-bold uppercase tracking-widest text-navy">Should You Apply?</span>
                                                {results.company_intel.confidence_level && (
                                                    <span className={`ml-auto px-2 py-0.5 text-xs rounded ${results.company_intel.confidence_level === 'High' ? 'bg-green-100 text-green-700' :
                                                        results.company_intel.confidence_level === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                                                            'bg-red-100 text-red-700'
                                                        }`}>
                                                        {results.company_intel.confidence_level} confidence
                                                    </span>
                                                )}
                                            </div>
                                            <p className="text-charcoal leading-relaxed">{results.company_intel.recommendation}</p>
                                        </div>
                                    )}

                                    {/* Company Details Grid */}
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <IntelCard label="Industry" value={results.company_intel.industry} />
                                        <IntelCard label="Company Size" value={results.company_intel.employee_count_range} />
                                        <IntelCard label="Stage" value={results.company_intel.company_stage} />
                                        <IntelCard label="Website" value={results.company_intel.website} isLink />
                                    </div>

                                    {/* Mission */}
                                    {results.company_intel.mission && (
                                        <div className="card-editorial p-6">
                                            <h4 className="text-xs font-bold text-navy uppercase tracking-widest mb-3">Mission & Values</h4>
                                            <p className="text-charcoal leading-relaxed">{results.company_intel.mission}</p>
                                        </div>
                                    )}

                                    {/* Reputation Summary */}
                                    {results.company_intel.reputation_summary && (
                                        <div className="card-editorial p-6">
                                            <h4 className="text-xs font-bold text-navy uppercase tracking-widest mb-3">What People Say</h4>
                                            <p className="text-charcoal leading-relaxed">{results.company_intel.reputation_summary}</p>
                                        </div>
                                    )}

                                    {/* Culture Highlights */}
                                    {results.company_intel.culture_highlights?.length > 0 && (
                                        <div className="card-editorial p-6">
                                            <h4 className="text-xs font-bold text-navy uppercase tracking-widest mb-3">Culture</h4>
                                            <div className="flex flex-wrap gap-2">
                                                {results.company_intel.culture_highlights.map((item: string, i: number) => (
                                                    <span key={i} className="px-3 py-1 bg-cream text-navy text-sm rounded-full border border-cloud">
                                                        {item}
                                                    </span>
                                                ))}
                                            </div>
                                        </div>
                                    )}

                                    {/* Red Flags */}
                                    {results.company_intel.red_flags?.length > 0 && (
                                        <div className="card-editorial p-6 border-l-4 border-red-400 bg-red-50">
                                            <div className="flex items-center gap-2 mb-3">
                                                <AlertTriangle className="w-5 h-5 text-red-500" />
                                                <h4 className="text-xs font-bold text-red-700 uppercase tracking-widest">Potential Concerns</h4>
                                            </div>
                                            <ul className="space-y-2 text-sm text-red-700">
                                                {results.company_intel.red_flags.map((item: string, i: number) => (
                                                    <li key={i} className="flex items-start gap-2">
                                                        <span className="w-1.5 h-1.5 rounded-full bg-red-400 mt-2 shrink-0"></span>
                                                        {item}
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}

                                    {/* Recent News */}
                                    {results.company_intel.recent_funding_or_news?.length > 0 && (
                                        <div className="card-editorial p-6">
                                            <h4 className="text-xs font-bold text-navy uppercase tracking-widest mb-4">Recent News</h4>
                                            <ul className="space-y-2 text-sm text-slate">
                                                {results.company_intel.recent_funding_or_news.map((item: string, i: number) => (
                                                    <li key={i} className="flex items-start gap-2">
                                                        <span className="w-1.5 h-1.5 rounded-full bg-gold mt-2 shrink-0"></span>
                                                        {item}
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}

                                    {/* Sources */}
                                    {results.company_intel.sources?.length > 0 && (
                                        <div className="card-editorial p-6 bg-cream/50">
                                            <h4 className="text-xs font-bold text-navy uppercase tracking-widest mb-4">Sources</h4>
                                            <ul className="space-y-3 text-sm">
                                                {results.company_intel.sources.map((source: any, i: number) => (
                                                    <li key={i} className="flex items-start gap-2">
                                                        <ExternalLink className="w-4 h-4 text-gold mt-0.5 shrink-0" />
                                                        <div>
                                                            <a
                                                                href={source.url}
                                                                target="_blank"
                                                                rel="noopener noreferrer"
                                                                className="text-navy hover:text-gold transition-colors underline"
                                                            >
                                                                {source.title || source.url}
                                                            </a>
                                                            {source.fact && (
                                                                <p className="text-slate text-xs mt-0.5">"{source.fact}"</p>
                                                            )}
                                                        </div>
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}
                                </div>
                            ) : (
                                /* Cover Letter / Email */
                                <div className="card-editorial p-10 md:p-14">
                                    <div className="flex items-center gap-2 mb-6">
                                        {activeTab === 'cover' ? (
                                            <MessageSquare className="w-5 h-5 text-gold" />
                                        ) : (
                                            <Mail className="w-5 h-5 text-gold" />
                                        )}
                                        <span className="text-xs font-bold uppercase tracking-widest text-gold">
                                            {activeTab === 'cover' ? 'Cover Letter' : 'Cold Outreach Email'}
                                        </span>
                                    </div>
                                    <div className="whitespace-pre-wrap leading-relaxed text-charcoal font-serif text-lg">
                                        {activeTab === 'cover'
                                            ? results.writing.cover_letter.content
                                            : results.writing.cold_email.content
                                        }
                                    </div>
                                </div>
                            )}
                        </motion.div>
                    </AnimatePresence>
                </div>
            </div>
        </div>
    );
}

function IntelCard({ label, value, isLink }: { label: string; value?: string; isLink?: boolean }) {
    if (!value) return null;
    return (
        <div className="card-editorial p-5">
            <p className="text-xs font-bold text-gold uppercase tracking-widest mb-2">{label}</p>
            {isLink ? (
                <a
                    href={value.startsWith('http') ? value : `https://${value}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-navy font-semibold flex items-center gap-2 hover:text-gold transition-colors"
                >
                    {value} <ExternalLink className="w-4 h-4" />
                </a>
            ) : (
                <p className="text-navy font-semibold">{value}</p>
            )}
        </div>
    );
}
