def list_to_intervals(lst: list[int]) -> list[list[int]]:
    '''Попарная группировка начала и конца интервалов'''
    return [[lst[i], lst[i+1]] for i in range(0, len(lst), 2)]


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    '''Cлияние интервалов'''
    if not intervals:
        return []
    sorted_intervals = sorted(intervals, key=lambda x: x[0])  # Сортировка по началу интервала
    merged = [sorted_intervals[0]]  # Взятие первого интервала за основу
    for current in sorted_intervals[1:]:
        last = merged[-1]  # Получение последнего интервала из уже слитых
        if current[0] <= last[1]:  # Если начало текущего интервала меньше конца последнего
            merged[-1][1] = max(last[1], current[1])  # Объединение интервалов в один
        else:
            merged.append(current)  # Добавление интервала в список слитых
    return merged


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson = intervals['lesson']  # Получение интервала урока
    pupil_intervals = list_to_intervals(intervals['pupil'])  # Попарная группировка для ученика
    tutor_intervals = list_to_intervals(intervals['tutor'])  # Попарная группировка для учителя

    merged_pupil = merge_intervals(pupil_intervals)  # Слияние интервалов для ученика
    merged_tutor = merge_intervals(tutor_intervals)  # Слияние интервалов для учителя

    i = j = 0  # Индексы
    overlaps = []  # Список с пересечениями интервалов
    while i < len(merged_pupil) and j < len(merged_tutor):  # Одновременное прохождение по интервала ученика и учителя
        p_start, p_end = merged_pupil[i]  # Текущий интервал ученика
        t_start, t_end = merged_tutor[j]  # Текущий интервал учителя

        # Сравнение интервалов ученика и учителя
        start = max(p_start, t_start)
        end = min(p_end, t_end)

        if start < end:
            overlaps.append([start, end])  # Добавление пересечения
            if p_end < t_end:  # Если ученик вышел раньше учителя
                i += 1  # Следующий интервал ученика
            else:
                j += 1  # Следующий интервал учителя
        elif p_end < t_end:  # Если ученик вышел раньше учителя
            i += 1  # Следующий интервал ученика
        else:
            j += 1  # Следующий интервал учителя

    lesson_start, lesson_end = lesson  # Интервал урока
    total = 0  # Суммарное время
    for start, end in overlaps:
        # Сравнение пересечения и интервала урока
        actual_start = max(start, lesson_start)
        actual_end = min(end, lesson_end)
        
        if actual_start < actual_end:  # Если интервал корректен
            total += (actual_end - actual_start)  # Подсчет времени и прибавка к общему
    return total
