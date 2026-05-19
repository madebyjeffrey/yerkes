from dataclasses import dataclass, field
import logging
from typing import List

from log import get_logger

_logger = get_logger(__name__)

MAX_PLANET_POPULATION = 1_000_000


@dataclass
class Planet:
    name: str
    population: int
    x: int
    y: int

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Planet name must not be empty.")
        if not isinstance(self.population, int):
            raise TypeError("Planet population must be an integer.")
        if not 0 <= self.population <= MAX_PLANET_POPULATION:
            raise ValueError(
                f"Planet population must be between 0 and {MAX_PLANET_POPULATION}."
            )
        _logger.debug("Planet created: %s (population=%d, x=%.2f, y=%.2f)",
                      self.name, self.population, self.x, self.y)

    def effective_capacity(self) -> float:
        return MAX_PLANET_POPULATION

    def crowding_factor(self) -> float:
        return 1.0 - (self.population / (4 * self.effective_capacity()))

    def growth_rate(self) -> float:
        return 0.15

    def population_growth(self) -> int:
        growth = int(self.population * self.crowding_factor() * self.growth_rate())
        return growth


@dataclass
class Starmap:
    maximum_size: int
    planets: List[Planet] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.maximum_size, int):
            raise TypeError("Starmap maximum_size must be an integer.")
        if self.maximum_size < 0:
            raise ValueError("Starmap maximum_size must be at least 0.")
        if len(self.planets) > self.maximum_size:
            raise ValueError("Starmap contains more planets than maximum_size allows.")
        if any(not isinstance(planet, Planet) for planet in self.planets):
            raise TypeError("Starmap planets must all be Planet instances.")

    def add_planet(self, planet: Planet) -> None:
        if not isinstance(planet, Planet):
            raise TypeError("Can only add Planet instances to a Starmap.")
        if len(self.planets) >= self.maximum_size:
            raise ValueError("Cannot add planet: starmap is at maximum capacity.")
        self.planets.append(planet)
        _logger.debug("Planet added to starmap: %s (total=%d/%d)",
                      planet.name, len(self.planets), self.maximum_size)
