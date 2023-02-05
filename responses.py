from enum import Enum
import logging

from scripts.ChampionData import ChampionData


class Commands(Enum):
    BASE = "lolcomp"
    HELP = "help"
    CHALLENGES = "challenges"
    CHAMP = "champ"


challenges_text = """
`lolcomp challenges [challenge name]` to see available champions for a particular challenge.
"""


help_text = """    
Commands:

`lolcomp`
 Base command. Works as a help command if no second argument is passed, or bad argument
 
`lolcomp help` 
reads out available commands

`lolcomp champ [champion]`
lists all helpful info for building teamcomp for this particular champion

`lolcomp challenges`
lists out the available challenges you could play

`lolcomp challenges [challenge]`
list out valid champoins and number of champions required
    """


logging.basicConfig(level=logging.DEBUG)


def challenges_response():
    challenges = ChampionData.get_all_challenges()
    challenges_list = ""

    for challenge in challenges:
        challenges_list += f"{challenge}\n"

    return challenges_text + "\n" + challenges_list


def challenge_response(challenge_name):
    challenge_info = ChampionData.challenges_info[challenge_name]
    if not challenge_info:
        return f"""
        invalid argument {challenge_name}
        """

    champ_string_list = ""
    champ_string_list += f"Challenge: {challenge_name.title()}\n"
    champ_string_list += f"Required champions: {challenge_info['required_champ_count']}/5\n"
    # champ_string_list += f"Number of required champs: "
    for champ in challenge_info["champs"]:
        champ_string_list += f"{champ[0]}\n"
    logging.debug(champ_string_list)

    return champ_string_list


def champ_challenges_response(champ_name):
    champ = ChampionData.get_champ_by_name(champ_name)
    if champ is None:
        return f"no champ with name {champ_name}. misspelled?"

    challenges = ChampionData.challenges_info

    challenges_list = []
    for key, value in challenges.items():
        if champ[value["index"]] == "TRUE":
            challenges_list.append(key.title())

    champion_challenges_string = f"champion: {champ_name.title()}\n"
    champion_challenges_string += "available challenges: \n"
    champion_challenges_string += "\n".join(challenges_list)

    return champion_challenges_string


