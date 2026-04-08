from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
import json
import re
from urllib.parse import urlparse


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="The full url of the website to fetch and analyze.")

class MyCustomTool(BaseTool):
    name: str = "fetch_code"
    description: str = (
        "Fetch the frontend code of a website and analyze it for security vulnerabilities. "
        "The input should be a full url of the website to analyze. "
        "The output should be json format of the security vulnerabilities found in the frontend code."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        """Fetch and analyze website for security vulnerabilities."""
        try:
            # Validate URL
            parsed = urlparse(argument)
            if not parsed.scheme:
                argument = "https://" + argument
            
            # Fetch the website
            headers = {
                'User-Agent': 'Mozilla/5.0 (Security Scanner)'
            }
            response = requests.get(argument, headers=headers, timeout=10)
            response.raise_for_status()
            html_content = response.text
            
            # Analyze for vulnerabilities
            vulnerabilities = {}
            
            # Check for missing security headers
            headers_to_check = {
                'Content-Security-Policy': 'Missing CSP header',
                'X-Frame-Options': 'Missing X-Frame-Options',
                'X-Content-Type-Options': 'Missing X-Content-Type-Options',
                'Strict-Transport-Security': 'Missing HSTS header',
            }
            vulnerabilities['missing_headers'] = [
                header for header in headers_to_check.keys()
                if header not in response.headers
            ]
            
            # Check for common vulnerabilities in HTML/JS
            vulnerabilities['issues'] = []
            
            # Check for inline scripts
            if '<script' in html_content and '>' in html_content:
                if re.search(r'<script[^>]*>.*?</script>', html_content, re.DOTALL):
                    vulnerabilities['issues'].append("Inline JavaScript detected")
            
            # Check for eval() usage
            if 'eval(' in html_content:
                vulnerabilities['issues'].append("eval() usage detected")
            
            # Check for unescaped content
            if 'innerHTML' in html_content:
                vulnerabilities['issues'].append("innerHTML usage detected (potential XSS)")
            
            # Check for form submission to HTTP
            if re.search(r'<form[^>]*action=["\']http:', html_content):
                vulnerabilities['issues'].append("Form submitting to HTTP (not HTTPS)")
            
            # Check for hardcoded credentials
            if re.search(r'(password|api_key|secret|token)\s*[=:]\s*["\'][^"\']+["\']', html_content, re.IGNORECASE):
                vulnerabilities['issues'].append("Potential hardcoded credentials found")
            
            vulnerabilities['scan_status'] = 'completed'
            vulnerabilities['url'] = argument
            
            return json.dumps(vulnerabilities, indent=2)
            
        except requests.exceptions.RequestException as e:
            return json.dumps({
                'error': f'Failed to fetch website: {str(e)}',
                'url': argument,
                'scan_status': 'failed'
            }, indent=2)
        except Exception as e:
            return json.dumps({
                'error': f'Analysis failed: {str(e)}',
                'scan_status': 'error'
            }, indent=2)
