"""LLM API adapter with multi-model support."""
import os
import json
from typing import Dict, Optional
from ..config import Config
from ..logger import logger

class LLMAdapter:
    """Unified interface for different LLM providers."""
    
    def __init__(self, model: str = "gpt-4"):
        self.model = model
        self.client = None
        self._setup_client()
    
    def _setup_client(self):
        """Initialize appropriate client based on model."""
        if self.model.startswith("gpt"):
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
                logger.info(f"Initialized OpenAI client: {self.model}")
            except ImportError:
                logger.warning("OpenAI library not installed. Run: pip install openai")
        
        elif self.model.startswith("gemini"):
            try:
                import google.generativeai as genai
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.client = genai.GenerativeModel(self.model)
                logger.info(f"Initialized Gemini client: {self.model}")
            except ImportError:
                logger.warning("Google AI library not installed. Run: pip install google-generativeai")
        
        elif self.model.startswith("claude"):
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
                logger.info(f"Initialized Anthropic client: {self.model}")
            except ImportError:
                logger.warning("Anthropic library not installed. Run: pip install anthropic")
    
    def generate(self, prompt: str, max_tokens: int = 4000, 
                temperature: float = 0.7, json_mode: bool = False) -> str:
        """
        Generate text from prompt.
        
        Args:
            prompt: The prompt text
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            json_mode: Force JSON output
            
        Returns:
            Generated text
        """
        if not self.client:
            return self._mock_response(prompt, json_mode)
        
        try:
            if self.model.startswith("gpt"):
                return self._generate_openai(prompt, max_tokens, temperature, json_mode)
            elif self.model.startswith("gemini"):
                return self._generate_gemini(prompt, max_tokens, temperature)
            elif self.model.startswith("claude"):
                return self._generate_claude(prompt, max_tokens, temperature)
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return self._mock_response(prompt, json_mode)
    
    def _generate_openai(self, prompt: str, max_tokens: int, 
                        temperature: float, json_mode: bool) -> str:
        """Generate using OpenAI API."""
        kwargs = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        
        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    
    def _generate_gemini(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate using Gemini API."""
        response = self.client.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": max_tokens,
                "temperature": temperature
            }
        )
        return response.text
    
    def _generate_claude(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate using Anthropic Claude API."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    def _mock_response(self, prompt: str, json_mode: bool) -> str:
        """Return mock response when no API available."""
        if json_mode:
            return json.dumps({
                "title": "Mock Başlık - API Key Gerekli",
                "abstract_tr": "Bu bir test yanıtıdır. Gerçek içerik üretmek için API key ekleyin.",
                "sections": [],
                "note": "API key missing - using mock response"
            })
        return "Mock response: API key gerekli. .env dosyasına API anahtarınızı ekleyin."
