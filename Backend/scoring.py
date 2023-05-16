import random
import re

sentence_ending_punc = ["'", '"', "!", "?", "."]
bad_responses = ["http://", "https://", "http://en.wikipedia.org/wiki/List_of_burn_centers_in_the_United_States"]


def check_bad_response(answer, score):
    for br in bad_responses:
        if answer == br:
            score -= 10
    return score


def check_messedup_link(answer, score):
    badlinks = re.findall(r'\[.*?\]\s?\(', answer)
    goodlinks = re.findall(r'\[.*?\]\s?\(.*?\)', answer)
    if len(badlinks) > len(goodlinks):
        return score - 3
    else:
        return score


def remove_punctuation(txt):
    for punc in punctuation:
        txt = txt.replace(punc, '')
    return txt


def check_ends_in_equals(answer, score):
    if answer[-1] == "=":
        score -= 3
    return score


def check_unknown_token(answer, score):
    if "<unk>" in answer:
        score -= 4
    return score


def check_similarity(question, answer, score):
    question = remove_punctuation(question)
    answer = remove_punctuation(answer)

    if question == answer:
        return score - 4

    if answer in question or question in answer:
        return score - 3

    return score


def check_ends_in_punctuation(answer, score):
    end_in_punc = any(answer[-1] == punc for punc in sentence_ending_punc)

    if end_in_punc:
        return score + 1

    return score


def check_answer_echo(answer, score):
    answer = remove_punctuation(answer)
    tokenized = answer.split(' ')

    toklen = len(tokenized)
    repeats = 0
    for token in tokenized:
        if tokenized.count(token) > 1:
            repeats += 1

    pct = float(repeats) / float(toklen)
    if pct == 1.0:
        score -= 5
    elif pct >= 0.75:
        score -= 4

    return score


def check_answer_echo_question(question, answer, score):
    answer = remove_punctuation(answer)
    question = remove_punctuation(question)

    ans_tokenized = answer.split(' ')
    que_tokenized = question.split(' ')

    toklen = len(ans_tokenized)

    if toklen == 1:
        return score

    repeats = 0
    for token in ans_tokenized:
        if que_tokenized.count(token) > 0:
            repeats += 1

    pct = float(repeats) / float(toklen)
    if pct == 1.0:
        score -= 5
    elif pct >= 0.75:
        score -= 4

    return score


def score_answer(question, answer, score):
    score = check_similarity(question, answer, score)
    score = check_ends_in_punctuation(answer, score)
    score = check_answer_echo(answer, score)
    score = check_answer_echo_question(question, answer, score)
    score = check_ends_in_equals(answer, score)
    score = check_unknown_token(answer, score)
    score = check_messedup_link(answer, score)
    score = check_bad_response(answer, score)
    return score


if __name__ == '__main__':
    name = 'full_some_questions-81k.out'

    with open(name, 'r', encoding='utf8') as f:
        contents = f.read().split("\n\n\n")
        for content in contents
            batches = content.split(">>>")

            ans_score = {}

            for idx, batch in enumerate(batches[1:]):
                question, answer = batch.split('\n')[0], batch.split('\n')[1].split('::: ')[1]
                score = float(batch.split('\n')[1].split(' ::: ')[0])

                score = score_answer(question, answer, score)

                ans_score[answer] = score

            scores = [v for k, v in ans_score.items()]
            max_score = max(scores)
            options = [k for k, v in ans_score.items() if v == max_score]
            choice_answer = random.choice(options)

            print(30 * "_")
            print('> ', question)
            print(choice_answer)
            print(30 * "_")
