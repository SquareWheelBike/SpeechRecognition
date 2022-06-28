# Import the AudioSegment class for processing audio and the
# split_on_silence function for separating out silent chunks.
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Define a function to normalize a chunk to a target amplitude.

def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)


# Load your audio.
print('loading audio...', end='')
song = AudioSegment.from_wav("./PP001_Dual_0back.wav")
print('done')

# Split track where the silence is 2 seconds or more and get chunks using
# the imported function.
print('processing chunks...')
chunklist = []
for db_change in range(-40, -10, 5):
    chunks = split_on_silence(
        # Use the loaded audio.
        song,
        # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
        min_silence_len=100,
        # Consider a chunk silent if it's quieter than -16 dBFS.
        # (You may want to adjust this parameter.)
        silence_thresh=db_change
    )
    chunklist.append(chunks)
    print(f'{db_change} dB found {len(chunks)} chunks')

# print(f'found {len(chunks)} chunks')
if all(len(chunk) == 0 for chunk in chunklist):
    print('no chunks found')
    exit()

exit()

# Process each chunk with your parameters
for i, chunk in enumerate(chunks):
    # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
    silence_chunk = AudioSegment.silent(duration=500)

    # Add the padding chunk to beginning and end of the entire chunk.
    audio_chunk = silence_chunk + chunk + silence_chunk

    # Normalize the entire chunk.
    normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

    # Export the audio chunk with new bitrate.
    print(f"Exporting chunk{i}.wav.")
    normalized_chunk.export(
        f"./chunk{i}.wav",
        bitrate="192k",
        format="wav"
    )
