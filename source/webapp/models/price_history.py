from django.db import models
from django.utils.html import format_html


class PriceHistory(models.Model):
    part = models.ForeignKey(
        "part.Part", related_name="price_history", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=1000, decimal_places=2)
    date_changed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.part} - {self.price}, {self.date_changed.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name_plural = "Истории цен"
        verbose_name = "История цены"
        db_table = "price_histories"
        ordering = ["-date_changed"]
        app_label = "webapp"

    def to_display(self):
        return format_html(
            '<strong ">{}</strong> - '
            '<span style="color: green; font-weight: bold;">{} ₽</span> '
            '<span style="color: gray;">{}</span>',
            self.part,
            self.price,
            self.date_changed.strftime("%Y-%m-%d %H:%M"),
        )
