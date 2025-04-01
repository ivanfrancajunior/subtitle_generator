# Video Subtitle Generator
```plaintext
# requirements.txt

# Biblioteca para manipulação de vídeos
moviepy==1.0.3

# Biblioteca para transcrição de áudio (AssemblyAI)
assemblyai==2.3.0

# Ferramenta para processamento de áudio (opcional, se necessário)
ffmpeg-python==0.2.0
```

```markdown
# Video Subtitle Generator

This project automates the process of generating subtitles (SRT files) for videos using AssemblyAI's transcription API. It extracts audio from videos, transcribes the audio into text, and saves the subtitles in SRT format.

## Features
- Validates video files (supports MP4 format).
- Extracts audio from videos and saves it as WAV files.
- Transcribes audio into Portuguese using AssemblyAI.
- Generates SRT subtitle files automatically.

## Prerequisites
Before running the project, ensure you have the following installed:
- Python 3.8 or higher.
- FFmpeg (required for audio extraction). You can install it from [here](https://ffmpeg.org/download.html).

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/video-subtitle-generator.git
   cd video-subtitle-generator
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your AssemblyAI API key:
   - Create an account at [AssemblyAI](https://www.assemblyai.com/) to get your API key.
   - Replace `your_api_key_here` in the script with your actual API key.

## Project Structure
```
project/
├── videos/       # Input videos (provided by the user)
├── audio/        # Extracted audio files (created automatically)
├── output/       # Generated SRT files (created automatically)
├── requirements.txt # List of dependencies
└── subtitle_gen_app.py # Main script
```

## Usage
1. Place your MP4 video files in the `videos/` directory.
2. Run the script:
   ```bash
   python subtitle_gen_app.py
   ```
3. The script will:
   - Validate the videos.
   - Extract audio and save it in the `audio/` directory.
   - Generate SRT files and save them in the `output/` directory.

## Example Output
After processing, the `output/` directory will contain SRT files like:
```
video1.srt
video2.srt
```

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
