"""Agent 3: Job URL Resolver.

Extracts job description content from job posting URLs.
Removes navigation, footers, and boilerplate.
"""
import httpx
import re
from services.llm import llm_service


# LOCKED PROMPT - DO NOT MODIFY
URL_CONTENT_EXTRACTOR_PROMPT = """You are a web content extraction specialist.

Input: Raw HTML or text from a job posting page.

Your task:
1. Extract only the job description content.
2. Remove navigation, footer, company boilerplate, and legal text.
3. Preserve headings, bullet points, and structure.
4. Do NOT summarize or rewrite.

Output:
- Clean job description text only
- No explanations
- No markdown"""


async def fetch_url_content(url: str) -> str:
    """
    Fetch raw content from a URL.
    
    Args:
        url: Job posting URL
        
    Returns:
        Raw HTML/text content
        
    Raises:
        ValueError: If fetch fails
    """
    try:
        async with httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
            
    except Exception as e:
        raise ValueError(f"Failed to fetch URL: {e}")


def basic_html_to_text(html: str) -> str:
    """
    Basic HTML to text conversion.
    
    Removes scripts, styles, and converts common HTML to text.
    """
    # Remove scripts and styles
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<noscript[^>]*>.*?</noscript>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Convert common elements
    html = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
    html = re.sub(r'<p[^>]*>', '\n\n', html, flags=re.IGNORECASE)
    html = re.sub(r'</p>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<li[^>]*>', '\n• ', html, flags=re.IGNORECASE)
    html = re.sub(r'<h[1-6][^>]*>', '\n\n', html, flags=re.IGNORECASE)
    html = re.sub(r'</h[1-6]>', '\n', html, flags=re.IGNORECASE)
    
    # Remove remaining tags
    html = re.sub(r'<[^>]+>', ' ', html)
    
    # Clean up whitespace
    html = re.sub(r'&nbsp;', ' ', html)
    html = re.sub(r'&amp;', '&', html)
    html = re.sub(r'&lt;', '<', html)
    html = re.sub(r'&gt;', '>', html)
    html = re.sub(r'&#\d+;', '', html)
    html = re.sub(r'&\w+;', '', html)
    
    # Normalize whitespace
    lines = []
    for line in html.split('\n'):
        line = ' '.join(line.split())
        if line:
            lines.append(line)
    
    return '\n'.join(lines)


async def extract_jd_from_url(url: str) -> str:
    """
    Extract clean job description from a job posting URL.
    
    Args:
        url: Job posting URL (LinkedIn, Indeed, company site, etc.)
        
    Returns:
        Clean job description text
        
    Raises:
        ValueError: If extraction fails
    """
    # Fetch raw content
    raw_html = await fetch_url_content(url)
    
    # Basic HTML to text conversion
    raw_text = basic_html_to_text(raw_html)
    
    # Limit text length for LLM (take middle portion which usually has JD)
    if len(raw_text) > 15000:
        # Take a portion more likely to contain the JD
        start = len(raw_text) // 4
        end = start + 12000
        raw_text = raw_text[start:end]
    
    # Use LLM to extract clean JD
    try:
        clean_jd = await llm_service.generate_text(
            user_prompt=f"Extract the job description from this content:\n\n{raw_text}",
            system_prompt=URL_CONTENT_EXTRACTOR_PROMPT,
            temperature=0.1
        )
        
        return clean_jd.strip()
        
    except Exception as e:
        raise ValueError(f"Failed to extract job description: {e}")
