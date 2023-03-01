from typing import Optional, Generator

from .dataStruct import *

from random import shuffle


class Seat:
    def __init__(self) -> None:
        self.seater: Optional[Person] = Person(name='None')  # TODO

    def __repr__(self) -> str:
        return f'<Seat(seater={self.seater})>'

    def __str__(self) -> str:
        return f'{str(self.seater)}'


class Aisle:
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f'<Aisle()>'

    def __str__(self) -> str:
        return f' '


class SeatingChart:
    def __init__(self, config) -> None:
        """从congfig文件中，初始化座位图

        关键字参数:
        config --
        """
        seat_format = config['seat chart']
        # 初始化座位图
        seat_chart = []
        for i in seat_format.split('\n'):
            seat_chart.append([Aisle() if j == ' ' else Seat() for j in i])
        self.chart: list[list[Seat | Aisle]] = seat_chart
        self.seats: list[list[Seat]] = self.removeAisle()

        # 初始化座位图的行列长度
        self.row_len = len(self.chart[0])
        self.line_len = len(self.chart)
        # ToDo:检测座位图是否合法(必须是矩形)
        pass

        self.stu_list = []
        self._loadStu(config)

    def __repr__(self) -> str:
        return f'<SeatingChart(...)>'

    def __str__(self) -> str:
        lines = []
        for row in self.chart:
            lines.append(
                ''.join(
                    self._nameFormat(i.seater.name) if isinstance(i, Seat) else ' '
                    for i in row
                )
            )
            lines.append('\n')
        return ''.join(lines)

    def __iter__(self):
        return iter(self.chart)

    def __getitem__(self, index):
        return self.chart[index]

    def rawGenerator(self) -> Generator:
        return (i for i in self.chart)

    def lineGenerator(self) -> Generator:
        for i in range(len(self.chart[0])):
            yield [j[i] for j in self.chart]

    def _nameFormat(self, name: str) -> str:
        if len(name) <= 2:
            return f'[ {name} ]'
        else:
            return f'[{name[0:3]}]'

    def _loadStu(self, config) -> None:
        for people in config['people']:
            self.stu_list.append(Person(**people))

    def randomize(self) -> None:
        shuffle(self.stu_list)
        for line in self.seats:
            for seat in line:
                seat.seater = self.stu_list.pop(0)

    def removeAisle(self) -> list[list[Seat]]:
        seats = []
        for line in self.chart:
            for seat in line:
                if isinstance(seat, Aisle):
                    line.remove(seat)
            seats.append(line)
        return seats

    @property
    def row(self) -> list[Seat | Aisle]:
        return list(self.rawGenerator())

    @property
    def line(self) -> list[Seat | Aisle]:
        return list(self.lineGenerator())
