from time import time

from flask import current_app as app
from app.models import Deployed


class UptimeController:
    @staticmethod
    def run_sql_script():
        ms_time = int(round(time() * 1000))
        data = app.session.query(Deployed).first()
        if data:
            app.session.delete(data)
            app.session.commit()

        data = Deployed(ms_time=ms_time)
        app.session.add(data)
        app.session.commit()

        return ms_time

    @staticmethod
    def get():
        data = app.session.query(Deployed).first()
        current_time = int(round(time() * 1000))

        return {
            'uptime': current_time - data.ms_time
        }

