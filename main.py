import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import pandas as pd
from pathlib import Path
from evaluators import *

folder = "ImagesTest"
rows = []

for image_path in Path(folder).glob("*"):

    image_path = str(image_path)

    blur = evaluate_blur(image_path)
    lighting = evaluate_lighting(image_path)
    pose = evaluate_pose(image_path)
    eyes = evaluate_eyes(image_path)

    row = {
        "image": Path(image_path).name,

        **blur,
        **lighting,
        **pose,
        **eyes
    }

    rows.append(row)


df = pd.DataFrame(rows)
df.to_csv("Results/final_scores.csv", index=False)

print("CSV saved successfully")