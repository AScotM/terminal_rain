#!/usr/bin/env python3
import os
import sys
import time
import random
import shutil
import argparse
from enum import Enum, auto
from dataclasses import dataclass
from colorama import Fore, init, Style
from typing import List, Dict, Tuple

init(autoreset=True)

class ColumnState(Enum):
    LINK = auto()
    RESOLVING = auto()
    CODE = auto()
    FADING = auto()

@dataclass
class Column:
    position: float
    speed: float
    life: int
    state: ColumnState
    url: str
    bright: bool
    head_char: str = ' '
    tail_chars: List[str] = None
    color: str = Fore.BLUE
    
    def __post_init__(self):
        self.tail_chars = []
        self.update_color()
    
    def advance(self):
        self.position += self.speed
        
        # State transitions
        if self.position > self.life:
            self.reset_column()
        elif self.position > self.life * 0.7 and self.state == ColumnState.CODE:
            self.state = ColumnState.FADING
            self.update_color()
        elif self.position > self.life * 0.3 and self.state == ColumnState.LINK and random.random() > 0.9:
            self.state = ColumnState.RESOLVING
            self.update_color()
        elif self.state == ColumnState.RESOLVING and random.random() > 0.7:
            self.state = ColumnState.CODE
            self.update_color()
        
        # Update characters
        self.head_char = self._get_head_char()
        if random.random() < 0.3:
            self.tail_chars.append(self._get_tail_char())
        if len(self.tail_chars) > 10:
            self.tail_chars.pop(0)
    
    def reset_column(self):
        self.position = random.randint(-height, 0)
        self.state = ColumnState.LINK
        self.url = random.choice([
            f"https://node/{random.randint(0, 65535):04x}",
            f"ftp://data/{random.randint(0, 4294967295):08x}",
            f"wss://stream/{random.choice(['alpha','beta','gamma'])}",
            f"mailto:{random.choice(['agent','sysadmin','root'])}@domain.com",
            f"telnet://{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        ])
        self.bright = random.choice([True, False])
        self.update_color()
        self.tail_chars = []
    
    def update_color(self):
        if self.state == ColumnState.LINK:
            self.color = Fore.LIGHTBLUE_EX if self.bright else Fore.BLUE
        elif self.state == ColumnState.RESOLVING:
            self.color = Fore.LIGHTMAGENTA_EX
        elif self.state == ColumnState.CODE:
            self.color = Fore.GREEN
        else:  # FADING
            self.color = Fore.LIGHTBLACK_EX
    
    def _get_head_char(self) -> str:
        if self.state == ColumnState.LINK:
            char_idx = int(self.position) % len(self.url)
            return self.url[char_idx]
        elif self.state == ColumnState.RESOLVING:
            return random.choice(['�', '✻', '⟁', '⌖', '⍟'])
        return random.choice(chars)
    
    def _get_tail_char(self) -> str:
        return random.choice(chars)

def parse_args():
    parser = argparse.ArgumentParser(description='Hyperlink Matrix Animation')
    parser.add_argument('--speed', type=float, default=1.0,
                      help='Animation speed multiplier (0.1-2.0)')
    parser.add_argument('--no-glitch', action='store_true',
                      help='Disable glitch effects')
    parser.add_argument('--theme', choices=['cyber', 'mono', 'retro'], default='cyber',
                      help='Color theme selection')
    parser.add_argument('--density', type=float, default=1.0,
                      help='Column density (0.1-2.0)')
    return parser.parse_args()

def init_theme(theme: str) -> Dict[str, str]:
    themes = {
        'cyber': {
            'LINK': Fore.BLUE,
            'RESOLVING': Fore.MAGENTA,
            'CODE': Fore.GREEN,
            'FADING': Fore.LIGHTBLACK_EX,
            'background': Fore.CYAN,
            'glitch': Fore.WHITE
        },
        'mono': {
            'LINK': Fore.WHITE,
            'RESOLVING': Fore.WHITE,
            'CODE': Fore.WHITE,
            'FADING': Fore.LIGHTBLACK_EX,
            'background': Fore.WHITE,
            'glitch': Fore.WHITE
        },
        'retro': {
            'LINK': Fore.GREEN,
            'RESOLVING': Fore.YELLOW,
            'CODE': Fore.LIGHTGREEN_EX,
            'FADING': Fore.LIGHTBLACK_EX,
            'background': Fore.GREEN,
            'glitch': Fore.LIGHTRED_EX
        }
    }
    return themes.get(theme, themes['cyber'])

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_terminal_size() -> Tuple[int, int]:
    try:
        return shutil.get_terminal_size()
    except:
        return 80, 24  # Fallback size

def create_columns(width: int, height: int, density: float) -> List[Column]:
    columns = []
    num_columns = int(width * density)
    for _ in range(num_columns):
        columns.append(Column(
            position=random.randint(-height, 0),
            speed=random.uniform(0.2, 0.5) * args.speed,
            life=random.randint(height, height*3),
            state=ColumnState.LINK,
            url=random.choice([
                f"https://node/{random.randint(0, 65535):04x}",
                f"ftp://data/{random.randint(0, 4294967295):08x}",
                f"wss://stream/{random.choice(['alpha','beta','gamma'])}"
            ]),
            bright=random.choice([True, False])
        ))
    return columns

def handle_resize(columns: List[Column], width: int, height: int, density: float) -> List[Column]:
    new_width, new_height = get_terminal_size()
    if new_width != width or new_height != height:
        return create_columns(new_width, new_height, density)
    return columns

def render_frame(columns: List[Column], width: int, height: int):
    frame = []
    for row in range(height):
        line = []
        for col in columns:
            if 0 <= col.position - row < 1:
                line.append(f"{col.color}{col.head_char}{Style.RESET_ALL}")
            elif 0 < col.position - row < height//2 and col.tail_chars:
                tail_idx = min(int(col.position - row) - 1, len(col.tail_chars) - 1)
                if tail_idx >= 0:
                    line.append(f"{theme['background']}{col.tail_chars[tail_idx]}{Style.RESET_ALL}")
                else:
                    line.append(' ')
            else:
                line.append(' ')
        frame.append(''.join(line))
    
    # Add occasional spark
    if random.random() > 0.95:
        x, y = random.randint(0, width-1), random.randint(0, height-1)
        if y < len(frame) and x < len(frame[y]):
            frame[y] = frame[y][:x] + Fore.YELLOW + '✦' + Style.RESET_ALL + frame[y][x+1:]
    
    sys.stdout.write('\n'.join(frame) + '\n')
    sys.stdout.flush()

def glitch_effect(width: int, height: int):
    if args.no_glitch or random.random() > 0.97:
        return
    
    glitch_lines = random.randint(1, 3)
    glitch_chars = ['_', '▒', '▓', '�', '╬', '╩', '╠']
    
    for _ in range(glitch_lines):
        glitch_line = []
        for _ in range(width):
            glitch_line.append(f"{theme['glitch']}{random.choice(glitch_chars)}")
        sys.stdout.write(''.join(glitch_line) + '\n')
    
    time.sleep(0.08)
    sys.stdout.write(f"\033[{glitch_lines}A")

def hyperlink_matrix():
    global height, width, chars, theme, args
    
    clear_screen()
    args = parse_args()
    theme = init_theme(args.theme)
    
    # Characters: Mix of code and URL-friendly symbols
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/:.#?=&-%[]@$€¥₿'
    
    width, height = get_terminal_size()
    columns = create_columns(width, height, args.density)
    
    try:
        while True:
            width, height = get_terminal_size()
            columns = handle_resize(columns, width, height, args.density)
            
            for col in columns:
                col.advance()
            
            render_frame(columns, width, height)
            time.sleep(0.12 / args.speed)
            
            # Move cursor back up
            sys.stdout.write(f"\033[{height}A")
            
            glitch_effect(width, height)
            
    except KeyboardInterrupt:
        clear_screen()
        print(Fore.CYAN + "[Connection terminated]" + Style.RESET_ALL)
        sys.exit(0)

if __name__ == '__main__':
    hyperlink_matrix()
