import os
import subprocess
import threading
import shutil
import random
terminal_width, _ = shutil.get_terminal_size()

# Directory containing audio files
AUDIO_DIR = '.'
# Path to the text file containing filenames and text
LOG_FILE = 'transcript.txt'

def check_audio_status(audio_process):
    while audio_process.poll() is None:
        # Audio process is still running
        continue
    # Audio process has finished
    notif=['/home/rei/dinga.wav','/home/rei/dingd.wav','/home/rei/dingfs.wav']
    subprocess.Popen(['mpv', '--volume=50', random.choice(notif)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Change the player command as per your system

def play_audio(file_path):
    """Plays the audio file using a system player"""
    audio_process = subprocess.Popen(['mpv','--speed=2.0', file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Change the player command as per your system

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

def good(sss):
    """Re-processes a file (placeholder function)"""
    # Add your re-processing logic here
    # Do nothing to the log fil
    # Read the file
    with open(LOG_FILE, 'r') as file:
        lines = file.readlines()

    # Remove lines starting with the given string
    removed_lines = [line for line in lines if line.startswith(sss)]
    lines = [line for line in lines if not line.startswith(sss)]

    # Write the modified contents back to the file
    with open(LOG_FILE, 'w') as file:
        file.writelines(lines)

    # Write removed lines to the destination file
    with open('good.txt', 'a') as removed_file:
        removed_file.writelines(removed_lines)


def update(sss, new_string):
    """Updates the string and adds it back to LOG_FILE"""
    # Read the file
    with open(LOG_FILE, 'r') as file:
        lines = file.readlines()

    # Remove lines starting with the given string
    removed_lines = [line for line in lines if line.startswith(sss)]
    lines = [line for line in lines if not line.startswith(sss)]
    
    # Append the new string to the top of the lines
    new_string = str(sss) + "|" + new_string + '\n'
    lines.insert(0, new_string)

    # Write the modified contents back to the file
    with open(LOG_FILE, 'w') as file:
        file.writelines(lines)

    # Write removed lines to the destination file
    with open(LOG_FILE, 'a') as removed_file:
        removed_file.writelines(removed_lines)

def bad(sss):
    """Marks a file as ready (placeholder function)"""
    # Read the file
    with open(LOG_FILE, 'r') as file:
        lines = file.readlines()

    # Remove lines starting with the given string
    removed_lines = [line for line in lines if line.startswith(sss)]
    lines = [line for line in lines if not line.startswith(sss)]

    # Write the modified contents back to the file
    with open(LOG_FILE, 'w') as file:
        file.writelines(lines)

    # Write removed lines to the destination file
    with open('bad.txt', 'a') as removed_file:
        removed_file.writelines(removed_lines)

def mid(sss):
    """Could use some reprocessing..."""
    # Read the file
    with open(LOG_FILE, 'r') as file:
        lines = file.readlines()

    # Remove lines starting with the given string
    removed_lines = [line for line in lines if line.startswith(sss)]
    lines = [line for line in lines if not line.startswith(sss)]

    # Write the modified contents back to the file
    with open(LOG_FILE, 'w') as file:
        file.writelines(lines)

    # Write removed lines to the destination file
    with open('mid.txt', 'a') as removed_file:
        removed_file.writelines(removed_lines)


def main():
    # Get a list of audio files in the directory
    #audio_files = [file for file in os.listdir(AUDIO_DIR) if file.startswith('out_') and file.endswith('.wav')]

    with open(LOG_FILE, 'r') as files:
        file_list = files.readlines()  # Read all lines into a list
        total_files = len(file_list)  # Get the total number of files
        
        for index, line in enumerate(file_list, start=1):
            file = line.strip().split('|')[0]
            file_path = os.path.join(AUDIO_DIR, file)
            while True:
                print(f"Playing file: {file_path} File Number: {index} out of {total_files}")                
                print(str(read_text(file)).center(terminal_width))
                process = play_audio(file_path)

                # Prompt user for action
                while True:
                    print("Commands:")
                    print("u - Good")
                    print("h - Bad")
                    print("r - Repeat")
                    print("e - Edit")
                    print("Anything else - exit")
                    action = input("Enter command:")
                    if action == 'u':
                        # GOod!
                        good(file)
                        break
                    elif action == 'h':
                        # BAD
                        bad(file)
                        break
                    elif action == 'r':
                        # replay audio
                        print(str(read_text(file)).center(terminal_width))
                        process = play_audio(file_path)
                    elif action == 'e':
                        print(str(read_text(file)).center(terminal_width))
                        n_string = input("Edit: ")
                        update(file,n_string)
                        print(str(read_text(file)).center(terminal_width))
                        process = play_audio(file_path)
                    else:
                        exit()
                break
            process.terminate()

def clean():
    """Move all unusable files to different folders"""
    move_files_from_list('bad.txt', 'bad')
    move_files_from_list('good.txt', 'good')

def move_files_from_list(filename, destination_folder):
    """Move files listed in the given file to the specified destination folder"""
    with open(filename, 'r') as file:
        for line in file:
            file_path = line.strip().split('|')[0]
            filename = os.path.basename(file_path)
            destination_path = os.path.join(destination_folder, filename)
            os.makedirs(destination_folder, exist_ok=True)  # Create the destination folder if it doesn't exist
            try:
                shutil.move(file_path, destination_path)
            except:
                pass



if __name__ == '__main__':
    main()
    print("You did it!")
    clean()


