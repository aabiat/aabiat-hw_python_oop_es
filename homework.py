class InfoMessage:
    """Mensaje sobre el entrenamiento."""

    def __init__(self, training_type: str, duration: float, distance: float,
                 speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Tipo de entrenamiento: {self.training_type}; '
                f'Duración: {self.duration:.3f} h; '
                f'Distancia: {self.distance:.3f} km; '
                f'Vel. promedio: {self.speed:.3f} km/h; '
                f'Calorías quemadas: {self.calories:.3f}.')


class Training:
    """Clase de entrenamiento de base."""

    # A continuación las constantes básicas:
    # M_IN_KM aplicable a todas las clases.
    # LEN_STEP no será incluída en la clase base toda vez que
    # cambia en función de la clase Running, SportsWalking
    # o Swimming.

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    # Atendiendo al contenido de "data", los atributos base son:
    # (1) número de pasos o brazadas (action),
    # (2) tiempo de entrenamiento en horas (duration),
    # (3) peso (weight).

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Obtiene la distancia en km."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Obtiene la velocidad media."""
        distance = self.get_distance()
        speed = distance / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Obtiene el número de calorías quemadas."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Devuelve mensaje sobre el entrenamiento completado."""
        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        message = InfoMessage(training_type, duration,
                              distance, speed, calories)
        return message


class Running(Training):
    """Entrenamiento: correr."""

    # Las constantes aplicables al cálculo de la quema de calorias
    # en la clase Running:
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    # Toda vez que Running heredará sólamente las clases de Training,
    # no es necesario inicializar esta clase y podemos brincarnos
    # directamente al método para el cálculo de calorias quemadas.

    def get_spent_calories(self) -> float:
        """Obtiene el número de calorías quemadas al correr."""
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.get_mean_speed()
                    + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM * self.duration
                    * self.MIN_IN_H)
        return calories


class SportsWalking(Training):
    """Entrenamiento: marcha rápida."""

    # Las constantes aplicables al cálculo de la quema de calorias
    # en la clase SportsWalking:

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    # Toda vez que SportsWalking tendrá atributos no disponibles en
    # Training, aquí si vamos a inicializar la clase.

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    # En SportsWalking, el cálculo de las calorias quedaría de la
    # siguiente forma.

    def get_spent_calories(self) -> float:
        """Obtiene el número de calorías quemadas durante el entrenamiento."""
        calories = ((self.CALORIES_WEIGHT_MULTIPLIER
                    * self.weight
                    + ((self.get_mean_speed() * self.KMH_IN_MSEC)**2
                       / (self.height / self.CM_IN_M))
                    * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                    * self.weight)
                    * self.duration * self.MIN_IN_H)
        return calories


class Swimming(Training):
    """Entrenamiento: natación."""

    # El siguiente valor de LEN_STEP es aplicable a la clase Swimming.

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2

    # Toda vez que Swimming tendrá atributos no disponibles en
    # Training, aquí también vamos a inicializar la clase.

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Obtiene la velocidad media."""
        speed = (self.length_pool * self.count_pool / self.M_IN_KM
                 / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Obtiene el número de calorías quemadas."""
        calories = ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                    * self.duration)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Lee los datos de los sensores."""
    if workout_type == 'SWM':
        action, duration, weight, length_pool, count_pool = data
        return Swimming(action, duration, weight, length_pool, count_pool)
    elif workout_type == 'RUN':
        action, duration, weight = data
        return Running(action, duration, weight)
    elif workout_type == 'WLK':
        action, duration, weight, height = data
        return SportsWalking(action, duration, weight, height)
    else:
        raise ValueError(f'Invalid workout type: {workout_type}')


def main(training: Training) -> None:
    """Función principal."""

    # Obtener los valores necesarios para el mensaje
    info = training.show_training_info()

    # Mostrar el mensaje en la consola
    message = info.get_message()
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
