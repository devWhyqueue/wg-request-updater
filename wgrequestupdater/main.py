import logging.config
from importlib.resources import files
from time import sleep

from click import command, argument, option
from selenium.common.exceptions import WebDriverException

from wgrequestupdater.webdriver import web_driver

logging_config = str(files('config').joinpath('logging.ini'))
logging.config.fileConfig(logging_config, disable_existing_loggers=False)
log = logging.getLogger("wgrequestupdater.main")


@command()
@argument('username')
@argument('password')
@option('--exec-path', '-e', default=None, help="Path to the geckodriver executable.")
def cli(username, password, exec_path):
    from wgrequestupdater.updater import WgRequestUpdater
    log.info("WG Request updater successfully started.")
    while True:
        webdriver = web_driver(exec_path)
        req = WgRequestUpdater(webdriver)
        try:
            req.update(username, password)
        except WebDriverException:
            log.error("A WebDriver exception occurred!")
            log.debug("Following exception was thrown:", exc_info=True)
        finally:
            webdriver.quit()
            sleep(3600)


if __name__ == '__main__':
    cli()
