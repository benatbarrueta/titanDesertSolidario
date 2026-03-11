import json

from app.db.session import SessionLocal
from app.db.models import Challenge, ChallengeOption, Warrior, Stage


def seed():
    db = SessionLocal()

    # ==========================
    # WARRIORS
    # ==========================
    if db.query(Warrior).count() == 0:
        warriors = [
            Warrior(id="beltran", 
                    dorsal=101, 
                    name="Beltran Sendagorta",
                    photo_url=None),
            Warrior(id="sergio", 
                    dorsal=102, 
                    name="Sergio Turull",
                    photo_url=None),
        ]
        db.add_all(warriors)
        print("Warriors creados")

    # ==========================
    # STAGES (listas para operar)
    # ==========================
    if db.query(Stage).count() == 0:
        stages = [
            Stage(
                id="stage-1",
                stage_number=1,
                name="Boumalne Dades – Boumalne Dades",
                start_location="Boumalne Dades",
                finish_location="Boumalne Dades",
                distance_km=98,
                elevation_gain_m=2175,
                is_loop=True,
                has_timed_challenge=True,
                is_published=True,
                is_open_for_contributions=True,
                is_archived=False,
                sort_order=1,
            ),
            Stage(
                id="stage-2",
                stage_number=2,
                name="Boumalne Dades – Battou",
                start_location="Boumalne Dades",
                finish_location="Battou",
                distance_km=105,
                elevation_gain_m=1550,
                is_published=True,
                is_open_for_contributions=True,
                is_archived=False,
                sort_order=2,
            ),
            Stage(
                id="stage-3",
                stage_number=3,
                name="Battou – Sidi Ali",
                start_location="Battou",
                finish_location="Sidi Ali",
                distance_km=98,
                elevation_gain_m=352,
                is_marathon_sector=True,
                is_published=True,
                is_open_for_contributions=True,
                is_archived=False,
                sort_order=3,
            ),
            Stage(
                id="stage-4",
                stage_number=4,
                name="Sidi Ali – Merzouga",
                start_location="Sidi Ali",
                finish_location="Merzouga",
                distance_km=123,
                elevation_gain_m=804,
                is_marathon_sector=True,
                is_published=True,
                is_open_for_contributions=True,
                is_archived=False,
                sort_order=4,
            ),
            Stage(
                id="stage-5",
                stage_number=5,
                name="Merzouga – Merzouga",
                start_location="Merzouga",
                finish_location="Merzouga",
                distance_km=87,
                elevation_gain_m=606,
                is_loop=True,
                has_navigation_sector=True,
                is_published=True,
                is_open_for_contributions=True,
                is_archived=False,
                sort_order=5,
            ),
            Stage(
                id="stage-6",
                stage_number=6,
                name="Merzouga – Maadid",
                start_location="Merzouga",
                finish_location="Maadid",
                distance_km=74,
                elevation_gain_m=609,
                is_published=True,
                is_open_for_contributions=True,
                is_archived=False,
                sort_order=6,
            ),
        ]
        db.add_all(stages)
        print("Stages creados")

    # ==========================
    # CHALLENGES
    # ==========================
    if db.query(Challenge).count() == 0:

        def create_challenge(slug, title, price, icon, options, stage_id=None, sort_order=0):
            challenge = Challenge(
                id=slug,
                stage_id=stage_id,
                title=title,
                description=title,
                price=price,
                icon=icon,
                currency="EUR",
                image_url=None,
                is_active=True,
                is_published=True,
                is_archived=False,
                available_from=None,
                available_until=None,
                sort_order=sort_order,
            )
            db.add(challenge)
            db.flush()

            for opt in options:
                db.add(
                    ChallengeOption(
                        challenge_id=slug,
                        name=opt["name"],
                        description=opt.get("description", ""),
                        subject_type=opt["subject_type"],
                        answer_type=opt["answer_type"],
                        number_of_selections=opt.get("number_of_selections", 1),
                        config_json=json.dumps(opt.get("config", {}), ensure_ascii=False),
                    )
                )

        create_challenge(
            "orden-y-posicion",
            "Orden y Posición",
            5,
            "🏁",
            [
                {"name": "1º del Equipo", "subject_type": "team", "answer_type": "warrior_pick"},
                {"name": "Top 3 del Equipo (sin orden)", "subject_type": "team", "answer_type": "warrior_pick", "number_of_selections": 3},
                {"name": "Último del Equipo", "subject_type": "team", "answer_type": "warrior_pick"},
                {"name": "Quién gana más etapas", "subject_type": "team", "answer_type": "warrior_pick"},
            ],
            stage_id=None,
            sort_order=1,
        )

        create_challenge(
            "tiempos",
            "Tiempos",
            5,
            "⏱️",
            [
                {"name": "Tiempo de corredor en etapa", "subject_type": "warrior_stage", "answer_type": "time"},
                {"name": "Etapa del primer pinchazo", "subject_type": "warrior", "answer_type": "stage_choice"},
                {
                    "name": "Tiempo en Etapa Reina",
                    "subject_type": "warrior",
                    "answer_type": "time",
                    "config": {"fixed_stage_id": "stage-4"}
                },
            ],
            stage_id=None,
            sort_order=2,
        )

        create_challenge(
            "kilometros",
            "Kilómetros",
            5,
            "📍",
            [
                {"name": "Km del primer pinchazo", "subject_type": "warrior_stage", "answer_type": "number"},
                {"name": "Km del primer problema mecánico", "subject_type": "warrior_stage", "answer_type": "number"},
                {"name": "Km en el que revienta físicamente", "subject_type": "warrior_stage", "answer_type": "number"},
            ],
            stage_id=None,
            sort_order=3,
        )

        create_challenge(
            "averias-incidentes",
            "Averías e Incidentes",
            5,
            "🔧",
            [
                {"name": "Número total de pinchazos", "subject_type": "warrior", "answer_type": "number"},
                {
                    "name": "Tipo de avería principal",
                    "subject_type": "warrior",
                    "answer_type": "choice",
                    "config": {
                        "allowed_values": [
                            "pinchazo",
                            "cadena",
                            "cambio",
                            "frenos",
                            "rueda",
                            "otro"
                        ]
                    }
                },
                {"name": "Número de caídas", "subject_type": "warrior", "answer_type": "number"},
            ],
            stage_id=None,
            sort_order=4,
        )

        create_challenge(
            "momentos-virales",
            "Momentos Virales",
            5,
            "😅",
            [
                {
                    "name": "¿Abandona por agotamiento?",
                    "subject_type": "warrior",
                    "answer_type": "boolean_stage",
                    "config": {"stage_required_if_true": True}
                },
                {
                    "name": "¿Se le ve llorar en meta?",
                    "subject_type": "warrior",
                    "answer_type": "boolean_stage_optional"
                },
                {"name": "Frase típica al acabar", "subject_type": "warrior", "answer_type": "text"},
                {
                    "name": "Pierde algo durante la carrera",
                    "subject_type": "warrior",
                    "answer_type": "boolean_stage_optional"
                },
            ],
            stage_id=None,
            sort_order=5,
        )

        create_challenge(
            "mental-resistencia",
            "Mental y Resistencia",
            5,
            "🧠",
            [
                {"name": "Etapa más dura", "subject_type": "warrior", "answer_type": "stage_choice"},
                {"name": "Día que duerme peor", "subject_type": "warrior", "answer_type": "stage_choice"},
                {"name": "¿Necesita ayuda médica?", "subject_type": "warrior", "answer_type": "boolean"},
            ],
            stage_id=None,
            sort_order=6,
        )

        create_challenge(
            "duelos-corredores",
            "Duelos entre Corredores",
            10,
            "👥",
            [
                {"name": "Quién aguanta más sin pinchar", "subject_type": "stage", "answer_type": "warrior_pick"},
                {"name": "Quién llega antes a meta", "subject_type": "stage", "answer_type": "warrior_pick"},
                {"name": "Quién abandona antes (si pasa)", "subject_type": "stage", "answer_type": "warrior_pick"},
            ],
            stage_id=None,
            sort_order=7,
        )

        create_challenge(
            "retos-equipo",
            "Retos de Equipo",
            10,
            "🏜️",
            [
                {"name": "Todos terminan la carrera", "subject_type": "team", "answer_type": "boolean"},
                {"name": "Número total de abandonos", "subject_type": "team", "answer_type": "number"},
                {"name": "Etapa con más abandonos", "subject_type": "team", "answer_type": "stage_choice"},
            ],
            stage_id=None,
            sort_order=8,
        )

        print("Challenges creados")

    db.commit()
    db.close()


if __name__ == "__main__":
    seed()