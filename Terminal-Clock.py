import datetime
import time
import os
import math

# ANSI color codes
COLOR_PURPLE = "\033[95m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ASCII art digits for time display
ASCII_NUMBERS = {
    '0': [" AAA ",
          "A   A",
          "A   A",
          "A   A",
          " AAA "],
    '1': ["  A  ",
          " AA  ",
          "  A  ",
          "  A  ",
          " AAA "],
    '2': [" AAA ",
          "A   A",
          "  AA ",
          " A   ",
          "AAAAA"],
    '3': [" AAA ",
          "A   A",
          "  AA ",
          "A   A",
          " AAA "],
    '4': ["A   A",
          "A   A",
          "AAAAA",
          "    A",
          "    A"],
    '5': ["AAAAA",
          "A    ",
          "AAAA ",
          "    A",
          "AAAA "],
    '6': [" AAA ",
          "A    ",
          "AAAA ",
          "A   A",
          " AAA "],
    '7': ["AAAAA",
          "    A",
          "   A ",
          "  A  ",
          " A   "],
    '8': [" AAA ",
          "A   A",
          " AAA ",
          "A   A",
          " AAA "],
    '9': [" AAA ",
          "A   A",
          " AAAA",
          "    A",
          " AAA "],
    ':': ["   ",
          " O ",
          "   ",
          " O ",
          "   "]
}

def get_ascii_number(num_str):
    lines = [""] * 5
    for char in num_str:
        if char in ASCII_NUMBERS:
            for i in range(5):
                lines[i] += ASCII_NUMBERS[char][i] + "  " # Add some spacing
    return lines

def draw_clock(hour, minute, second):
    radius = 10  # Increased radius for a bigger clock
    width_multiplier = 1.8 # Multiplier for width
    size_x = int(2 * radius * width_multiplier + 1)  # Grid width
    size_y = 2 * radius + 1 # Grid height
    center_x = int(radius * width_multiplier)
    center_y = radius
    
    grid = [[' ' for _ in range(size_x)] for _ in range(size_y)]

    # Draw clock face (circle)
    for angle_deg in range(0, 360, 1):  # Smaller step for more detail
        angle_rad = math.radians(angle_deg)
        x = int(center_x + radius * math.cos(angle_rad) * width_multiplier)
        y = int(center_y + radius * math.sin(angle_rad))
        if 0 <= x < size_x and 0 <= y < size_y:
            grid[y][x] = COLOR_PURPLE + '#' + COLOR_RESET  # Different symbol for clock face

    # Draw hour marks
    mark_length = 2 # Length of the hour mark
    for h_angle_deg in range(0, 360, 30): # 30 degrees per hour
        h_angle_rad = math.radians(h_angle_deg - 90) # Adjust for 0 at top
        
        # Outer point of the mark
        ox = int(center_x + radius * math.cos(h_angle_rad) * width_multiplier)
        oy = int(center_y + radius * math.sin(h_angle_rad))

        # Inner point of the mark
        ix = int(center_x + (radius - mark_length) * math.cos(h_angle_rad) * width_multiplier)
        iy = int(center_y + (radius - mark_length) * math.sin(h_angle_rad))

        # Draw a line for the mark
        def draw_mark_line(grid, x1, y1, x2, y2, char):
            # Simple line drawing algorithm (Bresenham-like for ASCII)
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1
            err = dx - dy

            while True:
                if 0 <= x1 < size_x and 0 <= y1 < size_y:
                    grid[y1][x1] = char
                if x1 == x2 and y1 == y2:
                    break
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x1 += sx
                if e2 < dx:
                    err += dx
                    y1 += sy

        draw_mark_line(grid, ix, iy, ox, oy, COLOR_PURPLE + '=' + COLOR_RESET) # Use '=' for hour marks

    # Draw center
    grid[center_y][center_x] = COLOR_BLUE + 'X' + COLOR_RESET

    # Hand lengths (adjusted for new radius)
    hour_len = radius * 0.4
    minute_len = radius * 0.7
    second_len = radius * 0.8

    # Calculate angles (in radians, 0 at top, clockwise)
    sec_angle = math.radians((second * 6) - 90)
    min_angle = math.radians((minute * 6 + second * 0.1) - 90)
    hr_angle = math.radians(((hour % 12) * 30 + minute * 0.5) - 90)

    # Draw hands
    def draw_line(grid, cx, cy, length, angle, char):
        for i in range(1, int(length) + 1):
            x = int(cx + i * math.cos(angle) * width_multiplier)
            y = int(cy + i * math.sin(angle))
            if 0 <= x < size_x and 0 <= y < size_y:
                # Only draw if the spot is empty or a clock face dot
                if grid[y][x] == ' ' or grid[y][x] == COLOR_PURPLE + '#' + COLOR_RESET:
                    grid[y][x] = COLOR_BLUE + char + COLOR_RESET

    draw_line(grid, center_x, center_y, second_len, sec_angle, '+')  # Different symbol for second hand
    draw_line(grid, center_x, center_y, minute_len, min_angle, '=')  # Different symbol for minute hand
    draw_line(grid, center_x, center_y, hour_len, hr_angle, '@')  # Different symbol for hour hand
    
    # Get terminal width
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        # Default width if terminal size can't be determined
        terminal_width = 80

    # Calculate padding for the analog clock
    analog_clock_width = size_x
    analog_padding = max(0, (terminal_width - analog_clock_width) // 2)

    # Print the grid with padding
    for row in grid:
        print(" " * analog_padding + "".join(row))
    
    # Print ASCII time
    time_str = f"{hour:02d}:{minute:02d}:{second:02d}"
    ascii_time_lines = get_ascii_number(time_str)
    
    # Calculate padding to center the ASCII art time
    if ascii_time_lines:
        ascii_time_width = len(ascii_time_lines[0])
        # Center the digital clock within the terminal width
        digital_padding = max(0, (terminal_width - ascii_time_width) // 2)
        
        for line in ascii_time_lines:
            print(" " * digital_padding + line)

def main():
    try:
        while True:
            now = datetime.datetime.now()
            h = now.hour
            m = now.minute
            s = now.second
            clear_screen()
            draw_clock(h, m, s)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Clock stopped.")

if __name__ == "__main__":
    main()
