#!/usr/bin/env python3
import os, sys, time, random, shutil
from colorama import Fore, init

def matrix_rain():
    init()  # Initialize colorama
    chars = '01'  # Binary mode
    width, height = shutil.get_terminal_size()
    columns = [0] * width
    colors = [Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.WHITE]

    try:
        while True:
            line = [' '] * width
            for i in range(width):
                if columns[i] == 0 and random.random() < 0.03:
                    columns[i] = 1
                
                if columns[i] > 0:
                    # Color based on position
                    color = colors[min(2, columns[i] // (height//3))]
                    line[i] = f"{color}{random.choice(chars)}"
                    columns[i] += 1
                    
                    # Random reset with fading
                    if columns[i] > height or random.random() > 0.92:
                        columns[i] = 0
            
            sys.stdout.write(''.join(line) + '\n')
            sys.stdout.flush()
            time.sleep(0.04)
            
    except KeyboardInterrupt:
        os.system('clear')
        print(Fore.GREEN + "The Matrix has you..." + Fore.RESET)
        sys.exit()

if __name__ == '__main__':
    os.system('clear')
    matrix_rain()
