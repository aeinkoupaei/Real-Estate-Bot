"""
Voice Message Handler for Real Estate Bot
Performs speech-to-text conversion using OpenAI transcription models.
"""
import asyncio

import openai

import config


class VoiceHandler:
    """
    Converts user voice messages to text using OpenAI APIs.
    """

    def __init__(self):
        self.available = bool(config.OPENAI_API_KEY)
        if self.available:
            openai.api_key = config.OPENAI_API_KEY
            self.model = getattr(
                config, "OPENAI_TRANSCRIPTION_MODEL", "whisper-1"
            )

    async def voice_to_text(self, voice_file_path):
        """
        Convert an audio file path into transcribed text.
        """
        if not self.available:
            return None

        loop = asyncio.get_running_loop()
        try:
            return await loop.run_in_executor(
                None, self._transcribe_file, voice_file_path
            )
        except Exception as exc:
            print(f"Error converting voice to text with OpenAI: {exc}")
            return None

    def _transcribe_file(self, voice_file_path):
        with open(voice_file_path, "rb") as audio_file:
            result = openai.Audio.transcribe(self.model, audio_file)
            if isinstance(result, dict):
                return result.get("text", "").strip()
            if hasattr(result, "text"):
                return result.text.strip()
            return None

    def is_available(self):
        """Return True if transcription service is configured."""
        return self.available
