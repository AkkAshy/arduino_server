from datetime import datetime
from .models import ArduinoSchedule

def can_process_arduino_post(user):
    try:
        schedule = user.arduino_schedule
    except ArduinoSchedule.DoesNotExist:
        return True  # если расписание не установлено, обрабатывать всегда

    now = datetime.now().time()
    if schedule.start_time <= schedule.end_time:
        return schedule.start_time <= now <= schedule.end_time
    else:
        # случай, когда диапазон «через полночь», например 20:00 - 08:00
        return now >= schedule.start_time or now <= schedule.end_time
