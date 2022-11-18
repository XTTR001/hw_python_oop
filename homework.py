from dataclasses import dataclass
from typing import Final, List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return (
            f'Тип тренировки: {self.training_type};'
            f' Длительность: {self.duration:.3f} ч.;'
            f' Дистанция: {self.distance:.3f} км;'
            f' Ср. скорость: {self.speed:.3f} км/ч;'
            f' Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Класс для расчета:
       дистанции
       средней скорости
       показа сообщений по тренировке"""

    LEN_STEP = 0.65
    M_IN_KM: Final[int] = 1000
    MIN_IN_H: Final[int] = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения """
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    LEN_STEP = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H
        )


class SportsWalking(Training):

    LEN_STEP = 0.65
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC: Final[float] = 0.278
    CM_IN_M: Final[int] = 100

    def __init__(
        self, action: int, duration: float, weight: float, height: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (
                    (self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                    / (self.height / self.CM_IN_M)
                )
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight
            )
            * self.duration
            * self.MIN_IN_H
        )


class Swimming(Training):
    """Перегрузка методов расчета средней скорости """

    LEN_STEP = 1.38
    CALORIES_WEIGHT_MULTIPLIER = 2
    CALORIES_MEAN_SPEED_SHIFT = 1.1

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool = length_pool

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight
            * self.duration
        )

# По идее основная программа должна лежать в одном файле
# а классы в другом. Не знаю как проверяет практикум


PACKAGES = [
    ('SWM', [720, 1, 80, 25, 40]),
    ('RUN', [15000, 1, 75]),
    ('WLK', [9000, 1, 75, 180]),
    ('WLK', [9000, 1, 75, 180, 15, 17]),
    ('KILL', [9000, 1, 75]),
]

TRAININGS = {
    'SWM': [Swimming, 5],
    'RUN': [Running, 3],
    'WLK': [SportsWalking, 4],
}


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    # Проверка на вхождения ключа в словарь ключей
    if workout_type not in TRAININGS:
        raise ValueError(f'Workout type "{workout_type}" not acceptable.')

    # Проверка на консистентность данных пакета
    if len(data) != TRAININGS[workout_type][1]:
        raise ValueError(f'Package: {data} out of range.'
                         f' Size should be {TRAININGS[workout_type][1]}')

    return TRAININGS[workout_type][0](*data)


def main(training: Training) -> None:
    print(training.show_training_info().get_message())  # noqa: T201


if __name__ == '__main__':

    for workout_type, data in PACKAGES:
        try:
            main(read_package(workout_type, data))
        except ValueError as _ex:
            print(_ex)
