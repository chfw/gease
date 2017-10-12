import re


class UriTemplate(object):

    def __init__(self, url_template_string):
        self.__s = url_template_string
        self.__variables = extract_variables(self.__s)
        for v in self.__variables:
            self.__dict__[v] = None

    def variables(self):
        return self.__variables

    def get_template_string(self):
        return self.__s

    def __call__(self, **keywords):
        for key, value in keywords.items():
            if key in self.__variables:
                self.__dict__[key] = value
        return self.__str__()

    def __str__(self):
        templated = self.__s.format(**self.__get_dict())
        return templated

    def __get_dict(self):
        a_new_dict = {}
        for v in self.__variables:
            if self.__dict__[v]:
                a_new_dict['/' + v] = '/' + self.__dict__[v]
            else:
                a_new_dict['/' + v] = '{/' + v + '}'
        return a_new_dict


def extract_variables(url_template_string):
    results = re.findall('\{/([^}]+)\}', url_template_string)
    return results


def is_partial(url_template_string):
    return True if extract_variables(url_template_string) else False
