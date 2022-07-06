"""
pass each of the split files through google's speech API and get the transcription, stored in a csv file
"""

import os
from os import path
import sys
import speech_recognition as sr
import csv
import pydub
import multiprocessing as mp

# iterate through subfolders in `./chunks` folder
SRCFOLDER = './chunks'
DSTCSV = './transcriptions.csv'
with open(DSTCSV, 'w') as f:
    f.write('file,transcription\n')

# send long file to google's speech API and return the result


def worker(subfolder):
    print("Processing subfolder: " + subfolder)
    # iterate through files in subfolder
    AUDIO_FILE = path.join(SRCFOLDER, f'{subfolder}.wav')
    if not os.path.exists(AUDIO_FILE):
        print(f'{AUDIO_FILE} does not exist, generating...')
        files = [path.join(SRCFOLDER, subfolder, file)
                 for file in os.listdir(path.join(SRCFOLDER, subfolder))]
        audiosnippets = [pydub.AudioSegment.from_wav(file) for file in files]
        # join all audiosnippets into one long audio snippet
        long_audio = pydub.AudioSegment.silent(duration=0)
        for snippet in audiosnippets:
            long_audio += snippet
        # convert to wav
        long_audio.export(AUDIO_FILE, format='wav')

    # use the audio file as the audio source
    print("Reading: " + AUDIO_FILE)
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

    try:
        text = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said: " + text)
    except sr.UnknownValueError:
        text = None
    except sr.RequestError as e:
        text = None

    # os.remove(AUDIO_FILE)
    return text


if __name__ == '__main__':
    ps = []  # pool of processes
    pool = mp.Pool(processes=mp.cpu_count())
    AUDIO_FILES = []  # list of all audio files for deletion later
    for subfolder in os.listdir(SRCFOLDER):
        # send long audio to google's speech API and return the result
        # skip if subfolder is not a folder
        if not os.path.isdir(path.join(SRCFOLDER, subfolder)):
            continue
        p = pool.apply_async(worker, args=(subfolder,))
        ps.append(p)
        AUDIO_FILES.append(subfolder)

    print('done creating worker pool')

    for p, audio in zip(ps, AUDIO_FILES):
        print("waiting for audio: " + audio)
        text = p.get()
        if text is None:
            print(f'{audio} failed to transcribe')
            continue
        # write to csv
        with open(DSTCSV, 'a') as f:
            f.write(f'{audio},{text}\n')
