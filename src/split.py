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
from itertools import product
with open('./results.txt', 'w') as f:
    pass
for x,y in product(range(50, 800, 50), range(-32, -15, 1)):
    chunks = split_on_silence(
        # Use the loaded audio.
        song,
        # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
        min_silence_len=x,
        # Consider a chunk silent if it's quieter than -16 dBFS.
        # (You may want to adjust this parameter.)
        silence_thresh=y
    )
    # if len(chunklist) > 0 and abs(len(chunklist[-1]) - 98 < abs(len(chunks) - 98)):
    #     print('getting further from target, not bothering to continue')
    #     break
    # chunklist.append(chunks)
    res = f'{x} ms, {y} dBFS found {len(chunks)} chunks'
    print(res)
    with open('./results.txt', 'a') as f:
        f.write(res + '\n')

exit() # stop here for now, we are just looking for the length of the chunks

# print(f'found {len(chunks)} chunks')
if all(len(chunk) == 0 for chunk in chunklist):
    print('no chunks found')
    exit()

# use the chunk closest to 98 separations
# print('using closest chunk...')
chunks = chunklist[0]
for i, c in enumerate(chunklist):
    if abs(98 - len(c)) < abs(98 - len(chunks)):
        chunks = c

print(f'using {len(chunks)} chunks')

# delete all files in './chunks'
print('deleting existing chunks...')
import os
for file in os.listdir('./chunks'):
    os.remove('./chunks/' + file)

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
        f"./chunks/chunk{i}.wav",
        bitrate="192k",
        format="wav"
    )
