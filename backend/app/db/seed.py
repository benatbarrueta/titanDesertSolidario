from app.db.session import SessionLocal
from app.db.models import Challenge, ChallengeOption, Warrior


def seed():
    db = SessionLocal()

    # ==========================
    # WARRIORS
    # ==========================
    if db.query(Warrior).count() == 0:
        warriors = [
            Warrior(id="beltran", dorsal=101, name="Beltran Sendagorta"),
            Warrior(id="sergio", dorsal=102, name="Sergio Turull"),
        ]
        db.add_all(warriors)
        print("Warriors creados")

    # ==========================
    # CHALLENGES
    # ==========================

    if db.query(Challenge).count() == 0:

        def create_challenge(slug, title, price, icon, options):
            challenge = Challenge(
                id=slug,
                title=title,
                description=title,
                price=price,
                icon=icon,
                is_active=True
            )
            db.add(challenge)
            db.flush()

            for opt in options:
                db.add(
                    ChallengeOption(
                        challenge_id=slug,
                        name=opt["name"],
                        description=opt.get("description", ""),
                        type="ranking",
                        number_of_selections=opt.get("selections", 1)
                    )
                )

        # ORDEN Y POSICIÓN
        create_challenge(
            "orden-y-posicion",
            "Orden y Posición",
            5,
            "🏁",
            [
                {"name": "1º del Equipo", "selections": 1},
                {"name": "Top 3 del Equipo (sin orden)", "selections": 3},
                {"name": "Último del Equipo", "selections": 1},
                {"name": "Quién gana más etapas", "selections": 1},
            ]
        )

        # TIEMPOS
        create_challenge(
            "tiempos",
            "Tiempos",
            5,
            "⏱️",
            [
                {"name": "Tiempo total de [Corredor]", "selections": 1},
                {"name": "Tiempo hasta primer pinchazo", "selections": 1},
                {"name": "Tiempo en Etapa Reina", "selections": 1},
            ]
        )

        # KILÓMETROS
        create_challenge(
            "kilometros",
            "Kilómetros",
            5,
            "📍",
            [
                {"name": "Km del primer pinchazo", "selections": 1},
                {"name": "Km del primer problema mecánico", "selections": 1},
                {"name": "Km en el que revienta físicamente", "selections": 1},
            ]
        )

        # AVERÍAS
        create_challenge(
            "averias-incidentes",
            "Averías e Incidentes",
            5,
            "🔧",
            [
                {"name": "Número total de pinchazos", "selections": 1},
                {"name": "Tipo de avería principal", "selections": 1},
                {"name": "Número de caídas", "selections": 1},
            ]
        )

        # MOMENTOS VIRALES
        create_challenge(
            "momentos-virales",
            "Momentos Virales",
            5,
            "😅",
            [
                {"name": "¿Abandona por agotamiento?", "selections": 1},
                {"name": "¿Se le ve llorar en meta?", "selections": 1},
                {"name": "Frase típica al acabar", "selections": 1},
                {"name": "Pierde algo durante la carrera", "selections": 1},
            ]
        )

        # MENTAL Y RESISTENCIA
        create_challenge(
            "mental-resistencia",
            "Mental y Resistencia",
            5,
            "🧠",
            [
                {"name": "Etapa más dura", "selections": 1},
                {"name": "Día que duerme peor", "selections": 1},
                {"name": "¿Necesita ayuda médica?", "selections": 1},
            ]
        )

        # DUELOS
        create_challenge(
            "duelos-corredores",
            "Duelos entre Corredores",
            10,
            "👥",
            [
                {"name": "Quién aguanta más sin pinchar", "selections": 1},
                {"name": "Quién llega antes a meta", "selections": 1},
                {"name": "Quién abandona antes (si pasa)", "selections": 1},
            ]
        )

        # RETOS DE EQUIPO
        create_challenge(
            "retos-equipo",
            "Retos de Equipo",
            10,
            "🏜️",
            [
                {"name": "Todos terminan la carrera", "selections": 1},
                {"name": "Número total de abandonos", "selections": 1},
                {"name": "Etapa con más abandonos", "selections": 1},
            ]
        )

        print("Challenges creados")

    db.commit()
    db.close()


if __name__ == "__main__":
    seed()
