from actions.FCAI_DB import FCAI_DB
from actions.Letters_Mapping import map_subject_name

# Access database
db = FCAI_DB()
""" if FCAI Subjects.dp is deleted uncomment below line """
# db.create_DB()
bylaw = db.get_tables('bylaw')
gpa_dict = db.get_tables('GPA')
schedule = db.get_schedule()


def get_subjects_priority(student_schedule, gpa):
    """
        Parameters:
            student_schedule: list of semester subject's
            gpa: int of student's GPA

        Return:
            student_schedule: string of best schedule
    """

    min_priority = {}

    for i in student_schedule:
        if i not in bylaw.keys():
            # if subject not in bylaw give it 0 priority
            min_priority[i] = 0
        else:
            min_priority[i] = int(bylaw[i][-1])
    # sort priorities ascending
    min_priority = sorted(min_priority.items(), key=lambda x: x[1], reverse=False)

    try:
        """ check on gpa to know how many subjects can be registered by student """
        if 1.5 < gpa < 2:
            student_schedule.remove(min_priority[0][0])
            student_schedule.remove(min_priority[1][0])

        elif gpa < 1.5:
            student_schedule.remove(min_priority[0][0])
            student_schedule.remove(min_priority[1][0])
            student_schedule.remove(min_priority[2][0])

        return ', '.join(student_schedule)
    except (KeyError, ValueError):
        print(KeyError, ValueError)


def get_best_schedule(student_schedule, failed_subject, gpa):
    """
        Searching on which subject in the schedule is depended on the failed subjects
                change the failed subjects with subject which depend on it

        Parameters:
            student_schedule: list of semester subjects
            failed_subject: list of failed subjects
            gpa: int of student GPA

        Return:
            best_schedule: string of best schedule
    """

    for i in student_schedule:
        index = student_schedule.index(i)
        # if subject is in bylaw
        if i in bylaw.keys():
            # check on this subject has 2 or 1 perquisite
            if len(bylaw[i]) > 1:
                if bylaw[i][0] in failed_subject:
                    student_schedule[index] = bylaw[0]

                elif bylaw[i][1] in failed_subject:
                    student_schedule[index] = bylaw[i][1]

            else:
                if bylaw[i][0] in failed_subject:
                    student_schedule[index] = bylaw[i][0]

    best_schedule = get_subjects_priority(student_schedule, int(gpa))
    return best_schedule


def get_failed_subjects(failed_subject, year, gpa):
    """
        Parameters:
            failed_subject: list of f subjects
            year: string of student's year and his department
            gpa: string of GPA

        Return:
            best_schedule: string of best schedule
    """
    student_schedule = schedule[year]
    best_schedule = "افضل جدول لك: "
    best_schedule += get_best_schedule(student_schedule, failed_subject, gpa)
    return best_schedule




def get_schedule(year):
    student_schedule = schedule[year]
    best_schedule = "جدولك: "
    print(student_schedule)
    return best_schedule + ', '.join(student_schedule)


def get_all_previous_prerequisites(subject, student_grades, subjects):
    """
        Parameters:
            subject: string for subject name
            subjects: subjects list
            student_grades: dictionary of student's results

        Return:
            string tell student what is the prerequisites of this subject
    """

    try:
        # get prerequisites of this subject
        subject = map_subject_name(subject, list(bylaw.keys()))
        subject_prerequisites = bylaw[subject]
        if subject_prerequisites[0][0] == 'none':
            return ''

    except KeyError:
        return subject

    for i in subject_prerequisites[0]:
        try:
            # check he take and pass these prerequisites
            failed = student_grades['f']
            if i not in subjects or i in failed:
                subject = i
                subject += ', ' + get_all_previous_prerequisites(subject, student_grades, subjects)
                return subject

        except KeyError:
            if i.lower() not in subjects:
                subject = i
                subject += ', ' + get_all_previous_prerequisites(subject, student_grades, subjects)
                return subject
            else:
                return ''


def ask_for_one_subject(subject, student_grades, subjects, cumulative_hours):
    """
        Parameters:
            subject: string for subject name
            subjects: subjects ;ist
            student_grades: dictionary of student's results
            cumulative_hours: number of hours that student took

        Return:
            string tell student can register this subject or not
    """
    selected1 = 'selected topics in artificial intelligence 1'
    selected2 = 'selected topics in artificial intelligence 2'

    if subject == selected1 and cumulative_hours >= 60:
        print("youssef")
        return f'تقدر تسجل {selected1}'
    elif subject == selected2 and cumulative_hours >= 60:
        return f'تقدر تسجل {selected2}'
    elif (subject == selected2 or subject == selected1) and cumulative_hours < 60:
        return 'لازم تجتاز 60 ساعة'

    subject = get_all_previous_prerequisites(subject, student_grades, subjects)

    if subject != '' and subject is not None:
        return f'لازم تاخد {subject[:-2]} الأول'

    return 'تقدر تسجلها'
