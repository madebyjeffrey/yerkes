import math
import random
from dataclasses import dataclass, field
from random import Random
from typing import List, Optional

from data import MAX_PLANET_POPULATION, Planet, Starmap
from log import get_logger
from news import NewsAccumulator, NewsItem, PopulationChangeNews
from planet_names import iter_planet_names

_logger = get_logger(__name__)

_GAME_NAME_ADJECTIVES = ("quiet", "hidden", "long", "brief", "wild", "golden")
_GAME_NAME_NOUNS = ("walk", "voyage", "drift", "dance", "journey", "flight")
_GAME_NAME_PLACES = ("park", "void", "nebula", "frontier", "expanse", "dark")
_PLACEMENT_ATTEMPTS_PER_PLANET = 250
_MAX_INITIAL_PLANET_POPULATION = 49_999


def generate_game_name(rng: Optional[Random] = None) -> str:
    """Generate a lightweight title in the style of 'A walk in the park'."""
    prng = rng or random.Random()
    adjective = prng.choice(_GAME_NAME_ADJECTIVES)
    noun = prng.choice(_GAME_NAME_NOUNS)
    place = prng.choice(_GAME_NAME_PLACES)
    return f"A {adjective} {noun} in the {place}"


def _distance(a_x: float, a_y: float, b_x: float, b_y: float) -> float:
    return math.hypot(a_x - b_x, a_y - b_y)


def _is_far_enough(existing: List[Planet], x: float, y: float, min_distance: float) -> bool:
    return all(_distance(planet.x, planet.y, x, y) >= min_distance for planet in existing)


def _target_map_size(number_of_planets: int) -> float:
    return max(20.0, (number_of_planets ** 0.5) * 11.0)


def _target_min_distance(number_of_planets: int, map_size: float) -> float:
    if number_of_planets <= 1:
        return 0.0
    return max(2.5, map_size / ((number_of_planets ** 0.5) * 2.6))


STARTING_YEAR = 2500


@dataclass
class Game:
    name: str
    starmap: Starmap
    year: int = STARTING_YEAR
    news: NewsAccumulator = field(default_factory=NewsAccumulator)

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Game name must not be empty.")
        if not isinstance(self.starmap, Starmap):
            raise TypeError("Game starmap must be a Starmap instance.")
        if not isinstance(self.year, int):
            raise TypeError("Game year must be an integer.")
        if not isinstance(self.news, NewsAccumulator):
            raise TypeError("Game news must be a NewsAccumulator instance.")

    def publish_news(self, headline: str, details: str = "") -> None:
        self.news.publish(year=self.year, headline=headline, details=details)
        _logger.info("News published [%d]: %s", self.year, headline)

    def consume_news(self) -> List[NewsItem]:
        return self.news.consume()

    def publish_population_change(
        self,
        *,
        planet_name: str,
        previous_population: int,
        new_population: int,
    ) -> PopulationChangeNews:
        item = self.news.publish_population_change(
            year=self.year,
            planet_name=planet_name,
            previous_population=previous_population,
            new_population=new_population,
        )
        return item

    def _next_population_for_planet(self, planet: Planet) -> int:
        growth = planet.population_growth()
        candidate = planet.population + growth
        return max(0, min(MAX_PLANET_POPULATION, candidate))

    def run_population_phase(self) -> None:
        """Apply population growth/decline and emit news for changes."""
        for planet in self.starmap.planets:
            previous_population = planet.population
            new_population = self._next_population_for_planet(planet)
            if new_population == previous_population:
                continue
            planet.population = new_population
            self.publish_population_change(
                planet_name=planet.name,
                previous_population=previous_population,
                new_population=new_population,
            )

    def advance_turn(self) -> None:
        """Advance one full turn: year progression and population phase."""
        self.advance_year()
        self.run_population_phase()

    def advance_year(self) -> None:
        """Advance the game by one year."""
        self.year += 1
        self.publish_news(headline=f"Year {self.year} begins")
        _logger.info("Year advanced to %d  [game=%s]", self.year, self.name)

    @classmethod
    def generate(
        cls,
        number_of_planets: int,
        game_name: Optional[str] = None,
        *,
        min_distance: Optional[float] = None,
        map_size: Optional[float] = None,
        seed: Optional[int] = None,
    ) -> "Game":
        if not isinstance(number_of_planets, int):
            raise TypeError("number_of_planets must be an integer.")
        if number_of_planets < 1:
            raise ValueError("number_of_planets must be at least 1.")
        if map_size is not None and map_size <= 0:
            raise ValueError("map_size must be greater than 0 when provided.")
        if min_distance is not None and min_distance < 0:
            raise ValueError("min_distance must be at least 0 when provided.")

        prng = random.Random(seed)
        resolved_name = game_name.strip() if game_name else generate_game_name(prng)
        if not resolved_name:
            raise ValueError("game_name must not be empty when provided.")

        resolved_map_size = map_size if map_size is not None else _target_map_size(number_of_planets)
        resolved_min_distance = (
            min_distance
            if min_distance is not None
            else _target_min_distance(number_of_planets, resolved_map_size)
        )

        _logger.info(
            "Generating game '%s': %d planets, map_size=%.1f, min_distance=%.2f",
            resolved_name, number_of_planets, resolved_map_size, resolved_min_distance,
        )

        planets: List[Planet] = []
        planet_names = iter_planet_names()

        for _ in range(number_of_planets):
            placed = False
            for _ in range(_PLACEMENT_ATTEMPTS_PER_PLANET):
                candidate_x = prng.randint(0, int(resolved_map_size))
                candidate_y = prng.randint(0, int(resolved_map_size))
                if _is_far_enough(planets, candidate_x, candidate_y, resolved_min_distance):
                    planets.append(
                        Planet(
                            name=next(planet_names),
                            population=prng.randint(0, _MAX_INITIAL_PLANET_POPULATION),
                            x=candidate_x,
                            y=candidate_y,
                        )
                    )
                    placed = True
                    break

            if not placed:
                _logger.debug("Relaxing min_distance (was %.2f) — map too dense.", resolved_min_distance)
                resolved_min_distance *= 0.92
                planets.append(
                    Planet(
                        name=next(planet_names),
                        population=prng.randint(0, _MAX_INITIAL_PLANET_POPULATION),
                        x=prng.randint(0, int(resolved_map_size)),
                        y=prng.randint(0, int(resolved_map_size)),
                    )
                )

        game = cls(name=resolved_name, starmap=Starmap(maximum_size=number_of_planets, planets=planets), year=STARTING_YEAR)
        _logger.info("Game '%s' ready — %d planets placed.", game.name, len(game.starmap.planets))
        return game
