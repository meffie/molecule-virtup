"""Functional tests."""
import os
import yaml
from pathlib import Path
from contextlib import contextmanager

from click.testing import CliRunner
import pytest

from molecule.util import run_command

@contextmanager
def change_dir(path):
    prev = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev)

def test_molecule_init_role():
    """Verify that init role works."""
    cmd = ['molecule', 'init', 'role', 'myrole', '--driver-name', 'virtup']
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = run_command(cmd)
        assert result.returncode == 0

def test_molecule_init_scenario():
    """Verify that init role works."""
    cmd = ['molecule', 'init', 'scenario', 'default', '--driver-name', 'virtup']
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = run_command(cmd)
        assert result.returncode == 0

@pytest.mark.parametrize('scenario_to_test', ['local', 'remote'])
def test_molecule_scenario(scenario_to_test):
    basedir = Path(__file__).resolve().parent
    testdir = basedir / 'scenarios' / scenario_to_test
    with change_dir(testdir):
        result = run_command(['molecule', 'test'])
        assert result.returncode == 0

def test_molecule_external_options_file(tmp_path):
    logfile = tmp_path / 'myfile.log'
    optionsfile = tmp_path / 'options.yml'
    options = {
        'connection': 'local',
        'host': 'localhost',
        'logfile': str(logfile),
    }
    optionsfile.write_text(yaml.dump(options, explicit_start=True))
    env = os.environ.copy()
    env['VIRTUP_FILE'] = str(optionsfile)

    basedir = Path(__file__).resolve().parent
    testdir = basedir / 'scenarios' / 'local'
    with change_dir(testdir):
        result = run_command(['molecule', 'test'], env=env)
        assert result.returncode == 0
        assert logfile.exists()
