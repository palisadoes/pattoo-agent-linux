import os
from pattoo_shared.installation import configure, shared
from pattoo_shared import files


def configure_daemon(daemon_name, config_dir, config_dict):
    config_file = configure.pattoo_config(
                                        daemon_name,
                                        config_dir,
                                        config_dict)

    configure.check_config(config_file, config_dict)


def install(daemon_list):
    """Start configuration process.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    if os.environ.get('PATTOO_CONFIGDIR') is None:
        os.environ['PATTOO_CONFIGDIR'] = '{0}etc{0}pattoo'.format(os.sep)
    config_dir = os.environ.get('PATTOO_CONFIGDIR')

    autonomousd_agent_dict = {
            'polling_interval': 300,
        }

    hubd_agent_dict = {
        'polling_interval': 300,
        'ip_targets': {
            'ip_address': '127:0.0.1',
            'ip_bind_port': 5000
        }
    }

    spoked_agent_dict = {
        'polling_interval': 300,
        'ip_listen_address': '127.0.0.1',
        'ip_bind_port': 5000
    }

    # Attempt to create configuration directory
    files.mkdir(config_dir)

    # Create the pattoo user and group
    configure.create_user('pattoo', '/nonexistent', ' /bin/false', True)

    # Attempt to change the ownership of the configuration directory
    shared.chown(config_dir)

    # Configure daemons in list regardless of order
    for daemon in daemon_list:
        # Configure autonomous agent
        if 'autonomousd' in daemon:
            configure_daemon(daemon, config_dir, autonomousd_agent_dict)

        # Configure spoked agent
        elif 'spoked' in daemon:
            configure_daemon(daemon, config_dir, spoked_agent_dict)

        # Convert hubd agents
        elif 'hubd' in daemon:
            configure_daemon(daemon, config_dir, hubd_agent_dict)

        else:
            continue
    # Done
