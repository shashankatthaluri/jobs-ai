/**
 * API client for the Jobs backend.
 * 
 * Multi-step flow:
 * 1. analyzeApplication() - CV parsing + JD analysis + skill gap
 * 2. tailorApplication() - Final tailoring with confirmed skills
 */

import { createClient } from '@/lib/supabase/client';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ============================================================
// Auth Helper - Get JWT for authenticated requests
// ============================================================

async function getAuthHeaders(): Promise<HeadersInit> {
    const supabase = createClient();
    const { data: { session } } = await supabase.auth.getSession();

    if (session?.access_token) {
        return {
            'Authorization': `Bearer ${session.access_token}`,
        };
    }
    return {};
}

// ============================================================
// Types for Multi-Step Flow
// ============================================================

export interface SkillMatch {
    skill: string;
    found_in_cv: boolean;
    source: string;
}

export interface SkillGapAnalysis {
    matched_skills: SkillMatch[];
    missing_skills: string[];
    preferred_skills_matched: string[];
    preferred_skills_missing: string[];
    match_percentage: number;
}

export interface AnalysisResponse {
    master_cv: any;
    job_analysis: {
        role_title: string;
        department: string;
        seniority_level: string;
        employment_type: string;
        required_skills: string[];
        preferred_skills: string[];
        responsibilities: string[];
        keywords_for_ats: string[];
        industry: string;
    };
    company_intel: {
        company_name: string;
        website: string;
        industry: string;
        employee_count_range: string;
        company_stage: string;
        recent_funding_or_news: string[];
        hiring_contacts: any[];
    };
    skill_gap: SkillGapAnalysis;
    cv_warnings: string[];
}

export interface TailorRequest {
    master_cv: any;
    job_analysis: any;
    company_intel: any;
    confirmed_skills: {
        confirmed_missing_skills: string[];
    };
}

export interface TailorResponse {
    resume_markdown: string;
    cover_letter: string;
    cold_email: string;
    company_summary: string;
    keywords_used: string[];
    matched_skills: string[];
}

// ============================================================
// Step 1: Analyze (CV + JD + Company + Skill Gap)
// ============================================================

export async function analyzeApplication(
    cvFile: File,
    jobDescription: string,
    jobUrl: string,
    companyUrl: string  // Changed from companyName to companyUrl
): Promise<AnalysisResponse> {
    const formData = new FormData();
    formData.append('cv_pdf', cvFile);
    if (jobDescription) formData.append('job_description', jobDescription);
    if (jobUrl) formData.append('job_url', jobUrl);
    formData.append('company_url', companyUrl);

    const authHeaders = await getAuthHeaders();
    const response = await fetch(`${API_BASE}/api/analyze/step1`, {
        method: 'POST',
        headers: authHeaders,
        body: formData,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Analysis failed');
    }

    return response.json();
}

// ============================================================
// Step 2: Tailor (with confirmed skills)
// ============================================================

export async function tailorApplication(
    request: TailorRequest
): Promise<TailorResponse> {
    const authHeaders = await getAuthHeaders();
    const response = await fetch(`${API_BASE}/api/analyze/step2/tailor`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...authHeaders,
        },
        body: JSON.stringify(request),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Tailoring failed');
    }

    return response.json();
}

// ============================================================
// Legacy: Single-step process (kept for backwards compatibility)
// ============================================================

export interface ProcessResponse {
    master_cv: any;
    job_analysis: any;
    company_intel: any;
    tailored_resume: {
        resume_markdown: string;
        matched_skills: string[];
        keywords_used: string[];
        relevance_summary: string;
    };
    writing: {
        cover_letter: { content: string; word_count: number };
        cold_email: { content: string; word_count: number };
        company_summary: { content: string; word_count: number };
    };
    warnings: string[];
}

export async function processApplication(
    cvFile: File,
    jobDescription: string,
    jobUrl: string,
    companyName: string
): Promise<ProcessResponse> {
    const formData = new FormData();
    formData.append('cv_pdf', cvFile);
    if (jobDescription) formData.append('job_description', jobDescription);
    if (jobUrl) formData.append('job_url', jobUrl);
    formData.append('company_name', companyName);

    const response = await fetch(`${API_BASE}/api/process/all`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Processing failed');
    }

    return response.json();
}
