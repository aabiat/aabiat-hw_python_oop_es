# Comentarios para el revisor de código:
# Aaron, muchas gracias por sus observaciones. Fueron
# de mucha utilidad para mi. Estoy atendiendo todas ellas.
# Un gusto.

# Algunos comentarios:
# 1) El pytest no me deja pasar si cambio de nombre
#    duration a duration_hrs, de distance a distance_km,
#    se speed a speed_hmh, de weight a weight_km

from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Mensaje sobre el entrenamiento."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = (
        'Tipo de entrenamiento: {training_type}; '
        'Duración: {duration:.3f} h; '
        'Distancia: {distance:.3f} km; '
        'Vel. promedio: {speed:.3f} km/h; '
        'Calorías quemadas: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Clase de entrenamiento de base."""

    # A continuación las constantes básicas:
    #
    # - LEN_STEP: float = 0.65 se aplicará a las clases
    #   hijo Running y SportsWalking pero, será sobreecrita en
    #   la clase Swimming
    #
    # - Por su parte, M_IN_KM y MIN_IN_H aplicables a cualquier
    #   clase hijo

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
        training_type = type(self).__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        message = InfoMessage(training_type, duration,
                              distance, speed, calories)
        return message


class Running(Training):
    """Entrenamiento: correr."""

    # Las constantes adicionales aplicables al cálculo de la quema
    # de calorias en la clase Running son:
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    # Toda vez que Running heredará de la clase de Training todos
    # los atributos, no es necesario inicializar esta clase y
    # podemos brincarnos directamente al método para el cálculo
    # de calorias quemadas.

    def get_spent_calories(self) -> float:
        """Obtiene el número de calorías quemadas al correr."""

        # Respecto de su comentario de separar en secciones
        # el cálculo de calorías, originalmente lo tenía
        # separado para hacerlo más legible pero,
        # al separar el cálculo de calories en bloques cambia,
        # de manera infinitecimal, el valor de calories y,
        # no puedo pasar el pytest para entregarle mi proyecto.
        # Esto es, me parece que la prueba esta programada
        # para que todo se calcule en el return
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.get_mean_speed()
                    + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM * self.duration
                    * self.MIN_IN_H)
        return calories


class SportsWalking(Training):
    """Entrenamiento: marcha rápida."""

    # Las constantes adicionales aplicables al cálculo de la quema
    # de claorias en la clase SportsWalking:

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    # Toda vez que SportsWalking tendrá a height como atributo no
    # disponible en Training, aquí vamos a agregar el atributo
    # height al constructor de inicialización.

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    # En SportsWalking, el cálculo de las calorias quedaría de la
    # siguiente forma.

    def get_spent_calories(self) -> float:
        """Obtiene el número de calorías quemadas durante el entrenamiento."""
        # Con relación a su comentario, aquí también, si no se calcula
        # calories en un sólo paso, entonces no puedo superar el pytest.
        # No me queda más que dejarlo así para poder someter mi
        # tarea a revisión pero, entiendo la importancia del comentario
        # que me formula.
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
    # Asimismo, aquí hay que definir otras dos nuevas constantes

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2

    # Toda vez que Swimming tendrá atributos no disponibles en
    # Training, aquí vamos a agregar los atributos length_pool
    # y count_pool al constructor de inicialización.

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
    # Comentario para Revisor de Código:
    # Muchas gracias por enseñarme el uso de diccionarios
    # con clases en los valores.
    exercise_dict = {
        'SWM': lambda data: Swimming(*data),
        'RUN': lambda data: Running(*data),
        'WLK': lambda data: SportsWalking(*data)
    }
    if workout_type in exercise_dict:
        return exercise_dict[workout_type](data)
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
