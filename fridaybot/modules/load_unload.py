from fridaybot.utils import friday_on_cmd, load_module, remove_plugin


@friday.on(friday_on_cmd(pattern="load ?(.*)", outgoing=True))
async def load(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match.group(1)
    try:
        try:
            remove_plugin(shortname)
        except:
            pass
        load_module(shortname)
        await friday.tr_engine(event, f"Successfully loaded {shortname}")
    except Exception as e:
        await friday.tr_engine(event, 
            f"Could not load {shortname} because of the following error.\n{str(e)}"
        )


@friday.on(friday_on_cmd(pattern="unload ?(.*)", outgoing=True))
async def unload(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match.group(1)
    try:
        remove_plugin(shortname)
        await friday.tr_engine(event, f"Unloaded {shortname} successfully")
    except Exception as e:
        await friday.tr_engine(event, 
            "Successfully unload {shortname}\n{}".format(shortname, str(e))
        )
