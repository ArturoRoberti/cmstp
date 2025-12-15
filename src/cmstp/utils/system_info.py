import inspect
import platform
import subprocess
from typing import Optional, TypedDict

import distro


class SystemInfo(TypedDict):
    """Detailed information about the host operating system."""

    # fmt: off
    type:              str
    kernel:            str
    name:              Optional[str]
    codename:          Optional[str]
    version_dot:       Optional[str]
    version_nodot:     Optional[str]
    arch:              str
    simulate_hardware: bool
    manufacturer:      str
    # fmt: on


def get_architecture() -> str:
    """
    Retrieve the system architecture using dpkg.

    :return: System architecture string
    :rtype: str
    """
    result = subprocess.run(
        ["dpkg", "--print-architecture"],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Failed to retrieve architecture info via dpkg: {result.stderr.strip()}"
        )
    else:
        return result.stdout.strip().lower()


# TODO: Test if this works without having to install "dmidecode" first (via apt) on a fresh system
def get_manufacturer() -> str:
    """
    Retrieve the system manufacturer using dmidecode.

    :return: System manufacturer string
    :rtype: str
    """
    result = subprocess.run(
        ["sudo", "dmidecode", "-s", "system-manufacturer"],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Failed to retrieve manufacturer info via dmidecode: {result.stderr.strip()}"
        )
    else:
        return result.stdout.strip().lower()


def get_system_info() -> SystemInfo:
    """
    Retrieve detailed information about the host system.

    :return: System information dictionary
    :rtype: SystemInfo
    """

    def is_current_test(test_name: str) -> bool:
        """
        Checks if the current execution context is within a specific pytest test function.

        :param test_name: Name of the pytest test function
        :type test_name: str
        :return: True if running inside the specified test function, False otherwise
        :rtype: bool
        """
        for frame_info in inspect.stack():
            func = frame_info.function
            # Typical pytest test functions start with "test_"
            if func.startswith("test_"):
                return func == test_name
        return False

    system_info = SystemInfo()
    # linux, darwin, etc.
    system_info["type"] = platform.system().lower()
    # x86_64, aarch64, etc.
    system_info["kernel"] = platform.machine()
    # Simulate Hardware (e.g. GPU)
    system_info["simulate_hardware"] = is_current_test(
        "test_hardware_specific"
    )
    if system_info["type"] == "linux":
        # ubuntu, debian, etc.
        system_info["name"] = distro.id().lower()
        # focal, jammy, buster, bullseye, etc.
        system_info["codename"] = distro.codename().lower()
        # 20.04, 22.04, etc.
        system_info["version_dot"] = distro.version()
        # 2004, 2204, etc.
        system_info["version_nodot"] = distro.version().replace(".", "")
        # amd64, arm64, etc.
        system_info["arch"] = get_architecture()
        # manufacturer
        system_info["manufacturer"] = get_manufacturer()
    else:
        # Unsupported OS
        system_info["name"] = None
        system_info["codename"] = None
        system_info["version_dot"] = None
        system_info["version_nodot"] = None
        system_info["arch"] = None
        system_info["manufacturer"] = None

    return system_info
