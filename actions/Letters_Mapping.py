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

    aliases = {
    "ml" : "theoretical foundations of machine learning",
    "ir" : "information retrieval",
    "ds" : "data structures",
    "algo": "algorithms analysis and design",
    "se 1": "introduction to software engineering",
    "se 2": "introduction to software engineering 2",
    "se1": "introduction to software engineering",
    "se2": "introduction to software engineering 2",
    "os" : "operating systems",
    "nlp": 'processing of formal and natural languages',
    "rl" : "reinforcement learning",
    "gans": "generative adversarial networks",
    "gan": "generative adversarial networks",
    "bci": "brain computer interfacing",
    "arc": "computer organization and architecture",
    "signals": "signals and systems"
    }


    if not check_language(subject):
        return 'بعد أذنك دخل أسم المادة بالأنجليزى'
    
    # if the user typed the alias of the subject
    if subject.lower() in aliases.keys():
        return aliases[subject.lower()]

        
    subjects_encoder = map_subjects(bylaw)
    subject = map_letters(subject)
    similarity = cosine_similarity([subject], subjects_encoder)

    print(bylaw[np.argmax(similarity)])
    print(np.max(similarity))
    print(similarity)

    # If cosine < Threshold "0.7" Then there is no subjects similar to input subject
    if np.max(similarity) < 0.7 :
        biggest_indices = similarity[0].argsort()[-3:][::-1]
        return " ولا \n".join( [bylaw[index] for index in biggest_indices ]) 
        
    return bylaw[np.argmax(similarity)]
