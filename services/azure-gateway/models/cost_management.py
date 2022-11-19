from datetime import datetime
from dateutil.parser import parse
from typing import List

from framework.validators.nulls import not_none


class CostManagementQuery:
    def __init__(self, granularity, _type, timeframe_type):
        self.granularity = granularity
        self._type = _type
        self.timeframe_type = timeframe_type

    def get_query(self):
        query = {
            'type': self._type,
            'dataSet': self.get_query_dataset(),
            'timeframe': self.timeframe_type,
            'timePeriod': self.get_query_time_period()
        }

        if self.timeframe_type == 'Custom':
            query = query | {
                'timePeriod': self.get_query_time_period()
            }

        return query

    def get_query_dataset(self):
        return {
            'granularity': self.granularity,
            'aggregation': self.get_query_aggregation(),
            'sorting': self.get_query_sorting(),
            'grouping': self.get_query_grouping()
        }

    def get_query_aggregation(self) -> dict:
        _total_cost = {
            'name': 'Cost',
            'function': 'Sum'
        }

        _total_cost_usd = {
            'name': 'CostUSD',
            'function': 'Sum'
        }

        return {
            'totalCost': _total_cost,
            'totalCostUSD': _total_cost_usd
        }

    def get_query_grouping(self) -> List[dict]:
        return []

    def get_query_sorting(self) -> List[dict]:
        return []

    def get_query_time_period(self) -> dict:
        return {
            'from': self.format_datetime(self.start_date),
            'to': self.format_datetime(self.end_date)
        }

    def format_datetime(self, datetime: datetime):
        return datetime.strftime('%Y-%m-%dT%H:%M:%S+00:00')


class CostByProductQuery(CostManagementQuery):
    def __init__(
            self,
            start_date: str,
            end_date: str):
        self.start_date = start_date
        self.end_date = end_date

        super().__init__(
            granularity='Daily',
            _type='ActualCost',
            timeframe_type='Custom')

    def get_query(self):
        return {
            'type': 'ActualCost',
            'dataSet': self.get_query_dataset(),
            'timeframe': 'Custom',
            'timePeriod': self.get_query_time_period()
        }

    def get_query_grouping(self) -> List[dict]:
        _grouping = {
            'type': 'Dimension',
            'name': 'Product'
        }

        return [_grouping]

    def get_query_sorting(self) -> List[dict]:
        _sorting = {
            'direction': 'ascending',
            'name': 'UsageDate'
        }

        return [_sorting]


class CostManagementRequest:
    def __init__(self, _request):
        self._start_date = _request.args.get('start_date')
        self._end_date = _request.args.get('end_date')

        not_none(self._start_date, 'start_date')
        not_none(self._end_date, 'end_date')

    @property
    def start_date(self):
        return parse(self._start_date)

    @property
    def end_date(self):
        return parse(self._end_date)

    def to_dict(self):
        return self.__dict__.copy()


class CostManagementData:
    def __init__(self, data):
        self._properties = data.get('properties')
        self._property_columns = self._properties.get('columns')
        self._property_rows = self._properties.get('rows')

    def _get_columns(self) -> List[str]:
        return [
            col.get('name') for col
            in self._property_columns
        ]

    def get_dict(self):
        _columns = self._get_columns()
        _rows = []

        for row in self._property_rows:
            entity = dict()
            for index in range(len(_columns)):

                if _columns[index] == 'UsageDate':
                    _usage_date = parse(str(row[index]))
                    entity[_columns[index]] = _usage_date.isoformat()
                else:
                    entity[_columns[index]] = row[index]

            _rows.append(entity)

        return _rows
