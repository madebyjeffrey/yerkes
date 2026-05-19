from game import Game
from log import configure_logging, get_logger

_logger = get_logger(__name__)


def demo() -> None:
    configure_logging(level="INFO")

    game = Game.generate(number_of_planets=5)

    _logger.info("Game: %s  (Year %d)", game.name, game.year)
    _logger.info("Planets (%d):", len(game.starmap.planets))
    for planet in game.starmap.planets:
        _logger.info("  - %s  population=%d  x=%d  y=%d",
                     planet.name, planet.population, planet.x, planet.y)

    for _ in range(10):
        game.advance_turn()
        _logger.info("After turn, year=%d", game.year)
        for news in game.consume_news():
            _logger.info("NEWS %s", news)


if __name__ == "__main__":
    demo()
