import csv
from dataclasses import dataclass
from typing import List
from enum import Enum


class InvalidInputDataError(Exception):
    pass


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
    """Расчет показателей тренировки.

    - get_distance() - расчет дистанции,
    - get_mean_speed() - расчет скорости,
    - get_spent_calories() - расчет каллорий,
    - show_training_info() - показ сообщения тренировки.
    """

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
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
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278  # Training.M_IN_KM / 3600 (секунд в часе)
    CM_IN_M = 100

    def __init__(
        self,
        action,
        duration,
        weight,
        height,
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
    LEN_STEP = 1.38
    CALORIES_WEIGHT_MULTIPLIER = 2
    CALORIES_MEAN_SPEED_SHIFT = 1.1

    def __init__(
        self,
        action,
        duration,
        weight,
        length_pool,
        count_pool,
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


class TrainingTypes(Enum):
    SWM = Swimming
    RUN = Running
    WLK = SportsWalking


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        return TrainingTypes[workout_type].value(*data)
    except (KeyError, TypeError) as err:
        raise InvalidInputDataError(err)


def main(training: Training) -> None:
    print(training.show_training_info().get_message())  # noqa: T201


if __name__ == '__main__':
    with open('packages.csv') as reader:
        packages = csv.reader(reader)
        for package in packages:
            workout, *data = package
            try:
                main(
                    read_package(
                        workout, [float(param) for param in data],
                    ),
                )
            except (ValueError, InvalidInputDataError) as err:
                print(f'Не корректные входные данные {err}')  # noqa: T201
