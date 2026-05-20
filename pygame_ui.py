import sys

try:
    import pygame
except ImportError:
    print("pygame is not installed. Run: python3 -m pip install -e '.[gui]'")
    sys.exit(1)

from game import Game


def _world_bounds(game: Game) -> tuple[int, int, int, int]:
    xs = [planet.x for planet in game.starmap.planets]
    ys = [planet.y for planet in game.starmap.planets]
    if not xs or not ys:
        return 0, 1, 0, 1
    return min(xs), max(xs), min(ys), max(ys)


def _to_screen(
    x: int,
    y: int,
    bounds: tuple[int, int, int, int],
    width: int,
    height: int,
    margin: int,
) -> tuple[int, int]:
    min_x, max_x, min_y, max_y = bounds
    span_x = max(1, max_x - min_x)
    span_y = max(1, max_y - min_y)
    sx = margin + int(((x - min_x) / span_x) * (width - margin * 2))
    sy = margin + int(((y - min_y) / span_y) * (height - margin * 2))
    return sx, sy


def _pick_planet(
    game: Game,
    mouse_pos: tuple[int, int],
    bounds: tuple[int, int, int, int],
    width: int,
    height: int,
    margin: int,
    hit_radius: int = 10,
):
    mx, my = mouse_pos
    best_planet = None
    best_dist2 = (hit_radius + 1) * (hit_radius + 1)
    for planet in game.starmap.planets:
        sx, sy = _to_screen(planet.x, planet.y, bounds, width, height, margin)
        dx = sx - mx
        dy = sy - my
        dist2 = dx * dx + dy * dy
        if dist2 <= hit_radius * hit_radius and dist2 < best_dist2:
            best_planet = planet
            best_dist2 = dist2
    return best_planet

def run() -> None:
    pygame.init()
    width, height = 1000, 700
    margin = 60
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Yerkes")
    font = pygame.font.SysFont("arial", 16)
    clock = pygame.time.Clock()

    game = Game.generate(number_of_planets=30)
    selected_planet = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game.advance_turn()  # same core method as CLI
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                bounds = _world_bounds(game)
                selected_planet = _pick_planet(
                    game,
                    event.pos,
                    bounds,
                    width,
                    height,
                    margin,
                )

        screen.fill((10, 10, 20))
        bounds = _world_bounds(game)

        for planet in game.starmap.planets:
            sx, sy = _to_screen(planet.x, planet.y, bounds, width, height, margin)
            color = (130, 210, 255)
            radius = 6
            if selected_planet is not None and planet.name == selected_planet.name:
                color = (255, 220, 120)
                radius = 8
            pygame.draw.circle(screen, color, (sx, sy), radius)
            label = font.render(planet.name, True, (220, 220, 220))
            screen.blit(label, (sx + 8, sy - 10))

        hud = font.render(
            f"{game.name}   Year {game.year}   Planets {len(game.starmap.planets)}   [SPACE] advance year",
            True,
            (240, 240, 120),
        )
        screen.blit(hud, (20, 20))

        if selected_planet is None:
            selection = font.render("Click a planet to view population", True, (180, 180, 180))
        else:
            selection = font.render(
                (
                    f"Selected: {selected_planet.name}  "
                    f"Population: {selected_planet.population:,}  "
                    f"Location: ({selected_planet.x}, {selected_planet.y})"
                ),
                True,
                (255, 255, 255),
            )
        screen.blit(selection, (20, height - 30))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run()