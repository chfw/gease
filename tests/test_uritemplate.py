from nose.tools import eq_

from gease.uritemplate import extract_variables
from gease.uritemplate import UriTemplate
from gease.uritemplate import is_partial


def test_extract_variables():
    url = '{/abc}{/dde}'
    variables = extract_variables(url)
    eq_(variables, ['abc', 'dde'])


def test_extract_variables_got_empty():
    url = ''
    variables = extract_variables(url)
    eq_(variables, [])


def test_uri_template_variable():
    template = UriTemplate('http://abc{/cute}')
    assert template.cute is None


def test_uri_template_template():
    template = UriTemplate('http://abc{/cute}')
    template.cute = 'world'
    eq_(str(template), 'http://abc/world')


def test_uri_template_template2():
    template = UriTemplate('http://abc{/cute}')
    eq_(template(cute='world'), 'http://abc/world')


def test_uri_template_partial_apply():
    template = UriTemplate('http://abc{/cute}{/left}')
    eq_(template(cute='world'), 'http://abc/world{/left}')


def test_is_partial():
    url = '{/abc}'
    assert is_partial(url) is True
