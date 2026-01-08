import random


def calcular_xp_requerida(nivel):
    return 50 + (nivel - 1) * 25


class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.nivel = 1
        self.xp = 0
        self.xp_requerida = calcular_xp_requerida(self.nivel)
        self.hp_max = 30
        self.hp = self.hp_max
        self.ataque = 6
        self.defensa = 2

    def esta_vivo(self):
        return self.hp > 0

    def ganar_xp(self, cantidad):
        self.xp += cantidad
        while self.xp >= self.xp_requerida:
            self.xp -= self.xp_requerida
            self.subir_nivel()

    def subir_nivel(self):
        self.nivel += 1
        self.xp_requerida = calcular_xp_requerida(self.nivel)
        self.hp_max += 8
        self.hp = self.hp_max
        self.ataque += 2
        self.defensa += 1
        print(
            f"\n¡{self.nombre} sube a nivel {self.nivel}! "
            f"HP {self.hp_max}, ATQ {self.ataque}, DEF {self.defensa}."
        )


class Enemigo:
    def __init__(self, nombre, nivel):
        self.nombre = nombre
        self.nivel = nivel
        self.hp_max = 18 + nivel * 6
        self.hp = self.hp_max
        self.ataque = 4 + nivel * 2
        self.defensa = 1 + nivel // 2
        self.xp_otorgada = 20 + nivel * 10

    def esta_vivo(self):
        return self.hp > 0


def crear_enemigo(nivel_jugador):
    nombres = ["Gólem", "Bandido", "Araña gigante", "Espectro", "Lobo oscuro"]
    nivel = max(1, nivel_jugador + random.choice([-1, 0, 1]))
    return Enemigo(random.choice(nombres), nivel)


def calcular_danio(ataque, defensa):
    base = ataque - defensa
    return max(1, base + random.randint(-1, 2))


def turno_jugador(jugador, enemigo):
    while True:
        eleccion = input("\nElige acción ([A]tacar / [C]urarse): ").strip().lower()
        if eleccion in {"a", "atacar"}:
            danio = calcular_danio(jugador.ataque, enemigo.defensa)
            enemigo.hp -= danio
            print(f"Atacas a {enemigo.nombre} y haces {danio} de daño.")
            return
        if eleccion in {"c", "curar", "curarse"}:
            curacion = random.randint(6, 10)
            jugador.hp = min(jugador.hp_max, jugador.hp + curacion)
            print(f"Te curas {curacion} HP. HP actual: {jugador.hp}/{jugador.hp_max}.")
            return
        print("Acción inválida. Intenta de nuevo.")


def turno_enemigo(jugador, enemigo):
    danio = calcular_danio(enemigo.ataque, jugador.defensa)
    jugador.hp -= danio
    print(f"{enemigo.nombre} te golpea y hace {danio} de daño.")


def mostrar_estado(jugador, enemigo):
    print(
        f"\n{jugador.nombre} (Nv {jugador.nivel}) HP {jugador.hp}/{jugador.hp_max} "
        f"| {enemigo.nombre} (Nv {enemigo.nivel}) HP {enemigo.hp}/{enemigo.hp_max}"
    )


def jugar():
    print("Bienvenido al mini RPG de combate por turnos.\n")
    nombre = input("Nombre del héroe: ").strip() or "Héroe"
    jugador = Jugador(nombre)

    enemigos_derrotados = 0

    while jugador.esta_vivo():
        enemigo = crear_enemigo(jugador.nivel)
        print(
            f"\n¡Aparece un {enemigo.nombre} (Nv {enemigo.nivel})! "
            f"HP {enemigo.hp}/{enemigo.hp_max}."
        )

        while enemigo.esta_vivo() and jugador.esta_vivo():
            mostrar_estado(jugador, enemigo)
            turno_jugador(jugador, enemigo)
            if enemigo.esta_vivo():
                turno_enemigo(jugador, enemigo)

        if jugador.esta_vivo():
            enemigos_derrotados += 1
            print(f"\nDerrotaste a {enemigo.nombre}.")
            jugador.ganar_xp(enemigo.xp_otorgada)
            print(
                f"XP: {jugador.xp}/{jugador.xp_requerida}. "
                f"Enemigos derrotados: {enemigos_derrotados}."
            )
            continuar = input("¿Continuar? ([S]í / [N]o): ").strip().lower()
            if continuar in {"n", "no"}:
                break
        else:
            print("\nHas caído en batalla. Fin del juego.")

    print(
        f"\nResumen: Nivel {jugador.nivel}, XP {jugador.xp}/{jugador.xp_requerida}, "
        f"Enemigos derrotados {enemigos_derrotados}."
    )


if __name__ == "__main__":
    jugar()
