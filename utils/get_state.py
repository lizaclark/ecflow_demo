import sys
import os.path

import ecflow

from core.log import set_logger

# -------------------------------------------------------------------- #
def main():

    logger = set_logger(os.path.splitext(os.path.split(__file__)[-1])[0], 'INFO')

    """Print ECFLOW server state."""
    try:
        ci = ecflow.Client()
        # Get server definition by syncing with client defs.
        ci.sync_local()
        # Set print style to show state.
        ecflow.PrintStyle.set_style(ecflow.Style.STATE)
        # Print the returned state.
        logger.info(ci.get_defs())
    except RuntimeError:
        msg = ('Error in {}\n'.format(__file__)+
              'ecflow was not able to retrieve server state')
        if sys.version_info[0] != 3:
           import traceback
           msg += '\n\nOriginal traceback:\n' + traceback.format_exc()
        raise RuntimeError(msg)
    return
# -------------------------------------------------------------------- #

# -------------------------------------------------------------------- #
if __name__ == "__main__":
    main()
# -------------------------------------------------------------------- #
