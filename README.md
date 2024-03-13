# FCFM Ramos

Plataforma de opiniones e información sobre los ramos FCFM, para ayudar al momento de toma de ramos de malla y electivos. Inspirado en <https://github.com/cadcc/ramosCC>.

[Development trello board](https://trello.com/b/PSyFevmn/ramos-fcfm)

Stack:

- Python
  - Linter: Ruff
- Flask
  - FlaskWTF
  - SQLAlchemy
  - SQLite
- Firebase (for authentication only)
- AlpineJS

Resources:

- Icons: <https://feathericons.com/>

## Installation

Set up the following files:

- `fcfmramos/web_scraper/config.py` (WIP)
- `fcfmramos/config.py` with the line `secret_key=_` (the secret key for flask)
- `fbconfig.json` with the firebase API info
- `fcfm-ramos-key.json` with the firebase auth info

Then:

```bash
pip install -r requirements.txt
```

## Database

First run:

```bash
flask --app fcfmramos db init
```

Changes to model:

```bash
flask --app fcfmramos db migrate -m "Message"
flask --app fcfmramos db upgrade
```

Populate with scraper data:

```bash
flask --app fcfmramos catalogos_scraper
flask --app fcfmramos planes_scraper
```

## Running locally

```bash
flask --app fcfmramos run --debug
```

## Temporary stuff for later

### Scoring

Achievements (awarded once):

- Verify email: 5p
- Like/dislike a course: 5p
- Like/dislike a text review: 5p
- Rate carga, utilidad and dificultad: 15p
- Write a summary: 20p
- Write a review: 20p

Renewable:

- Log in (daily): 1p
- Summary receives a like: 1p
- Review receives a like: 1p

### Emoji-scales

Dificultad:

1. 🥱 Trivial
2. 😎 Manejable
3. 😬 Desafiante
4. 😫 Duro
5. 💀 Letal

Carga:

1. 🎁 Regalado
2. 😴 Ligero
3. 😅 Moderado
4. 😰 Pesado
5. 🥵 Brutal

Utilidad:

1. 🙃 Inútil
2. 🙂 Básico
3. 🤓 Valioso
4. 🧠 Esencial
5. 🤩 Vital

Like/dislike ratio (calculated, not voted on):

1. 💖 Favorito
2. ❤ Amado
3. 🤔 Controversial
4. 😡 Odiado
5. 👿 Detestado

## License

To be defined once the MVP is ready, for now consider it free to re-use and modify for educational purposes. No commercial use. Contribution is welcome, but in these early stages it would be best if you contact me first <contact@eri.cl>.
