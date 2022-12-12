from TelegramBot.main import start_bot
from api.api import start_server
import multiprocessing




if __name__ == '__main__':
    p1 = multiprocessing.Process(target=start_bot)
    p2 = multiprocessing.Process(target=start_server)
    p1.start()
    p2.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        p1.kill()
        p2.kill()
    except:
        pass