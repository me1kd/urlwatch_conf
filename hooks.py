#
# Example hooks file for urlwatch
#
# Copyright (c) 2008-2019 Thomas Perl <m@thp.io>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import re

from urlwatch import filters
from urlwatch import jobs
from urlwatch import reporters

import json
from jsonpath_rw import jsonpath, parse


#class CustomLoginJob(jobs.UrlJob):
#    """Custom login for my webpage"""
#
#    __kind__ = 'custom-login'
#    __required__ = ('username', 'password')
#
#    def retrieve(self, job_state):
#        return 'Would log in to {} with {} and {}\n'.format(self.url, self.username, self.password)


#class CaseFilter(filters.FilterBase):
#    """Custom filter for changing case, needs to be selected manually"""
#
#    __kind__ = 'case'
#
#    def filter(self, data, subfilter=None):
#        # The subfilter is specified using a colon, for example the "case"
#        # filter here can be specified as "case:upper" and "case:lower"
#
#        if subfilter is None:
#            subfilter = 'upper'
#
#        if subfilter == 'upper':
#            return data.upper()
#        elif subfilter == 'lower':
#            return data.lower()
#        else:
#            raise ValueError('Unknown case subfilter: %r' % (subfilter,))


#class IndentFilter(filters.FilterBase):
#    """Custom filter for indenting, needs to be selected manually"""
#
#    __kind__ = 'indent'
#
#    def filter(self, data, subfilter=None):
#        # The subfilter here is a number of characters to indent
#
#        if subfilter is None:
#            indent = 8
#        else:
#            indent = int(subfilter)
#
#        return '\n'.join((' '*indent) + line for line in data.splitlines())



class CustomMatchUrlFilter(filters.AutoMatchFilter):
    # The AutoMatchFilter will apply automatically to all filters
    # that have the given properties set
    MATCH = {'url': 'http://example.org/'}

    def filter(self, data):
        return data.replace('foo', 'bar')

class CustomRegexMatchUrlFilter(filters.RegexMatchFilter):
    # Similar to AutoMatchFilter
    MATCH = {'url': re.compile('http://example.org/.*')}

    def filter(self, data):
        return data.replace('foo', 'bar')


class CustomTextFileReporter(reporters.TextReporter):
    """Custom reporter that writes the text-only report to a file"""

    __kind__ = 'custom_file'

    def submit(self):
        with open(self.config['filename'], 'w') as fp:
            fp.write('\n'.join(super().submit()))


class CustomHtmlFileReporter(reporters.HtmlReporter):
    """Custom reporter that writes the HTML report to a file"""

    __kind__ = 'custom_html'

    def submit(self):
        with open(self.config['filename'], 'w') as fp:
            fp.write('\n'.join(super().submit()))

class RegexFindall(filters.FilterBase):
    """Match text with regular expressions using Python's re.match"""

    __kind__ = 're.findall'

    def filter(self, data, subfilter=None):
        if subfilter is None:
            raise ValueError('{} needs a subfilter'.format(self.__kind__))

        # Allow for just specifying a regular expression
        if isinstance(subfilter, str):
            subfilter = {'pattern': subfilter}

        return re.findall(subfilter.get('pattern'), data)[0]

class JsonPath_two(filters.FilterBase):
    """Query Json based on jsonpath_rw"""

    __kind__ = 'jsonpath.two'

    def filter(self, data, subfilter=None):
        if subfilter is None:
            raise ValueError('{} needs a subfilter'.format(self.__kind__))

        # Allow for just specifying a jsonpath_rw query expression
        if isinstance(subfilter, str):
            subfilter = {'pattern': subfilter}

        jsonpath_expr = parse(subfilter.get('pattern'))
        object_json = json.loads(data)
        lResult = [match.value for match in jsonpath_expr.find(object_json)]
        lResult = [ x+' '+y for x,y in zip(lResult[0::2], lResult[1::2]) ]
        lResult.sort()
        sResult = '\n'.join([i for i in lResult[1:]])

        return sResult
