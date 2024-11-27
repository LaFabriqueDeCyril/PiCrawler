import Adafruit_PCA9685

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

# Fonction pour convertir un angle en valeur PWM
def angle_to_pwm(angle):
    pulse_length = 1000000 // 50 // 4096  # 1,000,000 us per second, 50 Hz, 12 bits of resolution
    pulse = angle * 1000 // 180 + 150  # 1000us per 180 degrees, plus offset for 0 degree
    return int(pulse // pulse_length)

# Fonction pour définir l'angle d'un servomoteur
def set_servo_angle(channel, angle):
    pwm_value = angle_to_pwm(angle)
    pwm.set_pwm(channel, 0, pwm_value)

# Fonction pour régler tous les servomoteurs à 90 degrés
def set_all_servos_to_90_degrees():
    for leg, channels in servo_channels.items():
        for channel in channels:
            set_servo_angle(channel, 90)
            print(f"Servomoteur sur canal {channel} réglé à 90 degrés")

# Boucle principale
if __name__ == '__main__':
    try:
        set_all_servos_to_90_degrees()
        print("Tous les servomoteurs ont été réglés à 90 degrés.")
    except KeyboardInterrupt:
        pass  # Rien de spécial à nettoyer avec le PCA9685
