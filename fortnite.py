# This is a simple demonstration on how to stream
# audio from microphone and then extract the pitch
# and volume directly with help of PyAudio and Aubio
# Python libraries. The PyAudio is used to interface
# the computer microphone. While the Aubio is used as
# a pitch detection object. There is also NumPy
# as well to convert format between PyAudio into
# the Aubio.
import aubio
import numpy as num
import pyaudio
import sys
import pyautogui
import time

# Some constants for setting the PyAudio and the
# Aubio.
BUFFER_SIZE             = 2048
CHANNELS                = 1
FORMAT                  = pyaudio.paFloat32
METHOD                  = "default"
SAMPLE_RATE             = 44100
HOP_SIZE                = BUFFER_SIZE//2
PERIOD_SIZE_IN_FRAME    = HOP_SIZE



NOTE_NAMES = 'C Db D Eb E F Gb G Ab A Bb B'.split()


notebind = {
    "D4": "W",
    "Bb3": "S",
    "F3": "A",
    "Bb2": "D"
    # "E4": "*MU"
}

def freq_to_number(f): return 69 + 12*num.log2(f/440.0)
def number_to_freq(n): return 440 * 2.0**((n-69)/12.0)
def note_name(n): return NOTE_NAMES[n % 12] + str(int(num.floor(n/12 - 1)))


def key(inp):
    if inp[0] == "*":
        if inp[1] == "M":
            if inp[2] =="U":
                pyautogui.move(0, -30) 
            elif inp[2] =="D":
                pyautogui.move(0, 30) 
            elif inp[2] =="L":
                pyautogui.move(-30, 0) 
            elif inp[2] =="R":
                pyautogui.move(30, 0) 
        elif inp[1] == "C":
            if inp[2] == "L":
                pyautogui.click()
            elif inp[2] == "R":
                pyautogui.click(button="right")
            elif inp[2] == "M":
                pyautogui.click(button="middle")   
        pyautogui.press(inp)


def main(args):

    # Initiating PyAudio object.
    pA = pyaudio.PyAudio()
    # Open the microphone stream.
    mic = pA.open(format=FORMAT, channels=CHANNELS,
        rate=SAMPLE_RATE, input=True,
        frames_per_buffer=PERIOD_SIZE_IN_FRAME)

    # Initiating Aubio's pitch detection object.
    pDetection = aubio.pitch(METHOD, BUFFER_SIZE,
        HOP_SIZE, SAMPLE_RATE)
    # Set unit.
    pDetection.set_unit("Hz")
    # Frequency under -40 dB will considered
    # as a silence.
    pDetection.set_silence(-40)
    last = "none"
    count = 0

    # Infinite loop!
    while True:

        # Always listening to the microphone.
        data = mic.read(PERIOD_SIZE_IN_FRAME,exception_on_overflow = False)
        # Convert into number that Aubio understand.
        samples = num.fromstring(data,
            dtype=aubio.float_type)
        # Finally get the pitch.
        pitch = pDetection(samples)[0]
        # Compute the energy (volume)
        # of the current frame.
        volume = num.sum(samples**2)/len(samples)
        # Format the volume output so it only
        # displays at most six numbers behind 0.
        volume = "{:6f}".format(volume)

        
        
        n = freq_to_number(pitch)
        if n == float("-inf") or n == float("inf"):
            n0 = "NAN"
            name = "none"
        else:
            n0 = round(n)
            name = note_name(n0)

        print(name)
        print(notebind.keys())

        if name in notebind.keys():
            if last == name and count == 1:
                count += 1
                key(notebind[name])
            elif last == name:
                count += 1
            else:
                last = name
                count = 1


        # Finally print the pitch and the volume.
        print(str(pitch) + " " + name + " " + str(volume))




if __name__ == "__main__": main(sys.argv)