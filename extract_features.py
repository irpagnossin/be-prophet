import csv
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pdb

def to_time(datetime_string):
    return datetime.strptime(datetime_string, '%d/%m/%Y %I:%M:%S %p')

def meeting_sessions(zoom_log):
    sessions = {}

    with open(zoom_log, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for (name, email, start, end, duration) in reader:
            session = (to_time(start), to_time(end), int(duration))

            key = (email if email else name).lower()

            try:
                sessions[key].append(session)
            except KeyError:
                sessions[key] = [session]
    
    for (_, student_sessions) in sessions.items():
        student_sessions.sort(key=lambda tuple: tuple[0])

    return sessions

def meeting_date(meeting_sessions):
    session_starts = sorted([
        session_start \
        for user_sessions in meeting_sessions.values() \
        for (session_start, _, _) in user_sessions
    ])

    return session_starts[0].date()

def users_count(meeting_sessions):
    return len(meeting_sessions.keys())

def sessions_count(sessions):
    return len(sessions)

def average_session_duration(sessions, lesson_duration):
    durations = [duration for (_, _, duration) in sessions]
    if len(durations) == 0:
        return 0
    else:
        return np.mean(durations) / lesson_duration

def time_delta(t1:datetime, t2:datetime):

    delta = t2 - t1

    seconds_in_a_day = 24 * 3600

    return (delta.days * seconds_in_a_day + delta.seconds) / 60

def arrival_delay(sessions, lesson_starts_at:datetime):
    '''
    Positivo se o aluno acessou a aula antes do início
    '''
    # TODO: adicionar tolerância
    return time_delta(sessions[0][0], lesson_starts_at)

def early_departure(sessions, lesson_ends_at):
    '''
    Positivo se o aluno deixou a aula após o término
    '''
    # TODO: adicionar tolerância
    return time_delta(lesson_ends_at, sessions[-1][1])

def time_delta_score(time_delta, tolerance=15):
    return 0 if time_delta > -tolerance else time_delta

def attendance(sessions, lesson_duration):
    '''
    attendance = # sessões x duração média das sessões
    '''
    return np.clip(np.sum([duration for (_, _, duration) in sessions]) / lesson_duration, 0, 1)

def session_duration_histogram(class_sessions, lesson, density=True):
    '''
    '''
    durations = [
        duration \
        for student_sessions in class_sessions.values() \
        for (_, _, duration) in student_sessions
    ]
    
    bins = range(0, np.max(durations), 10)
    return np.histogram(durations, bins=bins, density=density)

def presence(sessions, lesson):
    condicaoA = attendance(sessions, lesson.duration) > 0.7
    condicaoB = arrival_delay(sessions, lesson.start) > -15 # minutos
    condicaoC = early_departure(sessions, lesson.end) > -15 # minutos

    return condicaoA and condicaoB and condicaoC

def save_user_features(commission_code, class_sessions, lesson, output_filename):
    date = meeting_date(class_sessions)

    with open(output_filename, 'w') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(['code', 'date', 'id', 'avg_sess_duration', 'sess_count', 'arrival_delay', 'early_departure'])

        for (student_name, student_sessions) in class_sessions.items():
            student_delay = arrival_delay(student_sessions, lesson.start)
            student_early_departure = early_departure(student_sessions, lesson.end)

            writer.writerow([
                commission_code,
                date,
                student_name,
                average_session_duration(student_sessions, lesson.duration),
                sessions_count(student_sessions),
                student_delay,
                student_early_departure
            ])

def save_meeting_histogram(code, class_sessions, output_filename):
    date = meeting_date(class_sessions)

    frequencies, edges = session_duration_histogram(class_sessions, lesson, density=False)

    n_rows = len(frequencies)
    pd.DataFrame(data={
        'code': [code] * n_rows,
        'date': [date] * n_rows,
        'bin': edges[1:],
        'frequency': frequencies
    }).to_csv(output_filename, index=False)


class Lesson():
    def __init__(self, start, duration):
        self.start = start
        self.end = start + duration
        self.duration = duration.seconds / 60

if __name__ == '__main__':
    code = 'DS 2020 TN05'
    class_sessions = meeting_sessions('data/20_12_02.csv')
    lesson = Lesson(datetime(2020,12,2,19), timedelta(hours=2, minutes=15))

    save_user_features(code, class_sessions, lesson, 'output/user_features.csv')
    save_meeting_histogram(code, class_sessions, 'output/histogram.csv')
