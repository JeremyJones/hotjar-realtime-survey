"""
Models for the load tester for the real-time surveys solution.
"""

from requests import post
from json import loads
from time import sleep
from random import choice
from gzip import open
from re import sub

namesgenders = []


def get_a_namegender() -> list:
    if not len(namesgenders):
        fo = open('names.csv.gz')

        for line in fo:
            if line[0] == '"': continue
            namesgenders.append(line)

    return {"name":''.join(['abcdefghijklmnopqrstuvwxyz'[choice(range(26))]
                            for _ in range(choice(range(4,7)))]),
            "gender": choice(['Male','Female'])}

    mine = choice(namesgenders)
    raise RuntimeError(mine)
    return None


class Surveyee():

    def __init__(self):
        self.base_url = 'http://hotjar.jerjones.me'

    def ret_post_content(self, path):
        return post('{base}{path}'.\
                    format(base=self.base_url,
                           path=path)).content.decode('ascii')

    def answer(self, postdata):
        return post(self.base_url + '/answer', postdata)

    def finalise(self):
        pass
    
    def random_go(self):
        self.questions = loads(self.ret_post_content('/questions'))
        self.id = loads(self.ret_post_content('/getIdentifier'))
       
        for q in self.questions.get('_items'):
            postdata = {"who": self.id.get('eui'),
                        "q": 'answer2question{id}'.format(id=q.get('id'))}
            
            sleep(choice(range(1,3)))
                
            question = q.get('question')

            if question == 'Name':
                self.ngen = get_a_namegender()
                postdata['a'] = self.ngen['name']

                self.answer(postdata)

            elif question == 'Email':
                postdata['a'] = 'loadtest{rand}@jerjones.me'.\
                                format(rand=choice(range(10000)))
                self.answer(postdata)

            elif question == 'Age':
                options = loads(q.get('answer_options'))
                postdata['a'] = choice(options)
                self.answer(postdata)

            elif question == 'About Me':
                postdata['a'] = 'I was always instantiated to work for Hotjar.'
                self.answer(postdata)

            elif question == 'Gender':
                postdata['a'] = self.ngen['gender']
                self.answer(postdata)

            elif question == 'Favourite Colours':
                cols = loads(q.get('answer_options'))
                for num_colors in range(choice(range(len(cols)))):
                    for cnum in range(num_colors):
                        postdata['a'] = choice(cols)
                        self.answer(postdata)
