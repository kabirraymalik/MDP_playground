import pygame
import random
import sys

# Display Parameters
WIDTH, HEIGHT = 1200, 900
SIDE_MARGIN = 100
TOP_MARGIN = 100
BUTTON_WIDTH, BUTTON_HEIGHT = 120, 50
TICK_SPEED = 100   # milliseconds

# colors
BG_COLOR      = (18, 104, 36)
TEXTBOX_BG    = (240, 240, 240)
BORDER_COLOR  = (255, 255, 255)
TEXT_COLOR    = (0, 0, 0)
BUTTON_COLOR  = (70, 130, 180)
BUTTON_HOVER  = (100, 160, 210)

class State:
    def __init__(self, player_total, player_ace, dealer_card, dealer_ace):
        self.player_total = player_total
        self.player_ace = player_ace
        self.dealer_card = dealer_card
        self.dealer_ace = dealer_ace
    def to_str(self):
        return f"{self.player_total}_{self.player_ace}_{self.dealer_card}"
    
class Policy:
    def __init__(self):
        self.movelist = {}

class TextBox:
    def __init__(self, rect, label, font, initial=""):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.font = font
        self.value = str(initial)

    def set_value(self, new_val):
        self.value = str(new_val)

    def draw(self, surf):
        # box background & border
        pygame.draw.rect(surf, TEXTBOX_BG, self.rect, border_radius=6)
        pygame.draw.rect(surf, BORDER_COLOR, self.rect, 2, border_radius=6)

        # label (above)
        lbl_surf = self.font.render(self.label, True, BORDER_COLOR)
        lbl_rect = lbl_surf.get_rect(midbottom=(self.rect.centerx, self.rect.top - 4))
        surf.blit(lbl_surf, lbl_rect)

        # value (centered)
        val_surf = self.font.render(self.value, True, TEXT_COLOR)
        val_rect = val_surf.get_rect(center=self.rect.center)
        surf.blit(val_surf, val_rect)

class Button:
    def __init__(self, rect, label, callback, font):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.callback = callback
        self.font = font

    def draw(self, surf):
        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(surf, color, self.rect, border_radius=6)
        lbl = self.font.render(self.label, True, (255,255,255))
        surf.blit(lbl, lbl.get_rect(center=self.rect.center))

    def handle_event(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.rect.collidepoint(ev.pos):
                self.callback()

def main():
    # setup
    pygame.init()
    pygame.display.set_caption("Monte Carlo Blackjack Simulator")
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    clock   = pygame.time.Clock()
    FONT  = pygame.font.SysFont(None, 36)
    SMALL = pygame.font.SysFont(None, 24)

    # build graphics
    box_w, box_h = 180, 70
    h_spacing = 40
    v_top = TOP_MARGIN + 60

    dealer_total_box = TextBox((SIDE_MARGIN, v_top, box_w, box_h), "Dealer total", FONT, "-")
    dealer_ace_box = TextBox((SIDE_MARGIN + box_w + h_spacing, v_top, box_w, box_h), "Dealer ace", FONT, "-")
    player_total_box = TextBox((WIDTH - SIDE_MARGIN - 2*box_w - h_spacing, v_top, box_w, box_h), "Player total", FONT, "-")
    player_ace_box = TextBox((WIDTH - SIDE_MARGIN - box_w, v_top, box_w, box_h), "Player ace", FONT, "-")
    iter_box = TextBox(((WIDTH - box_w)//2, v_top + box_h + 80, box_w, box_h), "Simulation #", FONT, 0)
    text_boxes = [dealer_total_box, dealer_ace_box, player_total_box, player_ace_box, iter_box]

    #start button
    sim_running = False
    iteration = 0

    def start_sim():
        nonlocal sim_running, iteration
        # reset counters
        iteration = 0
        for tb in text_boxes:
            tb.set_value("-")
        iter_box.set_value(0)
        sim_running = True

    start_btn = Button(
        ((WIDTH - BUTTON_WIDTH)//2,
         TOP_MARGIN - BUTTON_HEIGHT - 10,
         BUTTON_WIDTH, BUTTON_HEIGHT),
        "START", start_sim, SMALL
    )

    # draw a frame
    def redraw():
        display.fill(BG_COLOR)

        # title
        title = FONT.render("Monte Carlo Blackjack Simulation", True, BORDER_COLOR)
        display.blit(title, title.get_rect(midtop=(WIDTH//2, 20)))

        # draw widgets
        for tb in text_boxes:
            tb.draw(display)

        start_btn.draw(display)
        pygame.display.flip()

    # wait for start button press
    while not sim_running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            start_btn.handle_event(ev)
        redraw()
        clock.tick(60)

    # main loop
    last_update = pygame.time.get_ticks()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); 
                sys.exit()

        # update simulation at a fixed tick speed
        now = pygame.time.get_ticks()
        if now - last_update >= TICK_SPEED:
            iteration += 1

            # --- placeholder Monte Carlo step ------------
            # Replace this with real sampling and policy updates
            dealer_total        = random.randint(17, 26)  # some busts
            dealer_has_ace      = random.choice([True, False])

            player_total        = random.randint(4, 23)
            player_has_ace      = random.choice([True, False])
            # ----------------------------------------------

            # update UI
            dealer_total_box.set_value(dealer_total)
            dealer_ace_box.set_value("1" if dealer_has_ace else "0")
            player_total_box.set_value(player_total)
            player_ace_box.set_value("1" if player_has_ace else "0")
            iter_box.set_value(iteration)

            last_update = now

        redraw()
        clock.tick(60)

if __name__ == "__main__":
    main()
