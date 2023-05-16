import html
import regex as re
from setup.settings import preprocessing

protected_phrases_regex = []
with open(preprocessing['protected_phrases_file'], 'r', encoding='utf-8') as protected_file:
    protected_phrases_regex = list(filter(lambda word: False if word[0] == '#' else True, filter(None, protected_file.read().split("\n"))))

matched_regexes = []
unmatched_regexes = []
phrase = ''
for protected_phrase_regex in protected_phrases_regex:
    matched_regex = re.search(r'\(\?:\^\|\\s\)\(\?i:\((.*?) \?\\.\)\)', protected_phrase_regex)
    if matched_regex:
        matched_regexes.append(matched_regex.group(1))
    else:
        unmatched_regexes.append(protected_phrase_regex)
if protected_phrase_regex:
    phrase = ('(?:^|\s)(?i:((?:{}) ?\.))'.format('|'.join(matched_regexes)) if matched_regexes else '') \
             + ('|(?:' + (')|(?:'.join(unmatched_regexes)) + ')' if unmatched_regexes else '')

regex = {
    'special': re.compile(r'[\x00-\x1f]+'),
    'protected': re.compile(phrase),
    'periods': re.compile('\.{2,}'),
    'separate': re.compile(r'([^\w\s\.])'),
    'digits': re.compile(r'([\d])'),
    'joined': re.compile(r'[^\w\d_]'),
    'spaces': re.compile(r'\s+'),
    'restorephrases': re.compile(r'PROTECTEDREGEXPHRASE([\d\s]+?)PROTECTEDREGEXPHRASE'),
    'restoreperiods': re.compile(r'PROTECTEDPERIODS([\d\s]+?)PROTECTEDPERIODS'),
}

protected_phrases_replace = []
protected_phrases_counter = 0

def tokenize(sentence):
    global protected_phrases_replace, protected_phrases_counter, regex
    protected_phrases_replace = []
    protected_phrases_counter = 0
    protected_periods_counter = 0

    sentence = sentence.replace('<unk>', '').replace('<s>', '').replace('</s>', '')
    sentence = html.unescape(sentence)
    sentence = sentence.strip()
    sentence = regex['special'].sub('', sentence)

    if regex['protected'].search(sentence):
        sentence = regex['protected'].sub(replace, sentence)

    m = regex['periods'].findall(sentence)
    if m:
        protected_periods_counter += 1
        for dots in list(set(m)):
            sentence = sentence.replace(dots, ' PROTECTEDPERIODS{}PROTECTEDPERIODS '.format(len(dots)))

    sentence = sentence.replace('`', '\'').replace('\'\'', '"')
    sentence = regex['separate'].sub(r' \1 ', sentence)
    sentence = regex['digits'].sub(' \\1 ', sentence)
    words = sentence.split()
    sentence = []

    for word in words:
        if word[-1] == '.':
            m = word.rstrip('.')
            if '.' in m and regex['joined'].search(m):
                pass
            else:
                word = m + ' .'

        sentence.append(word)

    sentence = " ".join(sentence)
    sentence = sentence.strip()
    sentence = regex['spaces'].sub(' ', sentence)

    if protected_phrases_counter:
        sentence = regex['restorephrases'].sub(lambda number: protected_phrases_replace[int(number.group(1).replace(" ", ""))], sentence)
    if protected_periods_counter:
        sentence = regex['restoreperiods'].sub(lambda number: ("." * int(number.group(1).replace(" ", ""))), sentence)

    return sentence

def replace(entity):
    global protected_phrases_replace, protected_phrases_counter
    phrase = list(filter(None, list(entity.groups())))[0]
    replacement = entity.group(0).replace(phrase, ' PROTECTEDREGEXPHRASE{}PROTECTEDREGEXPHRASE '.format(protected_phrases_counter))
    protected_phrases_replace.append(phrase)
    protected_phrases_counter += 1
    return replacement

answers_detokenize_regex = None

with open(preprocessing['answers_detokenize_file'], 'r', encoding='utf-8') as answers_detokenize_file:
    answers_detokenize_regex = list(filter(lambda word: False if word[0] == '#' else True, filter(None, answers_detokenize_file.read().split("\n"))))

def detokenize(answers):
    detokenized_answers = []

    for answer in answers:
        for detokenize_regex in answers_detokenize_regex:
            difference = 0

            if re.search(detokenize_regex, answer):
                regex = re.compile(detokenize_regex)
                for p in regex.finditer(answer):
                    if len(p.groups()) > 1:
                        groups = p.groups()[1:]
                        for i, group in enumerate(groups):
                            position = p.start(i+2) + (i) * 22
                            answer = answer[:position] + answer[position:].replace(" ", "##DONOTTOUCHTHISSPACE##", 1)
                        detokenize_regex = detokenize_regex.replace(' ', '(?: |##DONOTTOUCHTHISSPACE##)')
                
                regex = re.compile(detokenize_regex)
                for p in regex.finditer(answer):
                    replace_from = p.groups()[0]
                    replace_to = p.groups()[0].replace(" ", "")
                    position = p.start(1) + difference
                    difference += -len(replace_from) + len(replace_to)
                    answer = answer[:position] + answer[position:].replace(replace_from, replace_to, 1)

        answer = answer.replace("##DONOTTOUCHTHISSPACE##", ' ')
        detokenized_answers.append(answer)

    return detokenized_answers

# Run the tests
init()

for test in tests:
    detokenized_answers = detokenize([test[0]])
    print('[{}]  {}  ->  {}{}'.format(Fore.GREEN + 'PASS' + Fore.RESET if detokenized_answers[0] == test[1] else Fore.RED + 'FAIL' + Fore.RESET, test[0], test[1], '' if detokenized_answers[0] == test[1] else '  Result: {}'.format(detokenized_answers[0])))

