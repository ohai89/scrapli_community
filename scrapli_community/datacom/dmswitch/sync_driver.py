"""scrapli_community.datacom.dmswitch.sync_driver"""
from typing import Any

from scrapli.driver import NetworkDriver


def default_sync_on_open(conn: NetworkDriver) -> None:
    """
    Datacom datacom_dmswitch on_open callable

    Args:
        conn: NetworkDriver object

    Returns:
        N/A

    Raises:
        N/A
    """
    conn.acquire_priv(desired_priv=conn.default_desired_privilege_level)
    conn.send_command(command="configure")
    conn.send_command(command="no terminal paging")
    conn.send_command(command="exit")


def default_sync_on_close(conn: NetworkDriver) -> None:
    """
    datacom_dmswitch default on_close callable

    Args:
        conn: NetworkDriver object

    Returns:
        N/A

    Raises:
        N/A

    """
    conn.acquire_priv(desired_priv=conn.default_desired_privilege_level)
    conn.channel.write(channel_input="exit")
    conn.channel.send_return()


class DatacomDmSwitchDriver(NetworkDriver):
    def __init__(self, **kwargs: Any) -> None:
        """
        Datacom dmswitch platform class

        Args:
            kwargs: keyword args

        Returns:
            N/A

        Raises:
            N/A

        """
        # *if* using anything but system transport pop out ptyprocess transport options, leaving
        # anything else
        transport_plugin = kwargs.get("transport", "system")
        if transport_plugin != "system":
            kwargs.get("transport_options", {}).pop("ptyprocess", None)

        super().__init__(**kwargs)
