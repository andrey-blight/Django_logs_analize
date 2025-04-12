import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ReportsManager import ReportsManager


def test_invalid_report(capsys):
    try:
        ReportsManager("not_existing_report",
                       ["logs/app1.log", "logs/app2.log", "logs/app3.log"]).get_report()
    except SystemExit as e:
        assert e.code == 1

    output = capsys.readouterr().out
    assert output == "Invalid report name\n"

def test_all_files(capsys):
    ReportsManager("handlers",
                   ["logs/app1.log", "logs/app2.log", "logs/app3.log"]).get_report()

    output = capsys.readouterr().out.split("\n")
    table = "\n".join(line for line in output if line)
    assert table == ('HANDLERS REPORT\n'
                     'TOTAL: 300\n'
                     'HANDLERS            \tCRITICAL            \tDEBUG               \t'
                     'ERROR               \tINFO                \tWARNING             \n'
                     '/admin/dashboard/   \t1                   \t9                   \t'
                     '4                   \t13                  \t2                   \n'
                     '/admin/login/       \t1                   \t1                   \t'
                     '4                   \t12                  \t4                   \n'
                     '/api/v1/auth/login/ \t2                   \t3                   \t'
                     '2                   \t12                  \t5                   \n'
                     '/api/v1/cart/       \t3                   \t5                   \t'
                     '1                   \t9                   \t2                   \n'
                     '/api/v1/checkout/   \t2                   \t6                   \t'
                     '4                   \t15                  \t8                   \n'
                     '/api/v1/orders/     \t1                   \t2                   \t'
                     '4                   \t10                  \t4                   \n'
                     '/api/v1/payments/   \t0                   \t2                   \t'
                     '2                   \t12                  \t4                   \n'
                     '/api/v1/products/   \t3                   \t4                   \t'
                     '5                   \t12                  \t4                   \n'
                     '/api/v1/reviews/    \t0                   \t8                   \t'
                     '4                   \t20                  \t8                   \n'
                     '/api/v1/shipping/   \t0                   \t1                   \t'
                     '3                   \t8                   \t0                   \n'
                     '/api/v1/support/    \t2                   \t5                   \t'
                     '4                   \t16                  \t5                   \n'
                     '/api/v1/users/      \t0                   \t4                   \t'
                     '3                   \t9                   \t1                   ')
