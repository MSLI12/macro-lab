from django.db import models


class EconomicSeries(models.Model):
    fred_id = models.CharField(
        max_length=64,
        unique=True,
    )

    name = models.CharField(
        max_length=255,
    )

    frequency = models.CharField(
        max_length=32,
        blank=True,
    )

    units = models.CharField(
        max_length=128,
        blank=True,
    )

    source = models.CharField(
        max_length=128,
        default="FRED",
    )

    def __str__(self):
        return f"{self.name} ({self.fred_id})"


class Observation(models.Model):
    series = models.ForeignKey(
        EconomicSeries,
        on_delete=models.CASCADE,
        related_name="observations",
    )

    date = models.DateField()

    value = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["series", "date"],
                name="unique_series_observation",
            )
        ]

        ordering = ["date"]

    def __str__(self):
        return f"{self.series.fred_id} {self.date}: {self.value}"


class Scenario(models.Model):
    name = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name


class ScenarioPoint(models.Model):
    scenario = models.ForeignKey(
        Scenario,
        on_delete=models.CASCADE,
        related_name="points",
    )

    series = models.ForeignKey(
        EconomicSeries,
        on_delete=models.CASCADE,
        related_name="scenario_points",
    )

    date = models.DateField()

    value = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["scenario", "series", "date"],
                name="unique_scenario_series_point",
            )
        ]

        ordering = ["date"]