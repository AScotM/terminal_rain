#!/usr/bin/env python3
import os
import sys
import time
import random
import shutil
from colorama import Fore, init

def matrix_rain():
    init(autoreset=True)
    os.system('clear')
    
    # Latin alphanumeric characters with occasional symbols
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*'
    
    width, height = shutil.get_terminal_size()
    columns = [{
        'position': 0,
        'speed': random.uniform(0.3, 0.7),
        'life': random.randint(height//2, height*2),
        'color': random.choice([Fore.GREEN, Fore.LIGHTGREEN_EX])
    } for _ in range(width)]
    
    # Luxurious color palette with velvet red accents
    colors = [
        Fore.LIGHTBLACK_EX,
        Fore.GREEN,
        Fore.LIGHTGREEN_EX,
        Fore.WHITE,
        Fore.LIGHTRED_EX,  # Velvet accent
        Fore.RED,          # Velvet accent
        Fore.LIGHTGREEN_EX,
        Fore.GREEN,
        Fore.LIGHTBLACK_EX
    ]
    
    try:
        while True:
            line = [' '] * width
            
            for i in range(width):
                col = columns[i]
                
                # Randomly revive columns
                if col['position'] <= 0 and random.random() < 0.015:  # Very sparse
                    columns[i] = {
                        'position': 1,
                        'speed': random.uniform(0.2, 0.5),  # Slower speeds
                        'life': random.randint(height, height*3),
                        'color': random.choice([
                            Fore.GREEN, 
                            Fore.LIGHTGREEN_EX,
                            Fore.RED,  # Velvet accent
                            Fore.LIGHTRED_EX  # Velvet accent
                        ])
                    }
                    col = columns[i]
                
                # Active columns
                if col['position'] > 0:
                    # Head character (bright)
                    if random.random() > 0.7:  # Blinking effect
                        head_char = random.choice(chars)
                        line[i] = f"{col['color']}{head_char}"
                    
                    # Trail characters
                    trail_length = min(int(col['position'] * 0.7), height)
                    for j in range(1, trail_length):
                        if (col['position'] - j) > 0:
                            trail_char = random.choice(chars)
                            color_idx = min(j, len(colors)-1)
                            # Occasionally add velvet accents
                            if random.random() > 0.95:
                                line[i] = f"{random.choice([Fore.RED, Fore.LIGHTRED_EX])}{trail_char}"
                            else:
                                line[i] = f"{colors[color_idx]}{trail_char}"
                    
                    col['position'] += col['speed']
                    
                    # End columns
                    if col['position'] > col['life']:
                        col['position'] = 0
            
            # Luxurious slow rendering
            sys.stdout.write(''.join(line) + '\n')
            sys.stdout.flush()
            time.sleep(0.15)  # Very slow animation
            
    except KeyboardInterrupt:
        os.system('clear')
        print(Fore.RED + "The Matrix surrounds you..." + Fore.RESET)
        sys.exit(0)

if __name__ == '__main__':
    matrix_rain()
