import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def map_letters(word):
    """
        Parameters:
            word: string of subject name
        Return:
            converted_word: numpy array with values at index of each letter
    """
    converted_word = np.zeros(35)

    for i in word:
        try:
            if i.isdigit():
                # check if i is digit to get ascii code of it and increase one at it's index
                converted_word[ord(i) - 48] += 1
            else:
                # get ascii code of characters and increase one at it's index
                converted_word[ord(i) - 97] += 1

        except IndexError:
            continue
    return converted_word


def map_subjects(subjects):
    """
        Parameters:
            subjects: list of all subjects
        Return:
            subjects_encoder: numpy array with values at index of each letter
    """
    subjects_encoder = np.zeros((len(subjects), 35))

    for j in range(len(subjects)):
        subjects_encoder[j] = map_letters(subjects[j])
    return subjects_encoder


def check_language(word):
    """
        Parameters:
            word: string of subject name
        Return:
            True if it is english word
    """
    for i in word:
        if ord(i) > 122:
            return False
    return True


def map_subject_name(subject, bylaw):
    """
        Parameters:
            subject: string for subject name
            bylaw: list of all subject in database

        Return:
            string with the correct name of subject as it was saved in database
    """
    if check_language(subject):
        subjects_encoder = map_subjects(bylaw)
        subject = map_letters(subject)
        similarity = cosine_similarity([subject], subjects_encoder)
        return bylaw[np.argmax(similarity)]

    return 'بعد أذنك دخل أسم المادة بالأنجليزى'
