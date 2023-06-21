import os
import subprocess
import threading
import shutil
import random
terminal_width, _ = shutil.get_terminal_size()

# Directory containing audio files
AUDIO_DIR = '.'
# Path to the text file containing filenames and text
LOG_FILE = 'log.txt'

def check_audio_status(audio_process):
    while audio_process.poll() is None:
        # Audio process is still running
        continue
    # Audio process has finished
    notif=['/dinga.wav','/dingd.wav','/dingfs.wav']
    subprocess.Popen(['mpv', random.choice(notif)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Change the player command as per your system

def play_audio(file_path):
    """Plays the audio file using a system player"""
    audio_process = subprocess.Popen(['mpv', file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Change the player command as per your system

    # Start a separate thread to check audio status
    status_thread = threading.Thread(target=check_audio_status, args=(audio_process,))
    status_thread.start()
    return audio_process

def read_text(file_path):
    """Reads and returns the associated text for a file from the text file"""
    with open(LOG_FILE, 'r') as f:
        for line in f:
            filename, text = line.strip().split('|')
            if filename == file_path:
                return text
    return None

def good(sss,file_path):
    """Re-processes a file (placeholder function)"""
    # Add your re-processing logic here
    # Do nothing to the log fil
    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove lines starting with the given string
    removed_lines = [line for line in lines if line.startswith(sss)]
    lines = [line for line in lines if not line.startswith(sss)]

    # Write the modified contents back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

    # Write removed lines to the destination file
    with open('good.txt', 'a') as removed_file:
        removed_file.writelines(removed_lines)


def bad(sss,file_path):
    """Marks a file as ready (placeholder function)"""
    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove lines starting with the given string
    removed_lines = [line for line in lines if line.startswith(sss)]
    lines = [line for line in lines if not line.startswith(sss)]

    # Write the modified contents back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

    # Write removed lines to the destination file
    with open('bad.txt', 'a') as removed_file:
        removed_file.writelines(removed_lines)

def mid(sss,file_path):
    """Could use some reprocessing..."""
    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove lines starting with the given string
    removed_lines = [line for line in lines if line.startswith(sss)]
    lines = [line for line in lines if not line.startswith(sss)]

    # Write the modified contents back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

    # Write removed lines to the destination file
    with open('mid.txt', 'a') as removed_file:
        removed_file.writelines(removed_lines)


def main():
    # Get a list of audio files in the directory
    audio_files = [file for file in os.listdir(AUDIO_DIR) if file.startswith('out_') and file.endswith('.wav')]

    with open(LOG_FILE, 'r') as files:
        for line in files:
            file = line.strip().split('|')[0]
            # Iterate through the audio files
            while True:
                file_path = os.path.join(AUDIO_DIR, file)
                print(f"Playing file: {file_path}")
                print(str(read_text(file)).center(terminal_width))
                process = play_audio(file_path)

                # Prompt user for action
                while True:
                    print("Commands:")
                    print("u - Good")
                    print("h - Bad")
                    print("t - Mid")
                    action = input("Enter command:")
                    if action == 'u':
                        # GOod!
                        good(file,LOG_FILE)
                        break
                    elif action == 'h':
                        # BAD
                        bad(file,LOG_FILE)
                        break
                    elif action == 't':
                        # mid
                        mid(file,LOG_FILE)
                        break
                    elif action == 'r':
                        # replay audio
                        process = play_audio(file_path)
                    else:
                        pass
                break
            process.terminate()


if __name__ == '__main__':
    main()

