# Speech Recognition

At the request of Dr. Bala, the Python [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) project is adapted to recognize speech of the numbers 1-9.

## Resources

- [SpeechRecognition PyPi reference](https://pypi.org/project/SpeechRecognition/)
- [Source Code](https://github.com/Uberi/speech_recognition)
- [Transcribe an Audio File Example](https://github.com/Uberi/speech_recognition/blob/master/examples/audio_transcribe.py) (in local repository under [example/audio_transcribe.py](example/audio_transcribe.py))

## Requirements

requirements.txt has all pip requirements. If you are using pocketsphinx, make sure you install swig on your operating system, BEFORE trying to `pip install` the package.

## Dev Notes

- pocketsphinx is a pain to install and is terrible at recognizing speech
- google cloud speech does an alright job
- google speech recognition uses a private API key to connect to google

I am going to need to come up with a way to split each number spoken into its own audio file or `AudioData` object. Right now jumbling numbers into each other in one file is confusing to the reader.

Alternatively, we could just train our own Tensor AI to only recognise the numbers 1-9, but this will require a lot of training data that we will need to make ourselves.
