import re
from setup.settings import preprocessing


def load_blacklist(filename):
    blacklist = []
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.read().split("\n")
        for line in lines:
            if line and not line.startswith('#'):
                blacklist.append(line)
    return blacklist


def score_answers(answers, blacklist):
    scores = []
    for answer in answers:
        if '<unk>' in answer:
            scores.append(-1)
        elif any(re.search(regex, answer) for regex in blacklist):
            scores.append(0)
        else:
            scores.append(1)
    return scores


def load_replace(filename):
    replace = []
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.read().split("\n")
        for line in lines:
            if line and not line.startswith('#'):
                replace.append(line.split('##->##'))
    return replace


def replace_in_answers(answers, replace):
    replaced_answers = []
    for answer in answers:
        for replace_from, replace_to in replace:
            answer = re.sub(replace_from, replace_to, answer)
        replaced_answers.append(answer)
    return replaced_answers


answers_blacklist = load_blacklist(preprocessing['answers_blacklist_file'])
vocab_blacklist = load_blacklist(preprocessing['vocab_blacklist_file'])

answers_replace = load_replace(preprocessing['answers_replace_file'])
vocab_replace = load_replace(preprocessing['vocab_replace_file'])

def score_answers(answers, blacklist):
    scores = []
    for answer in answers:
        if '<unk>' in answer:
            scores.append(-1)
        elif any(re.search(regex, answer) for regex in blacklist):
            scores.append(0)
        else:
            scores.append(1)
    return scores

def replace_in_answers(answers, replace):
    replaced_answers = []
    for answer in answers:
        for replace_from, replace_to in replace:
            answer = re.sub(replace_from, replace_to, answer)
        replaced_answers.append(answer)
    return replaced_answers
