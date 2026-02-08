'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle2, AlertCircle, Sparkles } from 'lucide-react';
import { SkillGapAnalysis } from '@/lib/api';

interface SkillGapConfirmationProps {
    skillGap: SkillGapAnalysis;
    confirmedSkills: string[];
    onToggleSkill: (skill: string) => void;
    onConfirm: () => void;
    isProcessing: boolean;
}

/**
 * Skill Gap Confirmation Component
 * 
 * Shows matched and missing skills from CV vs JD comparison.
 * User can toggle missing skills they actually have.
 */
export default function SkillGapConfirmation({
    skillGap,
    confirmedSkills,
    onToggleSkill,
    onConfirm,
    isProcessing
}: SkillGapConfirmationProps) {
    const totalRequired = skillGap.matched_skills.length + skillGap.missing_skills.length;
    const matchedCount = skillGap.matched_skills.length + confirmedSkills.length;
    const matchPercentage = totalRequired > 0 ? Math.round((matchedCount / totalRequired) * 100) : 0;

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-8"
        >
            {/* Header */}
            <div className="text-center">
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gold/10 text-gold mb-4">
                    <Sparkles className="w-4 h-4" />
                    <span className="text-sm font-semibold">Skill Analysis Complete</span>
                </div>
                <h2 className="font-display text-3xl font-bold text-navy mb-2">
                    Confirm Your Skills
                </h2>
                <p className="text-slate max-w-lg mx-auto">
                    We found some skills in the job description that weren't in your CV.
                    Toggle any skills you actually have so we can include them.
                </p>
            </div>

            {/* Match Score */}
            <div className="flex items-center justify-center gap-8 p-6 bg-cream-dark rounded-xl">
                <div className="text-center">
                    <div className="font-display text-4xl font-bold text-navy">{matchPercentage}%</div>
                    <div className="text-sm text-stone">Match Score</div>
                </div>
                <div className="w-px h-12 bg-cloud"></div>
                <div className="text-center">
                    <div className="font-display text-4xl font-bold text-gold">{matchedCount}</div>
                    <div className="text-sm text-stone">of {totalRequired} Skills</div>
                </div>
            </div>

            {/* Matched Skills (from CV) */}
            <div className="space-y-4">
                <h3 className="font-display text-lg font-semibold text-navy flex items-center gap-2">
                    <CheckCircle2 className="w-5 h-5 text-green-600" />
                    Found in Your CV ({skillGap.matched_skills.length})
                </h3>
                <div className="flex flex-wrap gap-2">
                    {skillGap.matched_skills.map((match) => (
                        <div
                            key={match.skill}
                            className="px-4 py-2 rounded-full bg-green-50 text-green-700 border border-green-200 text-sm font-medium flex items-center gap-2"
                        >
                            <CheckCircle2 className="w-4 h-4" />
                            {match.skill}
                        </div>
                    ))}
                </div>
            </div>

            {/* Missing Skills (toggleable) */}
            {skillGap.missing_skills.length > 0 && (
                <div className="space-y-4">
                    <h3 className="font-display text-lg font-semibold text-navy flex items-center gap-2">
                        <AlertCircle className="w-5 h-5 text-amber-500" />
                        Not Found in CV — Do You Have These?
                    </h3>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        {skillGap.missing_skills.map((skill) => {
                            const isConfirmed = confirmedSkills.includes(skill);
                            return (
                                <button
                                    key={skill}
                                    type="button"
                                    onClick={() => onToggleSkill(skill)}
                                    className={`p-4 rounded-xl border-2 transition-all flex items-center justify-between group
                                        ${isConfirmed
                                            ? 'bg-gold/10 border-gold text-navy'
                                            : 'bg-white border-cloud hover:border-gold/50 text-slate'
                                        }`}
                                >
                                    <span className="font-medium">{skill}</span>
                                    <div className={`w-12 h-6 rounded-full transition-all relative
                                        ${isConfirmed ? 'bg-gold' : 'bg-mist'}`}
                                    >
                                        <div className={`absolute top-1 w-4 h-4 rounded-full bg-white shadow transition-all
                                            ${isConfirmed ? 'left-7' : 'left-1'}`}
                                        ></div>
                                    </div>
                                </button>
                            );
                        })}
                    </div>
                </div>
            )}

            {/* Preferred Skills (info only) */}
            {skillGap.preferred_skills_matched.length > 0 && (
                <div className="p-4 bg-blue-50 rounded-xl border border-blue-100">
                    <h4 className="text-sm font-semibold text-blue-800 mb-2">
                        Bonus: You also match these preferred skills
                    </h4>
                    <div className="flex flex-wrap gap-2">
                        {skillGap.preferred_skills_matched.map((skill) => (
                            <span key={skill} className="px-3 py-1 rounded-full bg-blue-100 text-blue-700 text-sm">
                                {skill}
                            </span>
                        ))}
                    </div>
                </div>
            )}

            {/* Confirm Button */}
            <button
                onClick={onConfirm}
                disabled={isProcessing}
                className="btn-gold w-full h-16 text-lg font-semibold flex items-center justify-center gap-3"
            >
                {isProcessing ? (
                    <>
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        Tailoring Your Application...
                    </>
                ) : (
                    <>
                        Generate Tailored Resume
                        <span className="text-sm opacity-75">& Cover Letter</span>
                    </>
                )}
            </button>
        </motion.div>
    );
}
