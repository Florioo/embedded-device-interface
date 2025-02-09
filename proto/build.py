import os
import subprocess
import click
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent

PROTO_DIR = SCRIPT_DIR / "interface.proto"
NANOPB_DIR = SCRIPT_DIR / "nanopb.proto"

PY_OUTPUT_DIR = ROOT_DIR / "client_python" / "src" / "device_api" / "generated"
C_OUTPUT_DIR = ROOT_DIR / "server_c" / "generated"

DOC_DIR = os.path.join(ROOT_DIR, "doc/gen")
os.makedirs(DOC_DIR, exist_ok=True)


def run_command(cmd: str):
    print(f"\n{cmd}\n")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise Exception(f"Failed to run command: {cmd}")


def replace_in_file(file_path: str, old: str, new: str):
    with open(file_path, "r") as file:
        data = file.read()

    data = data.replace(old, new)

    with open(file_path, "w") as file:
        file.write(data)


@click.group()
def cli():
    pass


# @cli.command()
def generate_python():
    run_command(
        f"protoc -I={SCRIPT_DIR} --python_out={PY_OUTPUT_DIR} --pyi_out={PY_OUTPUT_DIR} {PROTO_DIR}"
    )
    run_command(
        f"protoc -I={SCRIPT_DIR} --python_out={PY_OUTPUT_DIR} --pyi_out={PY_OUTPUT_DIR} {NANOPB_DIR}"
    )

    file_name = PROTO_DIR.name.replace(".proto", "_pb2.py")
    # Fix file imports
    replace_in_file(
        file_path=PY_OUTPUT_DIR / file_name,
        old="import nanopb_pb2 as nanopb__pb2",
        new="from . import nanopb_pb2",
    )


# @cli.command()
def generate_c():
    run_command(f"nanopb_generator -I {SCRIPT_DIR} -D {C_OUTPUT_DIR} {PROTO_DIR}")


if __name__ == "__main__":
    # Run geneate c by default
    generate_python()
    generate_c()
