import json
import os
import re
import subprocess
from contextlib import contextmanager
from datetime import datetime

# import schedule


@contextmanager
def chdir(path):
    """Change working directory to `path` and restore it again
    This context manager is useful if `path` stops existing during your
    operations.
    """
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)


def stream_command(cmd, shell=False, no_newline_regexp='Progess'):
    """stream a command (yield) back to the user, as each line is available.
    # Example usage:
    results = []
    for line in stream_command(cmd):
        print(line, end="")
        results.append(line)
    Parameters
    ==========
    cmd: the command to send, should be a list for subprocess
    no_newline_regexp: the regular expression to determine skipping a
                       newline. Defaults to finding Progress

    """
    process = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE, universal_newlines=True)
    for line in iter(process.stdout.readline, ''):
        if not re.search(no_newline_regexp, line):
            yield line
    process.stdout.close()
    return_code = process.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def job():
    builder_dir = '/glade/collections/cmip/catalog/intake-esm-datastore/builders'
    with chdir(builder_dir):
        cmd = """git pull origin master && conda activate esm-catalog-builder &&
                  python cmip.py --root-path /glade/collections/cmip/CMIP6 \
                       --pick-latest-version \
                       --cmip-version 6 \
                        --csv-filepath ../catalogs/glade-cmip6.csv.gz \
                        --depth 4"""
        for line in stream_command(cmd, shell=True):
            print(line, end='')

        with open('../catalogs/glade-cmip6.json') as f:
            data = json.load(f)

        last_updated = datetime.now().utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        data['last_updated'] = last_updated

        with open('../catalogs/glade-cmip6.json', 'w') as f:
            json.dump(data, f)

    with chdir('/glade/collections/cmip/catalog/intake-esm-datastore/catalogs'):
        commit_message = f'Scheduled CMIP6 catalog update: {last_updated}'
        cmd = 'source activate base && git add . && pre-commit run'
        try:
            for line in stream_command(cmd, shell=True):
                print(line, end='')
        except subprocess.CalledProcessError:
            pass
        cmd = f"git add . && git commit -m '{commit_message}' && git push"
        for line in stream_command(cmd, shell=True):
            print(line, end='')


# schedule.every(3).days.at('04:45').do(job)

# while True:
#    schedule.run_pending()
#    time.sleep(1)

if __name__ == '__main__':
    job()
