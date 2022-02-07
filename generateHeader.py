"""
Example Header for English:
{
      "labelIndex": 0,
      "arrayIndex": 0,
      "labelName": "0-msg_c04_chanpion_01_1",
      "styleInfo": {
        "styleIndex": 0,
        "colorIndex": -1,
        "fontSize": 54,
        "maxWidth": 1080,
        "controlID": 0
      },
      "attributeValueArray": [
        -1,
        0,
        0,
        -1,
        0
      ],
      "tagDataArray": [],
      "wordDataArray": [
        {
          "patternID": 7,
          "eventID": 1,
          "tagIndex": -1,
          "tagValue": 0.0,
          "str": "Oh, is that a Pokédex? You must be helping",
          "strWidth": 571.0625
        },
        {
          "patternID": 7,
          "eventID": 3,
          "tagIndex": -1,
          "tagValue": 0.0,
          "str": "Professor Rowan.",
          "strWidth": 220.71875
        },
        {
          "patternID": 7,
          "eventID": 3,
          "tagIndex": -1,
          "tagValue": 0.0,
          "str": "What’s your name?",
          "strWidth": 248.046875
        },
        {
          "patternID": 7,
          "eventID": 7,
          "tagIndex": -1,
          "tagValue": 0.0,
          "str": "...",
          "strWidth": 23.71875
        }
      ]
    },
"""

from textwrap import indent
import rapidjson


def addHeader(message, label):
    
    header = {
      "labelIndex": "CHANGE_BEFORE_IMPORT",
      "arrayIndex": "CHANGE_BEFORE_IMPORT",
      "labelName": "CHANGE_BEFORE_IMPORT",
      "styleInfo": {
        "styleIndex": 0,
        "colorIndex": -1,
        "fontSize": 54,
        "maxWidth": 1080,
        "controlID": 0
      },
      "attributeValueArray": [
        -1,
        0,
        0,
        -1,
        0
      ],
      "tagDataArray": [],
      "wordDataArray": []
    }
    
    header["labelName"] = label
    header["wordDataArray"] = message["wordDataArray"]
    
    return rapidjson.dumps(header, indent=4, ensure_ascii=False)