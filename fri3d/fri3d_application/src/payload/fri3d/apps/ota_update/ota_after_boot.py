import logging

logger = logging.getLogger('fri3d.ota_after_boot')

def confirm_boot():
    "confirm succesfull boot after (ota) update"
    try:
        from ota.rollback import cancel
        cancel()
    except Exception as e:
        logger.debug(f"Failed confirming boot: {e=}")