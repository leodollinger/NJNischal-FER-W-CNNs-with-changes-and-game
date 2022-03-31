import os
import json

class Rules:
    def __init__(self):

        self.emotions = {"Angry": 0, "Disgust": 0, "Fear": 0, "Happy": 0, "Neutral": 0, "Sad": 0, "Surprised": 0}
        self.emotions_set = [['Angry', 'Disgust', 'Sad'], ['Neutral'], ['Happy', 'Fear', 'Surprised']]
        with open('curr_rules.json') as json_file:
            curr_rules = json.load(json_file)

        with open('default_rules.json') as json_file:
            default_rules = json.load(json_file)

        if not os.path.exists('output_emotions.txt'):
            self.rule_set = default_rules
        else:
            self.rule_set = curr_rules
            group_match = self.analize_output_expression()
            self.genarate_rules(group_match)

            new_config_json = json.dumps(self.rule_set, indent=4)
            # Writing to sample.json
            with open("curr_rules.json", "w") as outfile:
                outfile.write(new_config_json)

    def analize_output_expression(self):
        with open('output_emotions.txt') as f:
            lines = f.readlines()
        for line in lines:
            self.emotions[line.replace("\n", "")] += 1
        self.emotions = sorted(self.emotions.items(), key=lambda x: x[1], reverse=True)
        max = self.emotions[0]
        med = self.emotions[1]
        min = self.emotions[2]
        group_match = {'A': 0, 'B': 0, 'C': 0}

        for i, emotion_set in enumerate(self.emotions_set):
            key = 'A' if i == 0 else ('B' if i == 1 else 'C')
            if max[0] in emotion_set:
                group_match[key] += 1
            if med[0] in emotion_set:
                group_match[key] += 1
            if min[0] in emotion_set:
                group_match[key] += 1

        return sorted(group_match.items(), key=lambda x: x[1], reverse=True)

    def genarate_rules(self, group_match):
        # difficulty up
        if group_match[0][1] == group_match[1][1] and group_match[1][1] == group_match[2][1]:
            if self.rule_set['ball']['radius'] > self.rule_set['ball']['min_radius'] and self.rule_set['ball']['speed'] < self.rule_set['ball']['max_speed']:
                if self.rule_set['ball']['radius'] <= 10 and self.rule_set['ball']['speed'] >= 10:
                    self.rule_set['ball']['radius'] -= 1
                    self.rule_set['ball']['speed'] += 2
                else:
                    self.rule_set['ball']['radius'] -= 2
                    self.rule_set['ball']['speed'] += 1

            if self.rule_set['paddle']['width'] > self.rule_set['paddle']['min_width'] and self.rule_set['paddle']['speed'] > self.rule_set['paddle']['min_speed']:
                if self.rule_set['paddle']['width'] <= 80 and self.rule_set['paddle']['speed'] <= 10:
                    self.rule_set['paddle']['width'] -= 10
                    self.rule_set['paddle']['speed'] -= 1
                else:
                    self.rule_set['paddle']['width'] -= 4
                    self.rule_set['paddle']['speed'] -= 18

        # difficulty up
        elif group_match[0][0] == 'A':
            if self.rule_set['ball']['radius'] < self.rule_set['ball']['max_radius'] and self.rule_set['ball']['speed'] > self.rule_set['ball']['min_speed']:
                if self.rule_set['ball']['radius'] >= 10 and self.rule_set['ball']['speed'] <= 10:
                    self.rule_set['ball']['radius'] += 2
                    self.rule_set['ball']['speed'] -= 1
                else:
                    self.rule_set['ball']['radius'] += 1
                    self.rule_set['ball']['speed'] -= 2

            if self.rule_set['paddle']['width'] < self.rule_set['paddle']['max_width'] and self.rule_set['paddle']['speed'] < self.rule_set['paddle']['max_speed']:
                if self.rule_set['paddle']['width'] >= 80 and self.rule_set['paddle']['speed'] >= 10:
                    self.rule_set['paddle']['width'] += 4
                    self.rule_set['paddle']['speed'] += 18
                else:
                    self.rule_set['paddle']['width'] += 10
                    self.rule_set['paddle']['speed'] += 1
        # difficulty kept
        # else:
        #     pass


# if __name__ == '__main__':
#     rules = Rules()