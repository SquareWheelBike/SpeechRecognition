"""
split the source file into chunks of silence and non-silence
"""

# Import the AudioSegment class for processing audio and the
# split_on_silence function for separating out silent chunks.
from pydub import AudioSegment
from pydub.silence import split_on_silence
import multiprocessing as mp
from itertools import product
import os


# Define a function to normalize a chunk to a target amplitude.

def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)


def worker(x, y, song):
    chunks = split_on_silence(
        # Use the loaded audio.
        song,
        # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
        min_silence_len=x,
        # Consider a chunk silent if it's quieter than -16 dBFS.
        # (You may want to adjust this parameter.)
        silence_thresh=y,
        keep_silence=100
    )
    return x, y, chunks


if __name__ == '__main__':
    OUTPUTFOLDER = './chunks'

    # Load your audio.
    print('loading audio...', end='')
    song = AudioSegment.from_wav("./PP001_Dual_0back.wav")
    print('done')

    # delete the old files
    print('preparing output directory...')
    # if chunks not exist, create it
    if not os.path.exists(OUTPUTFOLDER):
        os.makedirs(OUTPUTFOLDER)
    else:
        from reset import delete_subfolders
        delete_subfolders(path=OUTPUTFOLDER)

    # Split track where the silence is 2 seconds or more and get chunks using
    # the imported function.
    print('processing chunks...')
    with open('./results.txt', 'w') as f:
        f.write('ms,dBFS,chunks\n')

    # since we are processing a large number of hyperparameters, we use a pool to parallelize the processing
    ps = []
    pool = mp.Pool(processes=int(mp.cpu_count() * 0.5))
    for x, y in product(range(50, 800, 50), range(-32, -15, 1)):
        p = pool.apply_async(worker, args=(x, y, song))
        ps.append(p)

    # as processes finish, print the results to the console and write them to a file
    # results = []
    for p in ps:
        r = p.get()
        # results.append(r)
        x, y, chunks = r
        print(f'{x} ms, {y} dBFS found {len(chunks)} chunks')
        with open('./results.txt', 'a') as f:
            f.write(f'{r[0]},{r[1]},{len(r[2])}\n')

        # save the chunks to the output directory
        folder = os.path.join(OUTPUTFOLDER, f'{x}_len_{y}_threshold')
        os.makedirs(folder, exist_ok=False)
        for i, chunk in enumerate(chunks):
            path = os.path.join(folder, f"chunk{i}.wav")
            # print(f"Exporting {path}.")

            silence_chunk = AudioSegment.silent(duration=100)

            # Add the padding chunk to beginning and end of the entire chunk.
            audio_chunk = silence_chunk + chunk + silence_chunk

            # Normalize the entire chunk.
            normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

            # Export the audio chunk with new bitrate.
            normalized_chunk.export(
                path,
                bitrate="192k",
                format="wav"
            )