#!/usr/bin/env python3
import os
import sys
import time
import random
import shutil
from colorama import Fore, init, Style

def hyperlink_matrix():
    init(autoreset=True)
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Characters: Mix of code and URL-friendly symbols
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/:.#?=&-%[]@'
    
    try:
        width, height = shutil.get_terminal_size()
    except:
        width, height = 80, 24  # Fallback size
    
    columns = []
    for _ in range(width):
        columns.append({
            'position': random.randint(-height, 0),  # Stagger start positions
            'speed': random.uniform(0.2, 0.5),
            'life': random.randint(height, height*3),
            'state': 'LINK',  # LINK, RESOLVING, CODE, FADING
            'url': random.choice([
                f"https://node/{random.randint(0, 65535):04x}",
                f"ftp://data/{random.randint(0, 4294967295):08x}",
                f"wss://stream/{random.choice(['alpha','beta','gamma'])}"
            ]),
            'bright': random.choice([True, False])
        })
    
    # Cyber color palette
    colors = {
        'LINK': Fore.BLUE,
        'RESOLVING': Fore.MAGENTA,
        'CODE': Fore.GREEN,
        'FADING': Fore.LIGHTBLACK_EX
    }
    
    try:
        while True:
            try:
                width, height = shutil.get_terminal_size()
                if len(columns) != width:
                    columns = []
                    for _ in range(width):
                        columns.append({
                            'position': random.randint(-height, 0),
                            'speed': random.uniform(0.2, 0.5),
                            'life': random.randint(height, height*3),
                            'state': 'LINK',
                            'url': random.choice([
                                f"https://node/{random.randint(0, 65535):04x}",
                                f"wss://feed/{random.choice(['main','backup'])}"
                            ]),
                            'bright': random.choice([True, False])
                        })
            except:
                pass
            
            for row in range(height):
                line = []
                for i in range(width):
                    col = columns[i]
                    col['position'] += col['speed']
                    
                    # State transitions
                    if col['position'] > col['life']:
                        col['position'] = random.randint(-height, 0)
                        col['state'] = 'LINK'
                        col['url'] = random.choice([
                            f"https://node/{random.randint(0, 65535):04x}",
                            f"wss://feed/{random.choice(['main','backup'])}"
                        ])
                    elif col['position'] > col['life'] * 0.7 and col['state'] == 'CODE':
                        col['state'] = 'FADING'
                    elif col['position'] > col['life'] * 0.3 and col['state'] == 'LINK' and random.random() > 0.9:
                        col['state'] = 'RESOLVING'
                    elif col['state'] == 'RESOLVING' and random.random() > 0.7:
                        col['state'] = 'CODE'
                    
                    # Determine character
                    if 0 <= col['position'] - row < 1:
                        if col['state'] == 'LINK':
                            char_idx = int(col['position']) % len(col['url'])
                            char = col['url'][char_idx]
                            color = Fore.LIGHTBLUE_EX if col['bright'] else Fore.BLUE
                        elif col['state'] == 'RESOLVING':
                            char = random.choice(['�', '✻', '⟁'])
                            color = Fore.LIGHTMAGENTA_EX
                        else:
                            char = random.choice(chars)
                            color = colors[col['state']]
                        line.append(f"{color}{char}{Style.RESET_ALL}")
                    elif 0 < col['position'] - row < height//2:
                        line.append(f"{Fore.CYAN}{random.choice(chars)}{Style.RESET_ALL}")
                    else:
                        line.append(' ')
                
                sys.stdout.write(''.join(line) + '\n')
            
            sys.stdout.flush()
            time.sleep(0.12)
            
            # Move cursor back up
            sys.stdout.write(f"\033[{height}A")
            
            # Occasional glitch effect
            if random.random() > 0.97:
                glitch_lines = random.randint(1, 3)
                for _ in range(glitch_lines):
                    glitch_line = []
                    for _ in range(width):
                        glitch_line.append(f"{Fore.WHITE}{random.choice(['_', '▒', '▓', '�'])}")
                    sys.stdout.write(''.join(glitch_line) + '\n')
                time.sleep(0.08)
                sys.stdout.write(f"\033[{glitch_lines}A")
                
    except KeyboardInterrupt:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(Fore.CYAN + "[Connection terminated]" + Style.RESET_ALL)
        sys.exit(0)

if __name__ == '__main__':
    hyperlink_matrix()
