import os
import argparse
import shutil

from webdav import client as webdav

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


ROOT_DIR = os.environ.get('WEBDAV_BACKUPER_ROOT_DIR') or '/backup'


class PathList(argparse._StoreAction):

    def __call__(self, *args, **kwargs):
        args = list(args)
        args[2] = map(self._clean_path, args[2])
        result = super(PathList, self).__call__(*args, **kwargs)
        return result

    def _clean_path(self, path):
        path = os.path.abspath(path)
        path = path.lstrip('/')
        path = os.path.join(ROOT_DIR, path)
        if not os.path.exists(path):
            raise argparse.ArgumentError(self, 'Local directory "%s" does not exist' % path)
        return path


cli_parser = argparse.ArgumentParser\
    ( description='Send files or directories to webdav server'
    , )
cli_parser.add_argument\
    ( 'source'
    , nargs='+'
    , action=PathList
    , help='Source directory'
    )
cli_parser.add_argument\
    ( 'destination'
    )
cli_parser.add_argument\
    ( '--config'
    , default=os.environ.get('WEBDAV_BACKUPER_CONFIG') or '/etc/webdav_backuper/config.ini'
    , help='path to config file'
    )
cli_parser.add_argument\
    ( '--clean'
    , action='store_true'
    , default=False
    , help='delete source files after complete'
    )
cli_parser.add_argument\
    ( '--daemon'
    , action='store_true'
    , default=False
    , help='delete source files after complete'
    )
cli_parser.add_argument\
    ( '--method'
    , default='upload_sync'
    , choices=['upload_sync', 'upload_async', 'push']
    , help='method of syncronisation'
    )


config_parser = configparser.SafeConfigParser()
CONFIG_PARSER_INFLECT_METHOD = \
    { 'backup':
      { 'daemon': 'getboolean'
      , 'clean': 'getboolean'
    } }


def prepare_args():
    cli_parser_args = cli_parser.parse_args()
    result =\
        { 'options': {}
        , 'backup': {}
        }

    # Get options from config file
    with open(cli_parser_args.config) as fp:
        config_parser.readfp(fp)
        for section in ('options', 'backup'):
            try:
                variables = dict(config_parser.items(section)).keys()
                for var in variables:
                    inflect_method = (CONFIG_PARSER_INFLECT_METHOD.get(section) or {}).get(var) or 'get'
                    result[section][var] = getattr(config_parser, inflect_method)(section, var)
            except configparser.NoSectionError:
                result[section] = {}

    # Get options from CL and override
    section = 'backup'
    for option in ('config', 'clean', 'daemon', 'source', 'destination', 'method'):
        try:
            result[section][option]
        except (IndexError, KeyError):
            result[section][option] = getattr(cli_parser_args, option, None)

    # Clean useless
    result['backup'].pop('config', None)

    return result


def ensure_dir(client, path):
    path = os.path.dirname(path)
    prev = '/'
    for d in path.split(os.path.sep):
        if prev:
            d = os.path.join(prev, d)
        try:
            if d != '/':
                client.mkdir(d)
            prev = d
        except Exception as e:
            pass
    # instead of check
    client.list(path)


def main():
    args = prepare_args()
    backup = args['backup']
    options = args['options']

    client = webdav.Client(options)
    for source in backup['source']:
        method_name = backup['method']
        method = getattr(client, method_name)
        ensure_dir(client, backup['destination'])
        if method_name in ('upload_sync', 'upload_sync'):
            method\
                ( local_path=source
                , remote_path=backup['destination']
                )
        else:
            method\
                ( local_directory=source
                , remote_directory=backup['destination']
                )

    if backup['clean']:
        for source in backup['source']:
            try:
                shutil.rmtree(source)
            except Exception as e:
                print e


if __name__ == '__main__':
    main()