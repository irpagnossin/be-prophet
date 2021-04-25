import csv
from datetime import datetime, timedelta
import numpy as np
import pdb

def to_time(datetime_string):
    return datetime.strptime(datetime_string, '%d/%m/%Y %I:%M:%S %p')

def extract_sessions(zoom_log):
    sessions = {}

    with open(zoom_log, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for (name, _, start, end, duration) in reader:
            session = (to_time(start), to_time(end), int(duration))
            name = name.lower()

            try:
                sessions[name].append(session)
            except KeyError:
                sessions[name] = [session]
    
    for (_, student_sessions) in sessions.items():
        student_sessions.sort(key=lambda tuple: tuple[0])

    return sessions

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

def delay(sessions, lesson_starts_at:datetime):
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
    return min(1, np.sum([duration for (_, _, duration) in sessions]) / lesson_duration)

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
    condicaoA = attendance(student_sessions, lesson.duration) > 0.7
    condicaoB = delay(student_sessions, lesson.start) > -15 # minutos
    condicaoC = early_departure(student_sessions, lesson.end) > -15 # minutos

    return condicaoA and condicaoB and condicaoC

class Lesson():
    def __init__(self, start, duration):
        self.start = start
        self.end = start + duration
        self.duration = duration.seconds / 60

if __name__ == '__main__':
    class_sessions = extract_sessions('data/20_12_02.csv')
    lesson = Lesson(datetime(2020,12,2,19), timedelta(hours=2, minutes=15))

    for (student_name, student_sessions) in class_sessions.items():
        student_delay = delay(student_sessions, lesson.start)
        student_early_departure = early_departure(student_sessions, lesson.end)

        print('--------------')
        print(f'Nome: {student_name}')
        print('Duração média das sessões: ', average_session_duration(student_sessions, lesson.duration))
        print('# de sessões:', sessions_count(student_sessions))
        print('Delta 1 (atraso inicial): ', student_delay)
        print('Delta 1 score:', time_delta_score(student_delay))
        print('Delta 2 (saída antecipada):', student_early_departure)
        print('Delta 2 score:', time_delta_score(student_early_departure))
        print('Presença:', attendance(student_sessions, lesson.duration))
        print('Aluno é considerado presente?', presence(student_sessions, lesson))

    print('================')

    frequencies, edges = session_duration_histogram(class_sessions, lesson, density=False)
    print('== Histograma de sessões ==')
    print('frequencies:', frequencies)
    print('edges', edges)
    for i, frequency in enumerate(frequencies):
        print(edges[i+1], '+' * frequency)