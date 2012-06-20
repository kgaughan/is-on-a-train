#
# isonatrain
# by Keith Gaughan <http://stereochro.me/>
#
# Copyright (c) Keith Gaughan, 2012
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""
A daemon that tracks the tweets of people on Twitter, generating HTML pages
bases on certain trigger phrases containing a matching piece of text.
"""


import os.path
import sys
from ConfigParser import RawConfigParser
from tweepy import api, StreamListener, Stream, BasicAuthHandler
from pystache import render


__version__ = '1.0.0'
__author__ = 'Keith Gaughan'
__email__ = 'k@stereochro.me'


USAGE = "Usage: %s <config>"


class Listener(StreamListener):

    __slots__ = ('templates', 'output', 'triggers')

    def __init__(self, templates, output, triggers):
        super(Listener, self).__init__()
        self.templates = templates
        self.output = output
        self.triggers = triggers

    def on_status(self, status):
        screen_name = status.user.screen_name
        if screen_name not in self.triggers:
            return
        text = status.text.lower()
        for trigger, message in self.triggers[screen_name].iteritems():
            if text.find(trigger) != -1:
                with open(self.output[screen_name], 'w+') as fh:
                    fh.write(render(self.templates[screen_name], message=message))
                    break


def get_user_ids(screen_names):
    return [user.id for user in api.lookup_users(screen_names=screen_names)]

def read_config(parser):
    auth = dict((k, parser.get('auth', k)) for k in ('username', 'password'))
    templates = dict(parser.items('templates'))
    output = dict(parser.items('output'))
    if sorted(templates.keys()) != sorted(output.keys()):
        raise Exception('Templates and output locations must have same keys.')
    triggers = {}
    for section in parser.sections():
        if section.startswith('@'):
            screen_name = section[1:]
            if screen_name not in output:
                continue
            triggers[screen_name] = dict(parser.items(section))
    if sorted(output.keys()) != sorted(triggers.keys()):
        raise Exception('Must have a trigger section per output location.')
    return auth, templates, output, triggers

def load_templates(template_paths):
    templates = {}
    for name, path in template_paths.iteritems():
        with open(path, 'r') as fh:
            templates[name] = fh.read()
    return templates

def tweak_paths(base, path_dict):
    result = {}
    for key, path in path_dict.iteritems():
        result[key] = os.path.join(base, path)
    return result

def main():
    if len(sys.argv) != 2:
        print >> sys.stderr, USAGE % os.path.basename(sys.argv[0])
        return 1

    parser = RawConfigParser()
    parser.read(sys.argv[1])
    auth, template_paths, output, triggers = read_config(parser)

    # Tweak the paths to make them relative to the config file.
    base = os.path.dirname(sys.argv[1])
    template_paths = tweak_paths(base, template_paths)
    output = tweak_paths(base, output)

    templates = load_templates(template_paths)

    stream = Stream(
            BasicAuthHandler(auth['username'], auth['password']),
            Listener(templates, output, triggers),
            secure=True)
    try:
        stream.filter(follow=get_user_ids(triggers.keys()))
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    sys.exit(main())
