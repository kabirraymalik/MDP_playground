import pygame
import random
import sys

# Display Parameters
WIDTH, HEIGHT = 1200, 900
GRID_COLS, GRID_ROWS = 4, 3
SIDE_MARGIN = 100
TOP_MARGIN = 100
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 40
TICK_SPEED = 1000 #miliseconds
# colors
BG_COLOR      = (255, 253, 208)
GRID_COLOR    = (0, 0, 128)
BORDER_COLOR  = (0, 0, 128)
TEXT_COLOR    = (0, 0, 128)
DEAD_COLOR    = (50, 50, 50)
BUTTON_COLOR  = (70, 130, 180)
BUTTON_HOVER  = (100, 160, 210)

# MDP Parameters
GRID = [['1', '1', '1', '+'],
        ['1', '0', '1', '-'],
        ['1', '1', '1', '1']]

class GridSquare:
    def __init__(self, rect, text, mode, font):
        self.rect = pygame.Rect(rect)
        self.mode = mode
        self.font = font
        self.text = text
        if(self.mode == '0'):
            self.text = ""
            self.color = DEAD_COLOR
        else:
            self.color = BG_COLOR
        if(self.mode == "+"):
            self.text = "+1"
        if(self.mode == "-"):
            self.text = "-1"
    
    def get_val(self):
        if(self.mode == '1'):
            return self.value
        return 0
    
    def set_val(self, value):
        if(self.mode == '1'):
            self.value = value
            self.text=f"{self.value:.5f}"
    
    def increment_val(self, inc):
        if(self.mode == '1'):
            self.value = self.value + inc
            self.text=f"{self.value:.5f}"
    
    def set_random_val(self):
        if(self.mode == '1'):
            self.value = random.random()
            self.text=f"{self.value:.5f}"
    
    def draw(self, surf):
        # Draw cell background
        pygame.draw.rect(surf, self.color, self.rect)
        # Draw text centered
        txt_surf = self.font.render(self.text, True, TEXT_COLOR)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surf.blit(txt_surf, txt_rect)

class Button:
    def __init__(self, rect, label, callback, font):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.callback = callback
        self.font = font

    def draw(self, surf):
        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(surf, color, self.rect, border_radius=5)
        lbl = self.font.render(self.label, True, TEXT_COLOR)
        surf.blit(lbl, lbl.get_rect(center=self.rect.center))

    def handle_event(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.rect.collidepoint(ev.pos):
                self.callback()

def main():
    # starts pygame object
    pygame.init()
    running = False
    step = 0
    # set fonts
    FONT = pygame.font.SysFont(None, 24)
    TITLE_FONT = pygame.font.SysFont(None, 36)
    # sets display size
    display = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    # compute grid attributes
    grid_x = SIDE_MARGIN
    grid_y = TOP_MARGIN
    grid_w = (WIDTH - 2*SIDE_MARGIN) // GRID_COLS * GRID_COLS
    grid_h = (HEIGHT - TOP_MARGIN - SIDE_MARGIN) // GRID_ROWS * GRID_ROWS
    cell_w = grid_w // GRID_COLS
    cell_h = grid_h // GRID_ROWS
    grid_rect = pygame.Rect(grid_x, grid_y, grid_w, grid_h)
    
    grid = []
    for row in range(GRID_ROWS):
        row_arr = []
        for col in range(GRID_COLS):
            rect = (
                grid_x + col * cell_w,
                grid_y + row * cell_h,
                cell_w, cell_h
            )
            # creates grid square with appropriate characteristics from GRID
            row_arr.append(GridSquare(rect, text=f"[{row} , {col}]", mode=GRID[row][col], font=FONT))
        grid.append(row_arr)
    # create start button 
    def start():
        nonlocal running
        for r in grid:
            for grid_square in r:
                grid_square.set_random_val()
        running = True

    btn_rect = (
        WIDTH - SIDE_MARGIN - BUTTON_WIDTH,
        (TOP_MARGIN - BUTTON_HEIGHT)//2,
        BUTTON_WIDTH, BUTTON_HEIGHT
    )
    start_btn = Button(btn_rect, "start", start, FONT)
    # pre start loop
    while not running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            start_btn.handle_event(ev)

        display.fill(BG_COLOR)

        # draw each square with initialization
        for row_arr in grid:
            for sq in row_arr:
                sq.draw(display)
                
        # draw grid border
        pygame.draw.rect(display, BORDER_COLOR, grid_rect, 10)
        # draw vertical lines
        for i in range(1, GRID_COLS):
            x = grid_x + i * cell_w
            pygame.draw.line(display, GRID_COLOR,
                             (x, grid_y),
                             (x, grid_y + grid_h),
                             5)
        # draw horizontal lines
        for j in range(1, GRID_ROWS):
            y = grid_y + j * cell_h
            pygame.draw.line(display, GRID_COLOR,
                             (grid_x, y),
                             (grid_x + grid_w, y),
                             5)


        start_btn.draw(display)
        pygame.display.flip()
        clock.tick(60)

    def redraw_display(display, step):
        display.fill(BG_COLOR)

        # step counter
        step_surf = FONT.render(f"Step: {step}", True, TEXT_COLOR)
        # centered
        step_rect = step_surf.get_rect(midtop=(display.get_width() // 2, TOP_MARGIN // 2))
        display.blit(step_surf, step_rect)

        for row_arr in grid:
            for sq in row_arr:
                sq.draw(display)

        # draw grid
        pygame.draw.rect(display, BORDER_COLOR, grid_rect, 10)
        for i in range(1, GRID_COLS):
            x = grid_x + i * cell_w
            pygame.draw.line(display, GRID_COLOR,
                             (x, grid_y),
                             (x, grid_y + grid_h),
                             5)
        for j in range(1, GRID_ROWS):
            y = grid_y + j * cell_h
            pygame.draw.line(display, GRID_COLOR,
                             (grid_x, y),
                             (grid_x + grid_w, y),
                             5)
        
    # main loop
    first = 1
    last_update = pygame.time.get_ticks()
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

        if(first == 1):
            redraw_display(display, step)
            first = 0
        
        # update steps
        now = pygame.time.get_ticks()
        if now - last_update >= TICK_SPEED:
            step += 1

            #======================main logic goes here=======================
            for row in grid:
                for sq in row:
                    sq.increment_val(0.0001)
            
            #=================================================================

            last_update = now

        redraw_display(display, step)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()