import os
import subprocess
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import main

NO_REPORT_OUTPUT = """Incorrect arguments
No report name
Usage: python3 main.py filename1 filename2 ... --report <report name>"""

NO_FILES_OUTPUT = """Incorrect arguments
No log files
Usage: python3 main.py filename1 filename2 ... --report <report name>"""

INCORRECT_FILE_OUTPUT = """Incorrect arguments
File 'logs/app1000.log' does not exist.
Usage: python3 main.py filename1 filename2 ... --report <report name>"""


def test_correct_args():
    result = subprocess.run(
        ['python3', 'src/main.py', 'logs/app1.log', 'logs/app2.log', '--report', 'handlers'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = result.stdout.decode().strip().split('\n')[0]
    assert result.returncode == 0
    assert output != "Incorrect arguments"


def test_not_specify_report():
    result = subprocess.run(
        ['python3', 'src/main.py', 'logs/app1.log', 'logs/app2.log', '--report'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = result.stdout.decode().strip()
    assert result.returncode == 1
    assert output == NO_REPORT_OUTPUT


def test_not_specify_report_at_all():
    result = subprocess.run(
        ['python3', 'src/main.py', 'logs/app1.log', 'logs/app2.log'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = result.stdout.decode().strip()
    assert result.returncode == 1
    assert output == NO_REPORT_OUTPUT


def test_not_specify_files():
    result = subprocess.run(
        ['python3', 'src/main.py', '--report', "handlers"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = result.stdout.decode().strip()
    assert result.returncode == 1
    assert output == NO_FILES_OUTPUT


def test_no_such_file():
    result = subprocess.run(
        ['python3', 'src/main.py', "logs/app1000.log", '--report', "handlers"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = result.stdout.decode().strip()
    assert result.returncode == 1
    assert output == INCORRECT_FILE_OUTPUT
