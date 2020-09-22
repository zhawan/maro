# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""
This script is used to debug distributed algorithm in single host multi-process mode.
"""

import io
import os
import yaml

from maro.utils import convert_dottable


with io.open("config.yml", "r") as in_file:
    raw_config = yaml.safe_load(in_file)
    config = convert_dottable(raw_config)


learner_path = "components/dist_learner.py &"
actor_path = "components/dist_actor.py &"

for l_num in range(config.distributed.learner.peer["actor_worker"]):
    os.system(f"python " + learner_path)

for a_num in range(config.distributed.actor.peer["actor"]):
    os.system(f"python " + actor_path)
