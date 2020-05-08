import subprocess
import os
import time
import logging
import argparse
from subprocess import PIPE

"""
    Argparse setup
"""

parser = argparse.ArgumentParser(description="Start deepspeech server with ip and port")

parser.add_argument(
    "-ip",
    type=str,
    nargs="?",
    help="ip of the server, default is localhost",
    default="0.0.0.0",
)

parser.add_argument(
    "-port",
    type=int,
    nargs="?",
    help="port of the server, default is 4242",
    default=4242,
)

parser.add_argument(
    "-log",
    type=bool,
    nargs="?",
    help="should the server log the audio files that are generated",
    default=False,
)

args = vars(parser.parse_args())

PORT = args["port"]
ADDRESS = args["ip"]
LOG = args["log"]

print(f"Connecting on {ADDRESS} on {PORT}")

"""
    Starting klein http-server
"""

from klein import Klein
from twisted.internet.defer import succeed
import wave

app = Klein()


@app.route("/transcribe", methods=["POST"])
def transcribe(request):

    fname = f"{str(time.time()).replace('.','-')}.wav"
    cvtfname = "cvt" + fname

    with open(fname, "wb") as fileOutput:
        fileOutput.write(request.content.read())

    """
        Currently, only 16-bit, 16 kHz, mono-channel WAVE audio files are supported in the Python client
    """

    converted = False

    with wave.open(fname, "rb") as wv:
        try:
            print(f"Audiofile status:{wv.getparams()}")
            if not (
                wv.getnchannels() == 1
                and wv.getsampwidth() == 2
                and wv.getframerate() == 16000
            ):
                converted = True
                ret = runFFMPEG(
                    fname,
                    cvtfname,
                    wv.getnchannels() == 1,
                    wv.getsampwidth() == 2,
                    wv.getframerate() == 16000,
                )
                if not ret[0]:
                    print (stderr)
                    print("Conversion failed on FFMPEG")
                    request.setResponseCode(400)
                    return f"Failed to convert to suitable wav:{ret[1]}"
                else:
                    if not LOG:
                        os.remove(fname)
        except:
            # wave could not get decoded right by wave module
            ret = runFFMPEG(fname, cvtfname, True, True, True)
            converted = True
            if not ret[0]:
                print("Conversion failed on FFMPEG")
                request.setResponseCode(400)
                return f"Failed to convert to suitable wav:{ret[1]}"
            else:
                if not LOG:
                    os.remove(fname)

    if converted:
        fname = cvtfname
    # else, stays the same

    deepspeech = runDeepspeech(fname)

    if not LOG:
        os.remove(fname)

    if deepspeech[0]:
        if not LOG:
            print(f"Transcribed request: {deepspeech[1]}")
        request.setHeader("Content-Type", "text/plain")
        return deepspeech[1]
    else:
        print("Conversion failed on Deepspeech")
        request.setResponseCode(400)
        return f"Transcribe failed with process error:{deepspeech[1]}"


def runDeepspeech(audiofile):

    """
        Transcribes waves files to text
    """

    print(f"Running DeepSpeech with: {audiofile}")

    process = subprocess.run(
        [
            "deepspeech",
            "--model",
            "models/output_graph.pbmm",
            "--lm",
            "models/lm.binary",
            "--trie",
            "models/trie",
            "--alphabet",
            "models/alphabet.txt",
            "--audio",
            audiofile,
        ],
        stdout=PIPE, stderr=PIPE
    )

    if process.returncode != 0:
        return (False, process.stderr)
    else:
        return (True, process.stdout)


def runFFMPEG(fname, cvtfname, codec=True, channel=True, bitrate=True):

    """
        Converts audio files to wav files
    """

    print("in ffmpeg")

    args = []

    if codec:
        args += ["-acodec", "pcm_s16le"]
    elif channel:
        args += ["-ac", "1"]
    elif bitrate:
        args += ["-at", "16000"]

    if len(args) == 0:
        return None

    print(f"Running FMPEG with:{args}")

    process = subprocess.run(
        args=["ffmpeg", "-i", fname] + args + [cvtfname], stdout=PIPE, stderr=PIPE
    )

    if process.returncode != 0:
        return (False, process.stderr)
    else:
        return (True, process.stdout)


app.run(ADDRESS, PORT)

