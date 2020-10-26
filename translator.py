from bs4 import BeautifulSoup
import requests
import sys

user_agent = 'Mozilla/5.0'
translator = {1: 'Arabic', 2: 'German', 3: 'English', 4: 'Spanish', 5: 'French', 6: 'Hebrew', 7: 'Japanese',
              8: 'Dutch', 9: 'Polish', 10: 'Portuguese', 11: 'Romanian', 12: 'Russian', 13: 'Turkish'}
sentences = []
file = open('hello.txt', 'w+', encoding='utf-8')
try:
    s = requests.session()
except requests.exceptions.ConnectionError:
    print('Something wrong with your internet connection')
    exit()


def url_generator(choice_one, choice_two, word):
    word = word.replace(' ', '+')
    choice_one = translator[choice_one]
    choice_two = translator[choice_two]
    return f'https://context.reverso.net/translation/{choice_one.lower()}-{choice_two.lower()}/{word}'


def translations_and_examples(choice, stat='not all'):
    # Translations
    file.write(f'{translator[choice]} translations:')
    for index, j in enumerate(soup.find_all('a', attrs={'class': 'translation'})):
        if (index == 2 and stat == 'all') or (index == 6 and stat == 'not all'):
            break
        if index != 0:  # skip the first: Translation
            j = j.text.strip()
            file.write('\n' + j + '\n')
    # Examples
    file.write(f'\n{translator[choice]} examples:\n')
    k = soup.find('section', attrs={'id': 'examples-content'})
    for x in k.find_all('span', attrs={'class': 'text'}):
        temp = x.text.strip()
        if (len(sentences) > 1 and stat == 'all') or (len(sentences) > 9 and stat == 'not all'):
            break
        else:
            sentences.append(temp)
    for i in range(len(sentences)):
        if i % 2 == 1:  # odd index
            file.write(f'{sentences[i]}\n\n\n')
        else:
            file.write(f'{sentences[i]}:\n')
    # check error
    if sentences:
        file.seek(0)
        print(file.read())
    else:
        global word
        print(f'Sorry, unable to find {word}')
        exit()


def command_processor(line):
    c1 = line[1].capitalize()
    c2 = line[2].capitalize()
    if c2 == 'All':
        c2 = 0
    for index, language in translator.items():
        if c1 == language:
            c1 = index
        if c2 == language:
            c2 = index
    return c1, c2, ''.join(line[3:])


if sys.argv:
    args = sys.argv
    choice_1, choice_2, word = command_processor(args)
else:
    # prints menu
    print("Hello, you're welcome to the translator. Translator supports: ")
    for i in translator:
        print(f'{i}. {translator[i]}')

    # record user's choice
    choice_1 = int(input('Type the number of your language:\n'))
    choice_2 = int(input("Type the number of a language you want to translate to or '0' to translate to all languages:\n"))
    word = input('Type the word you want to translate:\n')

if choice_2 == 0:
    for x in range(1, 14):
        if x != choice_1:
            r = s.get(url_generator(choice_1, x, word), headers={'User-Agent': user_agent})
            """if r.status_code:
                print(f'{r.status_code} OK\n')"""
            src = r.content
            soup = BeautifulSoup(src, 'lxml')
            translations_and_examples(x, 'all')
            sentences = []
elif isinstance(choice_2, str):
    print(f"Sorry, the program doesn't support {choice_2}")
    exit()
else:
    r = s.get(url_generator(choice_1, choice_2, word), headers={'User-Agent': user_agent})
    src = r.content
    soup = BeautifulSoup(src, 'lxml')
    translations_and_examples(choice_2)
file.close()
