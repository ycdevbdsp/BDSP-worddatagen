# BDSP-worddatagen
 Generates a wordDataArray for use in english BDSP message files

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
 