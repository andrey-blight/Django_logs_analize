import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from reports.HandlersReportStrategy import HandlersReportStrategy


def test_file_parsing():
    data = HandlersReportStrategy()._parse_file("logs/app1.log")

    assert data == {
        '/api/v1/reviews/': {'INFO': 5, 'WARNING': 2, 'ERROR': 0, 'DEBUG': 1, 'CRITICAL': 0},
        '/admin/dashboard/': {'INFO': 6, 'WARNING': 1, 'ERROR': 2, 'DEBUG': 6, 'CRITICAL': 1},
        '/api/v1/users/': {'INFO': 4, 'WARNING': 1, 'ERROR': 0, 'DEBUG': 2, 'CRITICAL': 0},
        '/api/v1/cart/': {'INFO': 3, 'WARNING': 1, 'ERROR': 0, 'DEBUG': 2, 'CRITICAL': 2},
        '/api/v1/products/': {'INFO': 3, 'WARNING': 0, 'ERROR': 0, 'DEBUG': 0, 'CRITICAL': 0},
        '/api/v1/support/': {'INFO': 1, 'WARNING': 1, 'ERROR': 3, 'DEBUG': 1, 'CRITICAL': 1},
        '/api/v1/auth/login/': {'INFO': 4, 'WARNING': 3, 'ERROR': 1, 'DEBUG': 1, 'CRITICAL': 1},
        '/admin/login/': {'INFO': 5, 'WARNING': 1, 'ERROR': 1, 'DEBUG': 0, 'CRITICAL': 0},
        '/api/v1/checkout/': {'INFO': 6, 'WARNING': 0, 'ERROR': 1, 'DEBUG': 3, 'CRITICAL': 1},
        '/api/v1/payments/': {'INFO': 7, 'WARNING': 2, 'ERROR': 1, 'DEBUG': 2, 'CRITICAL': 0},
        '/api/v1/orders/': {'INFO': 2, 'WARNING': 1, 'ERROR': 2, 'DEBUG': 2, 'CRITICAL': 0},
        '/api/v1/shipping/': {'INFO': 2, 'WARNING': 0, 'ERROR': 1, 'DEBUG': 1, 'CRITICAL': 0}}


def test_merging():
    first = {"/user": {"DEBUG": 0, "INFO": 1, "WARNING": 0, "ERROR": 2, "CRITICAL": 0}}
    second = {"/user": {"DEBUG": 1, "INFO": 3, "WARNING": 0, "ERROR": 0, "CRITICAL": 0},
              "/login": {"DEBUG": 0, "INFO": 1, "WARNING": 0, "ERROR": 2, "CRITICAL": 0}}
    HandlersReportStrategy()._merge(first, second)

    assert first == {"/user": {"DEBUG": 1, "INFO": 4, "WARNING": 0, "ERROR": 2, "CRITICAL": 0},
                     "/login": {"DEBUG": 0, "INFO": 1, "WARNING": 0, "ERROR": 2, "CRITICAL": 0}}

    assert second == {"/user": {"DEBUG": 1, "INFO": 3, "WARNING": 0, "ERROR": 0, "CRITICAL": 0},
                      "/login": {"DEBUG": 0, "INFO": 1, "WARNING": 0, "ERROR": 2, "CRITICAL": 0}}


def test_stringify():
    data = {"/user": {"DEBUG": 1, "INFO": 3, "WARNING": 0, "ERROR": 0, "CRITICAL": 0},
            "/login": {"DEBUG": 0, "INFO": 1, "WARNING": 0, "ERROR": 2, "CRITICAL": 0}}
    table = HandlersReportStrategy()._stringify(data)

    assert table == ('HANDLERS REPORT\n'
                     'TOTAL: 7\n'
                     'HANDLERS            \tCRITICAL            \tDEBUG               \t'
                     'ERROR               \tINFO                \tWARNING             \n'
                     '/login              \t0                   \t0                   \t'
                     '2                   \t1                   \t0                   \n'
                     '/user               \t0                   \t1                   \t'
                     '0                   \t3                   \t0                   ')


def test_all_work():
    table = HandlersReportStrategy().generate_report(
        ["logs/app1.log", "logs/app2.log", "logs/app3.log"])

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