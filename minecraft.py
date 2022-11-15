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
import pydirectinput
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
    "D4": "W,h",  #1st postiton. high 
    "Bb3": "S,h", #1st postiton. med high 
    "F3": "A,h",  #1st postiton. med low 
    "Bb2": "D,h", #1st postiton. low 
    "C4": "*MU",  #3rd postiton. high
    "Ab3": "*MD", #3rd postiton. med high
    "Eb3": "*ML", #3rd postiton. med low
    "Ab2": "*MR", #3rd postiton. low 
    "F4": "*CL",  #1st position. Higher
    "Eb4": "*CR", #3rd position. Higher
    "D3": "*DM",  #4th position. med low
    "A3": "*SU",  #2nd Position. med high 
    "E3": "*SD",  #2nd Position. med low
}

def freq_to_number(f): return 69 + 12*num.log2(f/440.0)
def number_to_freq(n): return 440 * 2.0**((n-69)/12.0)
def note_name(n): return NOTE_NAMES[n % 12] + str(int(num.floor(n/12 - 1)))


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
    lastMode = "none"
    lookS = 10
    lookSH = 50
    lookSL = 10

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

        # print(name)
        # print(str(pitch) + " " + name + " " + str(volume))
        
        

        if name in notebind.keys(): 
            inp = notebind[name]
            print(inp)
            if last == name:
                count += 1
            else:
                if lastMode == "h":
                    pyautogui.keyUp(holding)
                    print("up")
                last = name
                count = 1
            if inp[0] == "*":
                if inp[1] == "M" and count >= 4:
                    count = 1
                    if inp[2] =="U":
                        pyautogui.move(0, -lookS)
                    elif inp[2] =="D":
                        pyautogui.move(0, lookS) 
                    elif inp[2] =="L":
                        pyautogui.move(-lookS, 0) 
                    elif inp[2] =="R":
                        pyautogui.move(lookS, 0) 
                elif inp[1] == "C" and count == 2:
                    if inp[2] == "L":
                        pyautogui.click()
                    elif inp[2] == "R":
                        pyautogui.click(button="right")
                    elif inp[2] == "M":
                        pyautogui.click(button="middle")
                elif inp[1] == "S" and count == 4:
                    count = 1
                    if inp[2] == "U":
                        print("scroll up")
                        pyautogui.scroll(50)
                    elif inp[2] == "D":
                        pyautogui.scroll(-50)
                        print("scroll down")
                elif inp[1] == "D" and count == 2:
                    if inp[2] == "M":
                        if lookS == lookSH:
                            lookS = lookSL
                        else: lookS = lookSH 
                        print("LOOK SPEED SWAPPED TO: "+ str(lookS))

            elif count == 3:
                print(inp.split(","))
                key,mode = inp.split(",")
                if mode == "h":
                    lastMode = "h"
                    holding = key
                    pyautogui.keyDown(key)
                    print("down")
                if mode == "t":
                    lastMode = "t"
                    pyaudio.press(key)
        elif lastMode == "h":
            pyautogui.keyUp(holding)
            lastMode = "noneD"
            print("up")

        



        # Finally print the pitch and the volume.




if __name__ == "__main__": main(sys.argv)