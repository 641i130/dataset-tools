import os, whisper, shutil

model = whisper.load_model("medium")
directory = "."  # Replace with the actual directory path
log_file = "transcript.txt"
def wfile(content):
    with open(log_file, 'a') as file:
        file.write(content)

# Iterate over each file in the directory
counter = 0
for filename in os.listdir(directory):
    if filename.endswith(".wav") and filename.startswith("desilenced_"):
        # filepath
        filepath = os.path.join(directory, filename)
        new_filename = f"out_{counter}.wav"  # Replace with the desired new file name
        new_filepath = os.path.join(directory, new_filename)
        shutil.move(filepath, new_filepath)
        filepath = new_filepath
        print(new_filepath)

        # Load audio and pad/trim it to fit 30 seconds
        audio = whisper.load_audio(filepath)
        audio = whisper.pad_or_trim(audio)

        # Make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        # Detect the spoken language
        #_, probs = model.detect_language(mel)
        #print(f"Detected language for {filename}: {max(probs, key=probs.get)}")

        # Decode the audio (change if you want a different lang)
        #options = whisper.DecodingOptions()
        options = whisper.DecodingOptions(language="en")
        result = whisper.decode(model, mel, options)

        # Print the recognized text
        out = f"{new_filename}|{result.text}\n"
        wfile(out)
        print(out)
        counter+=1
