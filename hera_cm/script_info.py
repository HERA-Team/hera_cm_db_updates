import argparse
from hera_mc import cm_utils


def get_arglist(args):
    arglist = []
    for arg in dir(args):
        if not arg.startswith('_'):
            arglist.append(arg)
    return arglist


def add_part_info():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--hpn", help="HERA part number", default=None)
    parser.add_argument("-r", "--rev", help="Revision of part", default="last")
    parser.add_argument("-c", "--comment", help="Comment on part", default=None)
    parser.add_argument("-l", "--reference", help="Library filename", default=None)
    parser.add_argument("-q", "--query", help="Set flag if wished to be queried", action="store_true")  # noqa
    parser.add_argument("--verbose", help="Turn verbose mode on.", action="store_true")
    cm_utils.add_date_time_args(parser)
    return parser


def add_part():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--hpn", help="HERA part number", default=None)
    parser.add_argument("-r", "--rev", help="Revision number of part", default=None)
    parser.add_argument("-t", "--hptype", help="HERA part type", default=None)
    parser.add_argument("-m", "--mfg", help="Manufacturers number for part", default=None)
    parser.add_argument("--disallow_restart", dest="allow_restart", action='store_false',
                        help="Flag to disallow restarting an " "existing and stopped part")
    cm_utils.add_date_time_args(parser)
    cm_utils.add_verbosity_args(parser)
    return parser


def stop_part():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--part", help="Part number", default=None)
    parser.add_argument("-r", "--rev", help="Revision", default=None)
    parser.add_argument("--allow_override", help="Flag to allow override of existing value.",
                        action="store_true")
    cm_utils.add_date_time_args(parser)
    return parser


def add_connection():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--uppart", help="Upstream part number", default=None)
    parser.add_argument("--uprev", help="Upstream part revision", default=None)
    parser.add_argument("--upport", help="Upstream output port", default=None)
    parser.add_argument("-d", "--dnpart", help="Downstream part number", default=None)
    parser.add_argument("--dnrev", help="Downstream part revision", default=None)
    parser.add_argument("--dnport", help="Downstream input port", default=None)
    cm_utils.add_date_time_args(parser)
    cm_utils.add_verbosity_args(parser)
    return parser


def stop_connection():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--uppart", help="Upstream part number", default=None)
    parser.add_argument("--uprev", help="Upstream part revision", default=None)
    parser.add_argument("--upport", help="Upstream output port", default=None)
    parser.add_argument("-d", "--dnpart", help="Downstream part number", default=None)
    parser.add_argument("--dnrev", help="Downstream part revision", default=None)
    parser.add_argument("--dnport", help="Downstream input port", default=None)
    cm_utils.add_date_time_args(parser)
    return parser


def update_apriori():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--hpn", help="HERA part number")
    parser.add_argument(
        "-s",
        "--status",
        help="New apriori status.",
        choices=[
            "dish_maintenance",
            "dish_ok",
            "RF_maintenance",
            "RF_ok",
            "digital_maintenance",
            "digital_ok",
            "calibration_maintenance",
            "calibration_ok",
            "calibration_triage",
        ],
    )
    cm_utils.add_date_time_args(parser)
    return parser
