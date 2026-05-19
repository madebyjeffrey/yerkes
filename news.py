from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class NewsItem:
    year: int
    headline: str
    details: str = ""

    def __str__(self) -> str:
        if self.details:
            return f"[{self.year}] {self.headline} - {self.details}"
        return f"[{self.year}] {self.headline}"


@dataclass(frozen=True)
class PopulationChangeNews(NewsItem):
    planet_name: str = ""
    previous_population: int = 0
    new_population: int = 0

    @property
    def delta(self) -> int:
        return self.new_population - self.previous_population

    def __str__(self) -> str:
        return (
            f"[{self.year}] {self.headline}: "
            f"{self.previous_population} -> {self.new_population} ({self.delta:+d})"
        )

    @classmethod
    def create(
        cls,
        *,
        year: int,
        planet_name: str,
        previous_population: int,
        new_population: int,
    ) -> "PopulationChangeNews":
        if not planet_name or not planet_name.strip():
            raise ValueError("planet_name must not be empty.")
        if previous_population < 0 or new_population < 0:
            raise ValueError("Population values must be non-negative.")

        delta = new_population - previous_population
        direction = "increased" if delta >= 0 else "decreased"
        clean_planet_name = planet_name.strip()
        headline = f"Population {direction} on {clean_planet_name}"
        details = f"{previous_population} -> {new_population} ({delta:+d})"
        return cls(
            year=year,
            headline=headline,
            details=details,
            planet_name=clean_planet_name,
            previous_population=previous_population,
            new_population=new_population,
        )


@dataclass
class NewsAccumulator:
    items: List[NewsItem] = field(default_factory=list)

    def add(self, item: NewsItem) -> None:
        if not isinstance(item, NewsItem):
            raise TypeError("item must be a NewsItem.")
        self.items.append(item)

    def publish(self, year: int, headline: str, details: str = "") -> None:
        if not headline or not headline.strip():
            raise ValueError("News headline must not be empty.")
        self.items.append(NewsItem(year=year, headline=headline.strip(), details=details.strip()))

    def publish_population_change(
        self,
        *,
        year: int,
        planet_name: str,
        previous_population: int,
        new_population: int,
    ) -> PopulationChangeNews:
        item = PopulationChangeNews.create(
            year=year,
            planet_name=planet_name,
            previous_population=previous_population,
            new_population=new_population,
        )
        self.items.append(item)
        return item

    def peek(self) -> List[NewsItem]:
        return list(self.items)

    def consume(self) -> List[NewsItem]:
        published = list(self.items)
        self.items.clear()
        return published

