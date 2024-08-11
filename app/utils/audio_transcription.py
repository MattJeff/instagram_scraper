# app/utils/audio_transcription.py
# Transcription de l'audio en texte via l'API AssemblyAI.

import assemblyai as aai
import config

def transcribe_audio_with_api(mp3_path):
    print(f"Début de la transcription de l'audio à partir de: {mp3_path}")
    configaai = aai.settings.api_key = config.Config.ASSEMBLYAI_API_KEY
    configaai = aai.TranscriptionConfig(speech_model=aai.SpeechModel.nano)
    configaai = aai.TranscriptionConfig(language_detection=True)
    transcriber = aai.Transcriber(config=configaai)

    with open(mp3_path, 'rb') as audio_file:
        transcript = transcriber.transcribe(audio_file)

    if transcript.status == aai.TranscriptStatus.error:
        print(f"Erreur lors de la transcription: {transcript.error}")
    else:
        print(f"Transcription réussie: {transcript.text}")
        return transcript
