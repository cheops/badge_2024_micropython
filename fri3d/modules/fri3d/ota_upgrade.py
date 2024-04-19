
def confirm_boot():
    "confirm succesfull boot after (ota) update"
    try:
        from ota.rollback import cancel
        cancel()
    except Exception as e:
        log.debug(f"Failed confirming boot: {e=}")
