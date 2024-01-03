"""Utils functions"""
import calendar
from datetime import datetime, timedelta, date

import jwt

# Django
from django.conf import settings
from django.utils import timezone

# Models
from kumbio_api_v2.organizations.models import Professional


def generate_auth_token(user, type, **kwargs):
    """Create JWT token that the user can use to login for specific context [origin]."""
    expiration_date = timezone.localtime() + timedelta(days=2)
    payload = {
        "user": user.email,
        "exp": int(expiration_date.timestamp()),
        "type": type,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def decode_auth_token(token):
    """Decode JWT auth token based on origin."""
    error = []
    payload = ""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
        except jwt.ExpiredSignatureError:
            error.append("Verification link has expired.")
    except jwt.PyJWTError:
        error.append("Invalid token")
    if not payload:
        error.append("Not payload")
    return payload, error


def generate_available_hours(sorted_busy_hours, work_start_time, work_end_time):
    if sorted_busy_hours:
        intervals = [{"hour_init": work_start_time.strftime("%H:%M"), "hour_end": sorted_busy_hours[0]["hour_init"]}]
        # Crear intervalos entre las horas ocupadas
        for i in range(len(sorted_busy_hours) - 1):
            if sorted_busy_hours[i]["hour_end"] != sorted_busy_hours[i + 1]["hour_init"]:
                intervals.append({"hour_init": sorted_busy_hours[i]["hour_end"], "hour_end": sorted_busy_hours[i + 1]["hour_init"]})

        # Crear intervalo desde la última hora ocupada hasta la hora de finalización
        intervals.append({"hour_init": sorted_busy_hours[-1]["hour_end"], "hour_end": work_end_time.strftime("%H:%M")})
    else:
        intervals = [{"hour_init": work_start_time.strftime("%H:%M"), "hour_end": work_end_time.strftime("%H:%M")}]
    return intervals


def professiona_availability(professional, place, service, date_availability):
    """Check availability professional."""
    if not date_availability:
        current_date = datetime.now().date()
        current_day_of_week = current_date.strftime("%A").upper()
    else:
        current_date = date.fromisoformat(date_availability)
        current_day_of_week = calendar.day_name[current_date.isoweekday()].upper()
    service_duration = service.duration
    if professional != "all":
        busy_hours = []
        non_working_hours = (
            professional.professional_schedule.filter(professional=professional, day=current_day_of_week, is_working=False)
            .values_list("hour_init", "hour_end")
            .order_by("hour_init")
        )
        appointments = (
            professional.professional_appointments.filter(professional_user=professional, date=current_date)
            .values_list("hour_init", "hour_end")
            .order_by("hour_init")
        )
        for no_working in non_working_hours:
            busy_hours.append(
                {
                    "hour_init": no_working[0].strftime("%H:%M"),
                    "hour_end": no_working[1].strftime("%H:%M"),
                }
            )
        for appointment in appointments:
            busy_hours.append(
                {
                    "hour_init": appointment[0].strftime("%H:%M"),
                    "hour_end": appointment[1].strftime("%H:%M"),
                }
            )
        work_schedule = professional.professional_schedule.filter(
            professional=professional, day=current_day_of_week, is_working=True
        ).first()
        work_start_time = work_schedule.hour_init
        work_end_time = work_schedule.hour_end
        sorted_busy_hours = sorted(busy_hours, key=lambda x: x["hour_init"])
        availability_intervals = generate_available_hours(sorted_busy_hours, work_start_time, work_end_time)
        schedule_availability = {}
        schedule_availability["professional_pk"] = professional.pk
        schedule_availability["availability"] = []
        for interval in availability_intervals:
            start_time = datetime.strptime(interval["hour_init"], "%H:%M").time()
            end_time = datetime.strptime(interval["hour_end"], "%H:%M").time()
            current_time = datetime.combine(current_date, start_time)
            finish_time = datetime.combine(current_date, end_time)
            while current_time < finish_time:
                next_time = current_time + timedelta(minutes=service_duration)
                if next_time <= finish_time:
                    schedule_availability.get("availability").append(
                        {"hour_init": current_time.strftime("%H:%M"), "hour_end": next_time.strftime("%H:%M")}
                    )
                current_time = next_time
    else:
        professionals = Professional.objects.filter(
            services=service, professional_schedule__day=current_day_of_week, professional_schedule__is_working=True
        ).prefetch_related("professional_schedule", "professional_appointments")
        schedule_availability = {}
        schedule_availability["availability"] = []
        for professional in professionals:
            busy_hours = []
            non_working_hours = (
                professional.professional_schedule.filter(professional=professional, day=current_day_of_week, is_working=False)
                .values_list("hour_init", "hour_end")
                .order_by("hour_init")
            )
            appointments = (
                professional.professional_appointments.filter(professional_user=professional, date=current_date)
                .values_list("hour_init", "hour_end")
                .order_by("hour_init")
            )
            for no_working in non_working_hours:
                busy_hours.append(
                    {
                        "hour_init": no_working[0].strftime("%H:%M"),
                        "hour_end": no_working[1].strftime("%H:%M"),
                    }
                )
            for appointment in appointments:
                busy_hours.append(
                    {
                        "hour_init": appointment[0].strftime("%H:%M"),
                        "hour_end": appointment[1].strftime("%H:%M"),
                    }
                )
            work_schedule = professional.professional_schedule.filter(
                professional=professional, day=current_day_of_week, is_working=True
            ).first()
            work_start_time = work_schedule.hour_init
            work_end_time = work_schedule.hour_end
            sorted_busy_hours = sorted(busy_hours, key=lambda x: x["hour_init"])
            availability_intervals = generate_available_hours(sorted_busy_hours, work_start_time, work_end_time)
            for interval in availability_intervals:
                start_time = datetime.strptime(interval["hour_init"], "%H:%M").time()
                end_time = datetime.strptime(interval["hour_end"], "%H:%M").time()
                current_time = datetime.combine(current_date, start_time)
                finish_time = datetime.combine(current_date, end_time)
                while current_time < finish_time:
                    next_time = current_time + timedelta(minutes=service_duration)
                    if next_time <= finish_time:
                        schedule_availability.get("availability").append(
                            {
                                "professional_pk": professional.pk,
                                "hour_init": current_time.strftime("%H:%M"),
                                "hour_end": next_time.strftime("%H:%M"),
                            }
                        )
                    current_time = next_time
        schedule_availability = sorted(schedule_availability.get("availability"), key=lambda x: x["hour_init"])
    return schedule_availability
