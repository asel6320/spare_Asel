from datetime import datetime

import factory

from webapp.facroty import PartFactory
from webapp.models import PriceHistory

MIN_DECIMAL = 1
MAX_DECIMAL = 100


class PriceHistoryFactory:
    part = factory.SubFactory(PartFactory)
    price = factory.fuzzy.FuzzyDecimal(MIN_DECIMAL, MAX_DECIMAL)
    date_changed = factory.LazyFunction(datetime.now)

    class Meta:
        model = PriceHistory
