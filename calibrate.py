import Adafruit_PCA9685
import time

# Initialisation du module PCA9685 pour contrôler les servomoteurs
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)  # 50 Hz pour les servomoteurs

# Configuration des canaux pour les servomoteurs (3 par patte)
servo_channels = {
    'front_left': [0, 1, 2],
    'front_right': [3, 4, 5],
    'back_left': [6, 7, 8],
    'back_right': [9, 10, 11]
}

# Indiquer les servos inversés
inverted_servos = {
    0: True,
    4: True,
    6: True,
    10: True,
    # Ajoutez d'autres servos ici si nécessaire
}

# Fonction pour convertir un angle en valeur PWM
def angle_to_pwm(angle, inverted=False):
    if inverted:
        angle = 180 - angle  # Inverse l'angle si le servo est inversé
    pulse_length = 1000000 // 50 // 4096  # 1,000,000 us per second, 50 Hz, 12 bits of resolution
    pulse = angle * 1000 // 180 + 150  # 1000us per 180 degrees, plus offset for 0 degree
    return int(pulse // pulse_length)

# Fonction pour définir l'angle d'un servomoteur en tenant compte de l'inversion
def set_servo_angle(channel, angle):
    inverted = inverted_servos.get(channel, False)
    pwm_value = angle_to_pwm(angle, inverted)
    pwm.set_pwm(channel, 0, pwm_value)

# Fonction pour déplacer un servomoteur de manière fluide entre deux angles
def smooth_move_servo(channel, start_angle, end_angle, step=2, delay=0.02):
    if start_angle < end_angle:
        angle_range = range(start_angle, end_angle + 1, step)
    else:
        angle_range = range(start_angle, end_angle - 1, -step)

    for angle in angle_range:
        set_servo_angle(channel, angle)
        time.sleep(delay)  # Attendre un court instant entre chaque incrément pour un mouvement fluide

# Fonction pour abaisser tous les servos de manière fluide de 90 à 70 degrés puis revenir à 90 degrés
def lower_and_reset_all_servos_smooth():
    for leg, channels in servo_channels.items():
        for channel in channels:
            # Mouvement fluide vers le bas (de 90 à 70 degrés)
            smooth_move_servo(channel, 90, 60)

            # Mouvement fluide vers le haut (retour à 90 degrés)
            smooth_move_servo(channel, 60, 90)

            print(f"Servomoteur {channel} a effectué son mouvement.")

# Boucle principale
if __name__ == '__main__':
    try:
        lower_and_reset_all_servos_smooth()
        print("Tous les servomoteurs ont été baissés et remis à 90 degrés avec un mouvement fluide.")
    except KeyboardInterrupt:
        pass  # Rien de spécial à nettoyer avec le PCA9685
