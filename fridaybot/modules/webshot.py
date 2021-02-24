"""Take screenshot of any website
Syntax: .screencapture <Website URL>"""


import io

import requests

from fridaybot import CMD_HELP
from fridaybot.utils import friday_on_cmd


@friday.on(friday_on_cmd("screencapture (.*)"))
async def _(event):

    if event.fwd_from:

        return

    if Config.SCREEN_SHOT_LAYER_ACCESS_KEY is None:

        await friday.tr_engine(event, 
            "Need to get an API key from https://screenshotlayer.com/product \nModule stopping!"
        )

        return

    await friday.tr_engine(event, "Processing ...")

    sample_url = "https://api.screenshotlayer.com/api/capture?access_key={}&url={}&fullpage={}&viewport={}&format={}&force={}"

    input_str = event.pattern_match.group(1)

    response_api = requests.get(
        sample_url.format(
            Config.SCREEN_SHOT_LAYER_ACCESS_KEY, input_str, "1", "2560x1440", "PNG", "1"
        )
    )

    # https://stackoverflow.com/a/23718458/4723940

    contentType = response_api.headers["content-type"]

    if "image" in contentType:

        with io.BytesIO(response_api.content) as screenshot_image:

            screenshot_image.name = "screencapture.png"

            try:

                await friday.send_file(
                    event.chat_id,
                    screenshot_image,
                    caption=input_str,
                    force_document=True,
                    reply_to=event.message.reply_to_msg_id,
                )

                await event.delete()

            except Exception as e:

                await friday.tr_engine(event, str(e))

    else:

        await friday.tr_engine(event, response_api.text)


CMD_HELP.update(
    {
        "webshot": "**Webshot**\
\n\n**Syntax : **`.screencapture <webpage link>`\
\n**Usage :** takes screenshot of webpage."
    }
)
