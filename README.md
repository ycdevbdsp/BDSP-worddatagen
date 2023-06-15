# BDSP-worddatagen
 Generates a wordDataArray for use in english BDSP message files

A GUI tool to edit and add dialog to BDSP.

Supports DSPRE formatters:

\f
\r
\n

\n is very strange in the context of BDSP due to how the dialog processing works. Internally, \n is treated like a \r. I would strongly encourage just using \f and \r for your dialog flow instead.

Message preview window at the bottom of the UI shows you how the message will be formatted and shown in game. Currently does not allow for custom font editing (size, colors, etc).

Supports filtering messages by the speaker (e.g. filter just Professor Rowan's messages). Requires MsgWindowData.json and english_dlp_speakers_name.json in "input" folder. (not provided)

Supports the following commercial font for preview if available: https://fontworks.co.jp/fontsearch/udkakugoc80pro-m/?word=UD%20Kakugo_Condensation%2080%20M


![image](https://github.com/ycdevbdsp/BDSP-worddatagen/assets/56665250/092b4af1-58e6-456b-a6d0-da91b9ab503b)


Setting font color of individual dialog strings is technically possible using a standard HTML <color> tag. The vanilla game tends to put the <color> tags on their own line, and you'll see that throughout as you look at messages.
You can globally set the font color of all messages, excluding the color tags that are already set in messages (such as Rowan referring to the Pokedex in text), using the "Set All Color" button and selecting a color from the picker. Once you make this global setting, you won't be able to globally change the color (yet). Keep a copy of the original message without global color settings should you wish to change the color more than once. Again, you can still technically change the color individually with the text editor though it's cumbersome to do so right now and I don't have immediate intent to improve that capability.

It reads message json files from the "input" folder, and lists the messages within in the "Messages" window in the top right. Clicking a message in this list will populate the Message Contents window at the bottom. Give your message a label in the New Message Label field. It's not necessary if you're replacing a message, and has no impact on a replaced message.

Writing in the New Message window and clicking Replace will overwrite the selected message. Clicking Add will add it to the selected message json input. Save your changes with the Save button - this generates a new json file in the "output" folder with your changes.

The table on the right lists out all messages in the selected file "at a glance", and the filter field just underneath it allows you to quickly search for messages with a given keyword. Selecting the message from the table will select it in the Messages list and populate the contents for quick editing.

The "Adventure Notes" button opens a secondary form that allows editing Guidebook entries specifically. They're treated a little differently from standard dialog, and a request was made to split that out to allow for adding/editing Guidebook entries.

![image](https://github.com/ycdevbdsp/BDSP-worddatagen/assets/56665250/69e5512c-d9de-4eec-b9fb-e23d4a59e1e6)

I recommend launching the tool from a command shell as a result so any crash exceptions can be preserved. Feel free to DM me on twitter @ycdev_lum

**Full Changelog**: https://github.com/ycdevbdsp/BDSP-worddatagen/compare/beta...beta

# Example
 input: Excuse me, are you a Trainer?\nYou are? Lovely!\nI have several fossils here that some of my colleagues have collected from the tunnels underground.\nThere's a machine in Oreburgh's museum that can revive the Pokémon in these fossils.\nWould you be willing to take the fossils over there? They'll know what to do.
 
 
 result:
 
 {
 
    "wordDataArray": [
    
        {
        
            "patternID": 7,
            "eventID": 1,
            "tagIndex": -1,
            "tagValue": 0.0,
            "str": "Excuse me, are you a Trainer? ",
            "strWidth": 343.53125
        },
        {
            "patternID": 7,
            "eventID": 1,
            "tagIndex": -1,
            "tagValue": 0.0,
            "str": "You are? Lovely! ",
            "strWidth": 199.046875
        },
        {
            "patternID": 7,
            "eventID": 1,
            "tagIndex": -1,
            "tagValue": 0.0,
            "str": "I have several fossils here that some of my ",
            "strWidth": 475.953125
        },
        {
            "patternID": 7,
            "eventID": 3,
            "tagIndex": -1,
            "tagValue": 0.0,
            "str": "colleagues have collected from the tunnels ",
            "strWidth": 510.9375
        },
        {
            "patternID": 7,
            "eventID": 3,
            "tagIndex": -1,
            "tagValue": 0.0,
            "str": "underground. ",
            "strWidth": 173.40625
        },
        {
            "patternID": 7,
            "eventID": 1,
            "tagIndex": -1,
            "tagValue": 0.0,
            "str": "There’s a machine in Oreburgh’s museum that can ",
            "strWidth": 584.3125
        },
        {
            "patternID": 7,
            "eventID": 3,
            "tagIndex": -1,
            "tagValue": 0.0,
            "str": "revive the Pokémon in these fossils. ",
            "strWidth": 415.65625
        },
        {
            "patternID": 7,
            "eventID": 1,
            "tagIndex": -1,
            "tagValue": 0.0,
            "str": "Would you be willing to take the fossils over there? ",
            "strWidth": 589.453125
        },
        {
            "patternID": 7,
            "eventID": 7,
            "tagIndex": -1,
            "tagValue": 0.0,
            "str": "They’ll know what to do. ",
            "strWidth": 285.078125
        }
    ]
 }
 
