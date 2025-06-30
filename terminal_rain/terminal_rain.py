#!/usr/bin/env python3
import os
import sys
import time
import random
import shutil

def get_terminal_size():
    cols, rows = shutil.get_terminal_size()
    return cols, rows

def matrix_rain():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()'
    width, height = get_terminal_size()
    columns = [0] * width

    try:
        while True:
            # Create a blank line
            line = [' '] * width
            for i in range(width):
                if columns[i] == 0 and random.random() < 0.02:
                    columns[i] = 1
                if columns[i] > 0:
                    line[i] = random.choice(chars)
                    columns[i] += 1
                    if columns[i] > height or random.random() > 0.95:
                        columns[i] = 0
            sys.stdout.write(''.join(line) + '\n')
            sys.stdout.flush()
            time.sleep(0.05)
    except KeyboardInterrupt:
        # Clear screen on exit
        os.system('clear')
        sys.exit()

if __name__ == '__main__':
    # Clear terminal and start
    os.system('clear')
    matrix_rain()
