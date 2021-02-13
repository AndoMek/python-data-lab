#!/usr/bin/env python3

import argparse
import os
import shlex
import sys


def parse_build_args(filename):
    filename = os.path.expandvars(filename)
    filename = os.path.expanduser(filename)

    with open(filename, "rt") as fp:
        for line_no, line in enumerate(fp, start=1):
            line = line.strip()
            if len(line) == 0:
                continue

            yield line


def gen_command(command, args=None, kw: dict = None):
    """
    Args:
        command: Command path / name
        args: List of command argument
        kw: Dictionary(map) command key-value arguments

    Features key-values:
        One letter key convert to -key otherwise --key
        For None value argument skipped
        For boolean value and True than argument insert only --key-name
        For list/tuple value with same key created all values into list/tuple

    Examples:
        >>> gen_command("echo", args=["Test", ])
        'echo Test'
        >>> gen_command("echo", args=['Test "Escaped" Command', ])
        'echo \\'Test "Escaped" Command\\''
        >>> gen_command("cmd", kw={"i": True, "j": False, "key": "Value with whitespaces", "no-value": None})
        "cmd -i --key 'Value with whitespaces'"
        >>> gen_command("cmd", kw={"list-val": [1, 2, 3], })
        'cmd --list-val 1 --list-val 2 --list-val 3'

    Returns:
        String shell command (POSIX escaped)
    """
    args = args or []
    kw = kw or {}
    cmd = command + " "

    # shlex.join method released in python version 3.8
    for arg in args:
        cmd += shlex.quote(str(arg))

    for k, v in kw.items():
        if v is None:
            continue
        key = ("--%s" if len(k) > 1 else "-%s") % k

        if isinstance(v, bool):
            if v is False:
                continue
            cmd += " %s" % key
        elif isinstance(v, (list, tuple)):
            for item in v:
                cmd += " %s %s" % (key, shlex.quote(str(item)))
        else:
            cmd += " %s %s" % (key, shlex.quote(str(v)))

    return cmd.strip()


def main():
    parser = argparse.ArgumentParser(description="Python Docker Build Helper")
    parser.add_argument(
        "__path",
        type=str,
        help="Docker Context",
        metavar="PATH | URL | -"
    )
    parser.add_argument(
        "--add-host",
        type=str,
        default=[],
        action="append",
        help="Add a custom host-to-IP mapping (host:ip)",
        metavar="list"
    )
    parser.add_argument(
        "--build-arg",
        type=str,
        default=[],
        action="append",
        help="Set build-time variables",
        metavar="list"
    )
    parser.add_argument(
        "--cache-from",
        type=str,
        help="Images to consider as cache sources",
        metavar="strings"
    )
    parser.add_argument(
        "--cgroup-parent",
        type=str,
        help="Optional parent cgroup for the container",
        metavar="string"
    )
    parser.add_argument(
        "--compress",
        action="store_true",
        help="Compress the build context using gzip"
    )
    parser.add_argument(
        "--cpu-period",
        type=int,
        help="Limit the CPU CFS (Completely Fair Scheduler) period",
        metavar="int"
    )
    parser.add_argument(
        "--cpu-quota",
        type=int,
        help="Limit the CPU CFS (Completely Fair Scheduler) quota",
        metavar="int"
    )
    parser.add_argument(
        "-c", "--cpu-shares",
        type=int,
        help="CPU shares (relative weight)",
        metavar="int"
    )
    parser.add_argument(
        "--cpuset-cpus",
        type=str,
        help="CPUs in which to allow execution (0-3, 0,1)",
        metavar="string"
    )
    parser.add_argument(
        "--cpuset-mems",
        type=str,
        help="MEMs in which to allow execution (0-3, 0,1)",
        metavar="string"
    )
    parser.add_argument(
        "--disable-content-trust",
        action="store_true",
        help="Skip image verification (default true)"
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Name of the Dockerfile (Default is 'PATH/Dockerfile')",
        metavar="string"
    )
    parser.add_argument(
        "--force-rm",
        action="store_true",
        help="Always remove intermediate containers"
    )
    parser.add_argument(
        "--iidfile",
        type=str,
        help="Write the image ID to the file",
        metavar="string"
    )
    parser.add_argument(
        "--isolation",
        type=str,
        help="Container isolation technology",
        metavar="string"
    )
    parser.add_argument(
        "--label",
        type=str,
        default=[],
        action="append",
        help="Set metadata for an image",
        metavar="list"
    )
    parser.add_argument(
        "-m", "--memory",
        type=int,
        help="Memory limit",
        metavar="bytes"
    )
    parser.add_argument(
        "--memory-swap",
        type=int,
        help="Swap limit equal to memory plus swap: '-1' to enable unlimited swap",
        metavar="bytes"
    )
    parser.add_argument(
        "--network",
        type=str,
        help='Set the networking mode for the RUN instructions during build (default "default")',
        metavar="string"
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Do not use cache when building the image"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output destination (format: type=local,dest=path)",
        metavar="stringArray"
    )
    parser.add_argument(
        "--platform",
        type=str,
        help="Set platform if server is multi-platform capable",
        metavar="string"
    )
    parser.add_argument(
        "--progress",
        type=str,
        help='Set type of progress output (auto, plain, tty). Use plain to show container output (default "auto")',
        metavar="string"
    )
    parser.add_argument(
        "--pull",
        action="store_true",
        help="Always attempt to pull a newer version of the image"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress the build output and print image ID on success"
    )
    parser.add_argument(
        "--rm",
        action="store_true",
        help="Remove intermediate containers after a successful build (default true)"
    )
    parser.add_argument(
        "--secret",
        type=str,
        help="Secret file to expose to the build (only if BuildKit enabled): id=mysecret,src=/local/secret",
        metavar="stringArray"
    )
    parser.add_argument(
        "--security-opt",
        type=str,
        help="Security options",
        metavar="strings"
    )
    parser.add_argument(
        "--shm-size",
        type=int,
        help="Size of /dev/shm",
        metavar="bytes"
    )
    parser.add_argument(
        "--squash",
        action="store_true",
        help="Squash newly built layers into a single new layer"
    )
    parser.add_argument(
        "--ssh",
        type=str,
        help="SSH agent socket or keys to expose to the build (only if BuildKit enabled)"
             " (format: default|<id>[=<socket>|<key>[,<key>]])",
        metavar="stringArray"
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Stream attaches to server to negotiate build context"
    )
    parser.add_argument(
        "-t", "--tag",
        type=str,
        default=[],
        action="append",
        help="Name and optionally a tag in the 'name:tag' format",
        metavar="list"
    )
    parser.add_argument(
        "--target",
        type=str,
        help="Set the target build stage to build.",
        metavar="string"
    )
    parser.add_argument(
        "--ulimit",
        type=str,
        help="Ulimit options (default [])",
        metavar="ulimit"
    )
    parser.add_argument(
        "--build-arg-file",
        type=str,
        default=[],
        action="append",
        help="Read in a file of build-time variables",
        metavar="list"
    )

    cmd_args = parser.parse_args()
    positional_args = [
        getattr(cmd_args, key) for key in vars(cmd_args) if key.startswith("__")
    ]
    keyword_args = {
        key.replace("_", "-"): getattr(cmd_args, key) for key in vars(cmd_args) if not key.startswith("__")
    }

    for file in keyword_args.pop("build-arg-file"):
        keyword_args["build-arg"].extend(
            list(parse_build_args(file))
        )

    return gen_command(
        "docker build",
        args=positional_args,
        kw=keyword_args
    )


if __name__ == "__main__":
    print(main(), file=sys.stdout, end="")
