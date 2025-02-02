#!/usr/bin/env python3
import json
import csv
import os

# Set paths (adjust if needed)
DATA_DIR = "/home/zingg/Documents/swiss-tts"
JSON_PATH = os.path.join(DATA_DIR, "sentences_ch_de_transcribed.json")
AUDIO_DIR = os.path.join(DATA_DIR, "zh")
OUTPUT_CSV = os.path.join(DATA_DIR, "metadata.csv")

def clean_text(text):
    # Remove extra quotes and normalize whitespace
    text = text.strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    # Replace double quotes with single quotes
    text = text.replace('""', "'")
    text = text.replace('"', "'")
    return text

def is_valid_audio_file(filename):
    return not filename.startswith('.') and filename.endswith('.wav')

# Count statistics
total_entries = 0
entries_with_zh = 0
skipped_entries = 0
valid_files = set(f for f in os.listdir(AUDIO_DIR) if is_valid_audio_file(f))

print(f"Found {len(valid_files)} valid audio files")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as csvfile:
    # Use tab as delimiter for strict LJSpeech format
    writer = csv.writer(csvfile, delimiter='|')
    
    for entry in data:
        total_entries += 1
        idx = entry["id"]
        
        # Skip entries that don't have Zürich dialect
        if "ch_zh" not in entry:
            skipped_entries += 1
            continue
            
        wav_filename = f"ch_zh_{idx:04d}.wav"
        
        # Skip if audio file doesn't exist
        if wav_filename not in valid_files:
            print(f"Warning: {wav_filename} not found in audio directory!")
            skipped_entries += 1
            continue
            
        entries_with_zh += 1
        transcript = clean_text(entry["ch_zh"])
        
        # Write in LJSpeech format:
        # id|audio_path|text
        # Note: remove .wav from the ID
        base_name = wav_filename[:-4]  # Remove .wav extension from ID
        # Just use the filename without the path prefix
        writer.writerow([base_name, wav_filename, transcript])

# Print summary
print(f"\nProcessing complete!")
print(f"Total entries processed: {total_entries}")
print(f"Entries with Zürich dialect and valid audio: {entries_with_zh}")
print(f"Entries skipped: {skipped_entries}")
