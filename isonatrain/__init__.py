import os.path
import sys
from ConfigParser import RawConfigParser
from tweepy import api, StreamListener, Stream, BasicAuthHandler
from pystache import render


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
        for trigger, message in self.triggers.iteritems():
            if text.find(trigger) != -1:
                with open(self.output[screen_name], 'w+') as fh:
                    fh.write(render(self.templates[screen_name], message=message))


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

def main(argv):
    if len(argv) != 2:
        print >> sys.stderr, "Syntax: %s <config>" % os.path.basename(argv[0])
        sys.exit(1)
    parser = RawConfigParser()
    parser.read(argv[1])
    auth, template_paths, output, triggers = read_config(parser)

    templates = load_templates(template_paths)

    stream = Stream(
            BasicAuthHandler(auth['username'], auth['password']),
            Listener(templates, output, triggers),
            secure=True)
    stream.filter(follow=get_user_ids(triggers.keys()))

if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        pass
