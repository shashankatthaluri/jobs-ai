"""Agent: Voice Extractor.

Analyzes company content and extracts writing style/voice profile.
This enables resume bullets to mirror the company's communication style.
"""
from models.job import CompanyVoiceProfile
from services.llm import llm_service


VOICE_EXTRACTION_PROMPT = """You are an expert linguistic analyst specializing in corporate communication styles.

Your task: Analyze the company content and extract their WRITING STYLE, not their facts.

Input: Company website content, careers page, blog posts, about page.

Analyze and extract:

1. SENTENCE STRUCTURE
   - Do they use short, punchy sentences? ("Ship fast. Move faster.")
   - Or detailed, complex sentences with multiple clauses?
   - Average sentence length pattern

2. OWNERSHIP LANGUAGE
   - Strong ownership: "I owned", "Led", "Built", "Drove"
   - Moderate: "Managed", "Coordinated", "Supported"
   - Passive: "Was responsible for", "Assisted with"

3. METRIC EMPHASIS
   - Heavy: Every statement has numbers ("reduced 23%", "served 10M users")
   - Moderate: Some metrics mixed with qualitative
   - Light: Focus on outcomes without specific numbers

4. TONE
   - Aggressive: Bold claims, competitive language
   - Collaborative: Team-focused, inclusive language
   - Formal: Professional, traditional corporate
   - Casual: Conversational, startup-y

5. VALUE VOCABULARY
   - Specific words the company uses repeatedly
   - These reveal their priorities (e.g., "customer obsession", "ownership", "innovation")

6. SAMPLE PHRASES
   - 3-5 actual phrases from their content that exemplify their style

Return the following JSON:

{
  "sentence_style": "short_punchy" | "detailed" | "balanced",
  "avg_sentence_length": "short" | "medium" | "long",
  "ownership_level": "strong" | "moderate" | "passive",
  "metric_emphasis": "heavy" | "moderate" | "light",
  "tone": "aggressive" | "collaborative" | "formal" | "casual",
  "value_vocabulary": ["word1", "word2", "word3"],
  "sample_phrases": ["phrase1", "phrase2", "phrase3"],
  "style_instructions": "Specific instructions for writing in this company's style"
}

IMPORTANT:
- Extract from ACTUAL content provided
- Do NOT invent vocabulary not present in the text
- If content is limited, make reasonable inferences and note in style_instructions
- style_instructions should be actionable guidance for a resume writer

Output ONLY valid JSON. No explanations."""


async def extract_voice_profile(company_content: str, company_name: str = "") -> CompanyVoiceProfile:
    """
    Extract company voice profile from content.
    
    Args:
        company_content: Text from company website, careers, about page, blogs
        company_name: Optional company name for context
        
    Returns:
        CompanyVoiceProfile with extracted style characteristics
    """
    if not company_content.strip():
        # Return default profile if no content
        return CompanyVoiceProfile(
            sentence_style="balanced",
            ownership_level="moderate",
            metric_emphasis="moderate",
            tone="collaborative",
            style_instructions="Standard professional resume style."
        )
    
    user_prompt = f"""Analyze the writing style of this company.

COMPANY: {company_name or 'Unknown'}

CONTENT TO ANALYZE:
{company_content[:8000]}

Extract their voice profile as JSON."""

    try:
        result = await llm_service.generate_json(
            user_prompt=user_prompt,
            system_prompt=VOICE_EXTRACTION_PROMPT,
            temperature=0.2
        )
        
        return CompanyVoiceProfile(**result)
        
    except Exception as e:
        # Return default on error
        return CompanyVoiceProfile(
            sentence_style="balanced",
            ownership_level="moderate", 
            metric_emphasis="moderate",
            tone="collaborative",
            style_instructions=f"Could not extract voice profile: {e}. Use standard professional style."
        )


async def extract_voice_from_research(research_results: dict) -> CompanyVoiceProfile:
    """
    Extract voice profile from Tavily deep research results.
    
    Args:
        research_results: Output from tavily_service.deep_research_company()
        
    Returns:
        CompanyVoiceProfile with extracted style
    """
    company_name = research_results.get("company_name", "")
    
    # Combine all content from research results
    content_parts = []
    
    # Add summary
    if research_results.get("combined_summary"):
        content_parts.append(research_results["combined_summary"])
    
    # Add individual result contents
    for result in research_results.get("results", []):
        if result.get("content"):
            content_parts.append(result["content"])
    
    combined_content = "\n\n".join(content_parts)
    
    return await extract_voice_profile(combined_content, company_name)
