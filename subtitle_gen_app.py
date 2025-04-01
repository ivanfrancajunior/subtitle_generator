#%%
import os
from moviepy import VideoFileClip
import assemblyai as aai

class ValidatePath:
    def __init__(self, video_path):
        """
        Initializes the class with the path to the video(s).
        Args:
            video_path (str): Path to a directory or a single MP4 file.
        """
        self.video_path = video_path
        self.videos = []

    def validate_files(self):
        """
        Validates if the provided path exists and contains valid MP4 files.
        Raises:
            FileNotFoundError: If the path does not exist.
            ValueError: If no MP4 files are found.
        """
        if not os.path.exists(self.video_path):
            raise FileNotFoundError(f"The provided path does not exist: {self.video_path}")

        if os.path.isdir(self.video_path):

            self.videos = [os.path.join(self.video_path, file) for file in os.listdir(self.video_path) if file.endswith(".mp4")]
        elif os.path.isfile(self.video_path):

            if self.video_path.endswith(".mp4"):
                self.videos.append(self.video_path)
            else:
                raise ValueError(f"The provided file is not an MP4: {self.video_path}")
        else:
            raise ValueError("The provided path is neither a directory nor a valid file.")

        if not self.videos:
            raise ValueError("No MP4 files found in the provided path.")

        print(f"{len(self.videos)} video(s) found:")
        for video in self.videos:
            print(f"- {video}")


class AudioExtractor:
    def __init__(self, video_path, output_dir="audio"):
        """
        Initializes the audio extractor with the video path and output directory.
        Args:
            video_path (str): Path to the video file.
            output_dir (str): Directory to save the extracted audio.
        """
        self.video_path = video_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def extract_audio(self):
        """
        Extracts the audio from the video and saves it as a WAV file.
        Returns:
            str: Path to the extracted audio file.
        Raises:
            RuntimeError: If there is an error during audio extraction.
        """
        try:
            video = VideoFileClip(self.video_path)
            audio_filename = os.path.splitext(os.path.basename(self.video_path))[0] + ".wav"
            audio_path = os.path.join(self.output_dir, audio_filename)
            video.audio.write_audiofile(audio_path, codec="pcm_s16le")
            return audio_path
        except Exception as e:
            raise RuntimeError(f"Error extracting audio: {e}")


class TranscriberAssemblyAI:
    def __init__(self, api_key):
        """
        Initializes the transcriber with the AssemblyAI API key.
        Args:
            api_key (str): Your AssemblyAI API key.
        """
        self.api_key = api_key
        aai.settings.api_key = api_key

    def transcribe_and_save_srt(self, audio_url, output_dir="./output"):
        """
        Transcribes the audio and saves the result as an SRT file.
        Args:
            audio_url (str): URL of the audio file (must be publicly accessible).
            output_dir (str): Directory to save the SRT file.
        Returns:
            str: Path to the generated SRT file.
        Raises:
            Exception: If transcription fails or encounters an error.
        """

        os.makedirs(output_dir, exist_ok=True)

        config = aai.TranscriptionConfig(
            language_code="pt"
        )

        transcriber = aai.Transcriber(config=config)
        transcript = transcriber.transcribe(audio_url)

        while transcript.status != "completed":
            if transcript.status == "error":
                raise Exception(f"Transcription error: {transcript.error}")
            transcript = transcriber.get_transcript(transcript.id)

        # Export SRT
        srt_content = transcript.export_subtitles_srt()
        audio_filename = os.path.splitext(os.path.basename(audio_url))[0]
        srt_path = os.path.join(output_dir, f"{audio_filename}.srt")
        with open(srt_path, "w", encoding="utf-8") as srt_file:
            srt_file.write(srt_content)

        return srt_path

# %%
if __name__ == "__main__":

    # Configuration
    api_key = "your api kei "

    video_path = "./videos"  # Path to a directory or a single MP4 file

    audio_output_dir = "./audio"  # Directory for extracted audio files

    srt_output_dir = "output"  # Directory for generated SRT files

    # Validate video files
    validator = ValidatePath(video_path)

    validator.validate_files()

    # Process each video
    for video in validator.videos:
        try:
            print(f"Processing video: {video}")

            # Extract audio
            audio_extractor = AudioExtractor(video, output_dir=audio_output_dir)
            audio_path = audio_extractor.extract_audio()

            # Transcribe audio and generate SRT
            transcriber = TranscriberAssemblyAI(api_key)
            srt_path = transcriber.transcribe_and_save_srt(audio_path, output_dir=srt_output_dir)

            print(f"SRT file saved at: {srt_path}")

        except Exception as e:
            print(f"Error processing video {video}: {e}")
# %%
