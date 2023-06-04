from chat.start import init_bot
from db.db_initializer import init_db
from utils.logger import init_logger

if __name__ == "__main__":
    init_logger()
    init_db()
    init_bot()
