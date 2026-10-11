
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "bot" / "data"


def get_bot_token() -> str:
    token = os.getenv("BOT_TOKEN")

    if not token:
        env_path = BASE_DIR / ".env"

        if env_path.is_file():
            for line in env_path.read_text(
                encoding="utf-8-sig"
            ).splitlines():
                line = line.strip()

                if line.startswith("BOT_TOKEN="):
                    token = line.split("=", 1)[1].strip()
                    token = token.strip('"').strip("'")
                    break

    if not token:
        raise RuntimeError(
            "BOT_TOKEN topilmadi. "
            "Loyiha papkasidagi .env faylini tekshiring."
        )

    return token
