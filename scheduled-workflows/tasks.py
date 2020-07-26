import json
import os
from contextlib import contextmanager
from datetime import datetime

from invoke import task

last_updated = datetime.now().utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
main_repo = '/glade/collections/cmip/catalog/intake-esm-datastore'


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


@task
def build(c):
    with chdir(f'{main_repo}/builders'):

        catalog_path = '../catalogs/glade-cmip6.csv.gz'
        command = f'git pull origin master && source activate esm-catalog-builder && python cmip.py --root-path /glade/collections/cmip/CMIP6 --pick-latest-version --cmip-version 6 --csv-filepath {catalog_path} --depth 4'
        c.run(command)

        command = f'git diff --text {catalog_path} 2>/dev/null | wc -l'
        output = c.run(command).stdout
        if int(output) > 0:
            with open('../catalogs/glade-cmip6.json', 'rw') as f:
                data = json.load(f)
                data['last_updated'] = last_updated
                json.dump(data, f)


@task(build)
def update(c):
    with chdir(main_repo):
        commit_message = f'Scheduled CMIP6 catalog update: {last_updated}'
        cmd = 'source activate base && git add catalogs && pre-commit run'
        try:
            c.run(cmd)
        except Exception:
            pass

        cmd = f"git add catalogs && git commit -m '{commit_message}' && git push"
        c.run(cmd)
