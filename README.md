# dataset-tools
Python tools to build ai datasets

Currently, the following files and workflows are structured for building a dataset for use with VITS/so-vits-svc. These are text to audio or audio to audio ai systems. 

# VITS Dataset Workflow

This assumes you're using a Linux system (or WSL) with modern `python3` and `sox`. 

1. First, download the stream(s) you want to use for the dataset. The requirements for the stream are as follows: the less background noise/music the better, and primarily the target voice talking a ton (more talking = more data). Minecraft livestreams seem to be pretty good from what I've tested. (This uses [yt-dlp](https://github.com/yt-dlp/yt-dlp))
   Use the command below to download the stream(s):
   `yt-dlp -f ba -x --audio-format "wav" --audio-quality 0 --embed-metadata https://youtu.be/dh4s0bBrPx0`

2. Once you have the stream, you'll need to split it into multiple files because it's too computationally hard to  process a 3 hour stream. Use the command below to split the file based off of the silence it detects. This may result in longer files if the background sounds/music are as loud as the speech in the source. This command assumes the input stream is `input.wav`:
   `sox input.wav split.wav silence 1 5.0 0.1% 1 0.3 0.1% : newfile : restart`

3. Next, you need to run this through [UVR5](https://ultimatevocalremover.com/) to remove all background sounds. Since we have the files, you can just select all the files as input for the software, and make a folder for the output. Use the following settings once you've set the input and output settings:

   - **Choose Process Method**
     - VR Architecture
   - **Window Size**
     - 512
   - **Aggression Setting**
     - 10
   - **Choose VR Model** (you download these in the settings of the program)
     - `6_HP-Karaoke-UVR`
   - Vocals Only, GPU Conversion

   Then click *Start Processing* to begin. This can take a few minutes to hours depending on the GPU you have! My 3070 took 6.5 minutes to process ~ 2.5 hours of Minecraft stream audio.

   There are chances that it fails when doing this step, just ignore it.

4. Once you have a directory with all the processed files,  we need to run it through `sox` to remove the silence from the lack of background music and sound effects. 

   When you're at this step, make sure you're in the folder with the processed wav files.
   `for file in *.wav; do sox "$file" "desilenced_${file}" silence 1 0.3 1% 1 0.3 1%; done `

5. Now that we have a bunch of audio files of speech, we need to run it through Openai's whisper to transcribe it into use-able data. To do this, install whisper to the system you're using ([guide on this page](https://github.com/openai/whisper/releases)). I've written a python script `whisper_transcript.py` that will do this.

6. In the directory, run this command (assuming the `whisper_transcript.py` is in the same directory)
   `python3 whisper_transcript.py`

7. Note: In the python file, change the model according to the VRAM you have

|  Size  | Parameters | English-only model | Multilingual model | Required VRAM | Relative speed |
|:------:|:----------:|:------------------:|:------------------:|:-------------:|:--------------:|
|  tiny  |    39 M    |     `tiny.en`      |       `tiny`       |     ~1 GB     |      ~32x      |
|  base  |    74 M    |     `base.en`      |       `base`       |     ~1 GB     |      ~16x      |
| small  |   244 M    |     `small.en`     |      `small`       |     ~2 GB     |      ~6x       |
| medium |   769 M    |    `medium.en`     |      `medium`      |     ~5 GB     |      ~2x       |
| large  |   1550 M   |        N/A         |      `large`       |    ~10 GB     |       1x       |

8. Cool, now you have a dataset with the files beginning with `out_` and a log with `transcript.txt`.

# Dataset Cleaning
(If you really want a clean dataset, this tool will help)
`python3 process.py`
