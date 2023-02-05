import csv
import os
import logging
from enum import Enum
from dotenv import load_dotenv


load_dotenv()
data_path = os.getenv("DATA_PATH")


class ChampionDataClass:
    def __init__(self, csv_path):
        self.champ_indexes = {}
        self.challenges_indexes = {}
        self.challenges_info = {}
        self.fields = []
        self.rows = []

        with open(csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            self.fields = next(csv_reader)

            for row in csv_reader:
                self.rows.append(row)

        self._set_champ_indexes()
        self._set_challenges_indexes()
        self._set_challenges_info()

    def _set_champ_indexes(self):
        logging.info("init champion indexes")
        for index, champion in enumerate(self.rows):
            self.champ_indexes.update({champion[0]: index})

    def _set_challenges_indexes(self):
        logging.info("init challenge indexes")
        challenges = self.get_all_challenges()
        for index, item in enumerate(challenges):
            challenges[index] = item.lower()

        for index, field in enumerate(self.fields):
            if challenges.count(field.lower()) > 0:
                self.challenges_indexes.update({field.lower(): index})

    def _set_challenges_info(self):
        for current_challenge in self.challenges_indexes:
            self.challenges_info.update({
                current_challenge: {
                    "index": self.challenges_indexes[current_challenge],
                    "required_champ_count": 5 if self.challenges_indexes[current_challenge] > 17 else 3,
                    "champs":  self.get_champs_by_challenge(current_challenge)
                }
            })


    # [0] is name column of champions
    # [1:12] is 3/5 champs needed
    # [12:18] is champion roles
    # [18: 31] need 5/5 champs to fulfill requirement
    # [31:] is the champions valid lanes/roles

    def get_all_champ_names(self):
        names_list = []
        for champ in self.champ_indexes:
            names_list.apppend(champ[0])

        return names_list

    def get_champ_by_name(self, name: str):
        capital_name = name.title()
        if not capital_name in self.champ_indexes.keys():
            return None
        return self.rows[self.champ_indexes[capital_name]]

    def get_champs_by_challenge(self, challenge_name):
        challenges = self.challenges_indexes.keys()

        if not challenge_name in challenges:
            return

        col_index = self.challenges_indexes[challenge_name]

        champion_list = []
        for row in self.rows:
            if row[col_index] == "TRUE":
                champion_list.append(row)
        return champion_list

    def get_all_challenges(self):
        challenges_list = []
        challenges_list += self.fields[1:12]
        challenges_list += self.fields[18:31]

        return challenges_list


# This is the main export of this file
ChampionData = ChampionDataClass(data_path)

