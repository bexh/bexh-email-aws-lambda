import codecs
import os
from abc import ABC, abstractmethod

from jinja2 import Template

from main.src.email import MailerFactory
from main.src.logger import LoggerFactory


class EmailHandlerOperator(ABC):
    def __init__(self, name, event, context):
        log_level = os.environ.get("LOG_LEVEL", None)
        self.logger = LoggerFactory().get_logger(name, log_level)
        self.event = event
        self.context = context
        self.mailer = MailerFactory().get_mailer(logger=self.logger)
        self.run()

    def run(self):
        try:
            self.logger.info("Start")
            self.logger.debug(f"Event: {self.event}")
            self.logger.debug(f"Context: {self.context}")
            self.execute()
            self.logger.info("Success")
        except Exception as e:
            self.logger.error(f"Email failed to send: {e}")

    def template(self, html_template: str, params: dict) -> str:
        self.logger.info(f"Templating with params: {params}")
        t = Template(html_template)
        return t.render(**params)

    @staticmethod
    def read_html(file_path: str) -> str:
        f = codecs.open(file_path, 'r')
        content = f.read()
        return content

    def send_email(self, from_email: str, to_email: str, subject: str, html_content: str):
        self.mailer.send_message(
            from_email=from_email,
            to_email=to_email,
            subject=subject,
            html_content=html_content
        )

    @abstractmethod
    def execute(self):
        pass
