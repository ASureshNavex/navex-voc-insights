from account_scoring_agent.domain.models import DriverVerbatim, RankedTheme, ThemeCount

TOP_THEMES = 3


def rank_themes(counts: tuple[ThemeCount, ...]) -> tuple[RankedTheme, ...]:
    """Most negative first, then most mentioned. The theme ID settles ties."""
    ordered = sorted(counts, key=lambda t: (-t.negative_volume, -t.volume, t.theme_id))
    return tuple(
        RankedTheme(t.theme_id, t.name, t.volume, t.negative_volume, rank, is_primary=rank == 1)
        for rank, t in enumerate(ordered, start=1)
    )


def driver_verbatims(
    themes: tuple[RankedTheme, ...], verbatims: tuple[DriverVerbatim, ...], per_theme: int
) -> tuple[DriverVerbatim, ...]:
    """Only the records that drive the analysis: the newest few for each of the top themes."""
    drivers: list[DriverVerbatim] = []
    for theme in themes[:TOP_THEMES]:
        matching = [v for v in verbatims if v.theme_id == theme.theme_id]
        matching.sort(key=lambda v: (v.feedback_date, v.verbatim_id), reverse=True)
        drivers.extend(matching[:per_theme])
    return tuple(drivers)
