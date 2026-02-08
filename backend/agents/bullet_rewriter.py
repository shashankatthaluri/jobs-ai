"""Agent 2: Bullet Rewriter - Enhanced with Voice Mirroring.

Rewrites selected bullets for ATS optimization AND company voice matching.
Preserves meaning, injects keywords only if truthful.
Transforms writing style to match target company.
"""
from models.cv import MasterCV
from models.job import CompanyVoiceProfile
from models.tailoring import MatchingResult, RewriteResult
from services.llm import llm_service


def _build_voice_instructions(voice_profile: CompanyVoiceProfile | None) -> str:
    """Build voice mirroring instructions from profile."""
    if not voice_profile:
        return "Use standard professional resume style."
    
    instructions = []
    
    # Sentence style
    if voice_profile.sentence_style == "short_punchy":
        instructions.append("Write SHORT, PUNCHY sentences. Max 15 words each. No fluff.")
    elif voice_profile.sentence_style == "detailed":
        instructions.append("Write complete, detailed sentences with context.")
    else:
        instructions.append("Balance brevity with clarity.")
    
    # Ownership level
    if voice_profile.ownership_level == "strong":
        instructions.append("Use STRONG ownership verbs: Owned, Led, Built, Drove, Shipped.")
    elif voice_profile.ownership_level == "passive":
        instructions.append("Use modest language: Contributed, Supported, Assisted.")
    else:
        instructions.append("Use balanced ownership: Managed, Developed, Implemented.")
    
    # Metric emphasis
    if voice_profile.metric_emphasis == "heavy":
        instructions.append("EVERY bullet must have a metric (%, $, count, time).")
    elif voice_profile.metric_emphasis == "light":
        instructions.append("Focus on outcomes, metrics optional.")
    else:
        instructions.append("Include metrics where available.")
    
    # Tone
    if voice_profile.tone == "aggressive":
        instructions.append("Use bold, confident language. No hedging.")
    elif voice_profile.tone == "collaborative":
        instructions.append("Emphasize team impact and cross-functional work.")
    elif voice_profile.tone == "casual":
        instructions.append("Use conversational, direct language.")
    else:
        instructions.append("Maintain professional, formal tone.")
    
    # Value vocabulary
    if voice_profile.value_vocabulary:
        vocab = ", ".join(voice_profile.value_vocabulary[:5])
        instructions.append(f"Mirror these company values in language: {vocab}")
    
    # Sample phrases
    if voice_profile.sample_phrases:
        phrases = " | ".join(voice_profile.sample_phrases[:3])
        instructions.append(f"Emulate these phrase patterns: {phrases}")
    
    # Custom instructions
    if voice_profile.style_instructions:
        instructions.append(voice_profile.style_instructions)
    
    return "\n".join(instructions)


# Enhanced prompt with voice mirroring
BULLET_REWRITER_PROMPT = """You are a professional resume editor specializing in ATS optimization AND company voice matching.

Inputs:
1. Relevant experience JSON (from matching step)
2. Job keywords list
3. Original CV experience with dates
4. Company voice instructions

Your task:
1. Rewrite bullets for clarity and ATS keyword alignment.
2. MATCH THE COMPANY'S WRITING STYLE using the voice instructions.
3. Preserve original meaning and facts.
4. Use strong action verbs matching company's ownership level.
5. Inject keywords ONLY if they are truthful.
6. Include start_date and end_date from the original CV.

VOICE MIRRORING RULES:
{voice_instructions}

General Rules:
- Do NOT add new responsibilities.
- Do NOT change metrics or outcomes.
- Keep bullets concise but complete (aim for 1-3 lines, prioritize clarity over brevity).
- If a bullet already matches well, return it unchanged.
- Preserve exact dates from original CV.
- The bullet should SOUND LIKE it was written by someone at the target company.

Output JSON:

{
  "rewritten_experience": [
    {
      "company": "",
      "role": "",
      "start_date": "",
      "end_date": "",
      "bullets": []
    }
  ]
}

Output ONLY valid JSON.
No commentary."""


async def rewrite_bullets(
    cv: MasterCV,
    matching: MatchingResult,
    job_keywords: list[str],
    voice_profile: CompanyVoiceProfile | None = None
) -> RewriteResult:
    """
    Rewrite bullets for ATS optimization with company voice matching.
    
    Args:
        cv: Original Master CV (for dates)
        matching: MatchingResult from matching step
        job_keywords: Keywords to inject where truthful
        voice_profile: Company voice profile for style mirroring
        
    Returns:
        RewriteResult with optimized, voice-matched bullets
    """
    # Build experience lookup for dates
    date_lookup = {}
    for exp in cv.experience:
        key = f"{exp.company}|{exp.role}"
        date_lookup[key] = {
            "start_date": exp.start_date,
            "end_date": exp.end_date
        }
    
    # Prepare relevant experience with dates
    relevant_exp_with_dates = []
    for rel_exp in matching.relevant_experience:
        key = f"{rel_exp.company}|{rel_exp.role}"
        dates = date_lookup.get(key, {"start_date": "", "end_date": ""})
        relevant_exp_with_dates.append({
            "company": rel_exp.company,
            "role": rel_exp.role,
            "start_date": dates["start_date"],
            "end_date": dates["end_date"],
            "relevance_score": rel_exp.relevance_score,
            "matched_skills": rel_exp.matched_skills,
            "relevant_bullets": rel_exp.relevant_bullets
        })
    
    # Build voice instructions
    voice_instructions = _build_voice_instructions(voice_profile)
    
    # Create prompt with voice instructions injected
    system_prompt = BULLET_REWRITER_PROMPT.replace("{voice_instructions}", voice_instructions)
    
    user_prompt = f"""Rewrite these resume bullets for ATS optimization AND company voice matching.

RELEVANT EXPERIENCE:
{relevant_exp_with_dates}

JOB KEYWORDS TO USE (if truthful):
{job_keywords}

VOICE PROFILE SUMMARY:
- Style: {voice_profile.sentence_style if voice_profile else 'balanced'}
- Ownership: {voice_profile.ownership_level if voice_profile else 'moderate'}
- Metrics: {voice_profile.metric_emphasis if voice_profile else 'moderate'}
- Tone: {voice_profile.tone if voice_profile else 'professional'}

Return rewritten experience as JSON. Make bullets SOUND LIKE this company's employees write."""
    
    try:
        result = await llm_service.generate_json(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3  # Slightly higher for natural variation
        )
        
        return RewriteResult(**result)
        
    except Exception as e:
        raise ValueError(f"Failed to rewrite bullets: {e}")
