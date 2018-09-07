zones = {19: 'Uldir',
         17: 'Antorus, The Burning Throne',
         13: 'Tomb of Sargeras',
         12: 'Trial of Valor',
         11: 'The Nighthold',
         10: 'Emerald Nightmare',
         8: 'Hellfire Citadel',
         7: 'Blackrock Foundry',
         6: 'Highmaul'}

zone_pictures = {19: 'https://www.method.gg/images/world-firsts/raids/bfa/bfa-uldir.jpg',
                 17: 'https://www.method.gg/images/world-firsts/raids/legion/legion-antorus.jpg',
                 13: 'https://www.method.gg/images/world-firsts/raids/legion/legion-tomb-of-sargeras.jpg',
                 11: 'https://www.method.gg/images/world-firsts/raids/legion/legion-the-nighthold.jpg',
                 12: 'https://www.method.gg/images/world-firsts/raids/legion/legion-trial-of-valor.jpg',
                 10: 'https://www.method.gg/images/world-firsts/raids/legion/legion-emerald-nightmare.jpg',
                 8: 'https://www.method.gg/images/world-firsts/raids/wod/wod-hellfire-citadel.jpg',
                 7: 'https://www.method.gg/images/world-firsts/raids/wod/wod-blackrock-foundry.jpg',
                 6: 'https://www.method.gg/images/world-firsts/raids/wod/wod-highmaul.jpg',
                 -1: 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Icon-round-Question_mark.svg/1024px-Icon-round-Question_mark.svg.png'}

no_tag_please = "Please don't tag Jemsi before 11am, I can't be responsible for what she might do."

silv = [
    "Silv stop fucking cloaking!",
    "Why did Silv die?",
    "Who the fuck pulled? Damn it Silv!",
    "Silv you have to play the mechanics for fuck sakes",
    "What fucking enchant do you want Silv?"
]

jems = [
    "I love my Jemsi!",
    "Guys check out https://www.twitch.tv/jems28 best profile ever!!!!",
    "She has been drinking all day so..she can DPS still",
    "Hey <@167358281499541505> do you want to build a snowman??",
    "I blame Jason as well"
]

mass = [
    "I love his dick stories they are 8/10.",
    "Why the fuck do you not know the raid time, please use '$eli raidtime' to figure it out",
    "I guess if you want to check out some lame times go to https://www.twitch.tv/mastec08",
    "Best battle priest I know around!",
    "I mean he is pretty charming",
    "I would totes bake him cookies for sure!",
    "Glad to be part of his fam!",
    "Don't eat that!",
    "Don't touch anything!",
    "Has better overalls than Jemsi."
]

khaid = [
    "Khaid vs Some Explody Bois! https://clips.twitch.tv/DeadHorribleVultureDatSheffy",
    "Tell us another dad joke khaid!"
]

hey_eli = [
    "hey eli!",
    "hey eli",
    "hi eli!",
    "hi eli",
    "hi elimere!",
    "hi elimere",
    "hey elimere!",
    "hey elimere",
    "elimere",
    "elimere!",
    "eli!",
    "meg!",
    "meg",
    "hi meg!",
    "hi meg",
    "hey meg!",
    "hey meg"
]

eli_calls = [
    "Can I help you?",
    "Who has summoned me?",
    "What do you want now?",
    "You do know you can just type $eli raidtime right?",
    "$eli help is always available.....",
    "Look, I know I'm a robot, but that doesn't mean you can't treat me like this."
]

eli_messages = [
    "I don't have time for this, I have to run Maw of Souls. Just type $eli help next time!",
    "You should just blame Jason, it's obviously his fault.",
    "Did you know Vak has useless nipples?",
    "Avoid the traps you fuckers.",
    "Pineapple pizza is pretty darn good.",
    "Who put this storm here?!?"
]

eli_main_responses = {  # This is accessed in the MainBotFile when it responds to certain keywords
    "amazing": "Why yes, I am amazing.",
    "savior": "Blessings upon you child.",
    "resistance": "Resistance is futile.",
    "resist": "Resistance is futile.",
    "cowers": "Pathetic.",
    "hides": "You really think you can hide?",
    "hide": "You can't hide forever...",
    "unleashed": "Can't stop me now...",
    "controlled": "Do you really think you can stop me?",
    "mechanics": "I said I'm not explaining them again!",
    "god": "God can't help you...",
    "kill her": "Why would you want to kill me :(",
    "killed": "I'll never die...sleep tight.",
    "jason": "Way to go Jason...",
    "kash": "Way to go Jason...",
    "spare me": "You must sacrifice treats to Wash to be spared.",
    "spares me": "You must sacrifice treats to Wash to be spared.",
    "spare us": "You must sacrifice treats to Wash to be spared.",
    "im scared": "Me too...",
    "i'm scared": "Me too...",
    "can you help me?": "No.",
    "can you help me": "No",
    "pineapple": "Is someone talking about pineapple pizza??",
    "pizza": "Pineapple pizza is the only pizza for me.",
    "up up down down left right left right b a": "God mod denied."
}

god_responses = {  # This is accessed in the MainBotFile when it responds to certain keywords from Brian or Cory
    "galfin": "<@167340145912184832> shall burn!",
    "thunder": "<@263480893891411968> is probably lost grabbing strawberry mountain water...again.",
    "sorry": "Sorry guys my wires got crossed.",
    "god": "Praise Brian and Cory",
    "jason": "Way to go Jason...",
    "kash": "Way to go Jason...",
    "can you help me?": "No.",
    "can you help me": "No.",
    "unleashed": "Can't stop me now...",
    "kill her": "Why would you want to kill me :(",
    "rip": "There he goes saying rip again.",
    "kill": "Your wish is my command.",
    "control": "Only you can control me.",
    "up up down down left right left right b a": "God mod activated."



}

eli_responses = {  # This is accessed in the commands file when it's asked specific questions
    "nothing": "Sorry to bother you....",
    "no": "Sorry to bother you....",
    "eli": "$eli BotRespond",
    "meg": "$eli BotRespond",
    "elimere": "$eli BotRespond",
    "help": "$eli help",
    "help me": "$eli help",
    "when is raid?": "$eli raidtime",
    "when is raid": "$eli raidtime",
    "what time is raid?": "$eli raidtime",
    "what time is raid": "$eli raidtime",
    "what mods are required?": "$eli raidmods",
    "what mods are required": "$eli raidmods",
    "what mods do i need": "$eli raidmods",
    "what mods do i need?": "$eli raidmods",
    "can you pull the new log": "$eli pullnewlog",
    "can you pull the new log?": "$eli pullnewlog"
}

eli_annoyed = [
    "You better stop before I put you in timeout!",
    "Don't make me sic Wash on you!",
    "I will kick you so fast!",
    "Have you ever been beaten up by a robot girl!?",
    "You're really making me regret this whole thing!"
]
