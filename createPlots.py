#! /usr/bin/env python

"""
Create plots of noise
Inputs
   csv -- input csv (after trimHeader.sh)
  yaml -- yaml file that has constants
  type -- True=Property line violation, False=75Feet violation
Outputs
   plots, tbd
"""

import sys
import altair as alt
import pandas as pd
import yaml
import numpy as np

print("1: " + sys.argv[1])
print("2: " + sys.argv[2])
print("3: " + sys.argv[3])

# print and save file that is used to create plot
print("Working on: " + sys.argv[1])
SOURCE_FILE = sys.argv[1]

# import yaml metadata from argv[2]
with open(sys.argv[2]) as f:
    doc = yaml.full_load(f)

# import trimmed csv from argv[1]
input_data = pd.read_csv(sys.argv[1])

# type of plot, propertyLine (True) or 75feet (False)?
TYPE = True if sys.argv[3] == "True" else False
if sys.argv[3] == "True":
    TYPE = True
elif sys.argv[3] == "False":
    TYPE = False
else:
    TYPE = "NA"

# import constants from yaml doc
if TYPE is True:
    NOISE_VIOLATION_THRESHOLD = doc["noisePropertyLineThreshold"]
elif TYPE is False:
    NOISE_VIOLATION_THRESHOLD = doc["noise75FeetThreshold"]
else:
    print("No type given as third argument, assuming property line")
    NOISE_VIOLATION_THRESHOLD = doc["noisePropertyLineThreshold"]
COLOR_SCALE = doc["colorScale"]
Y_SCALE_DOMAIN_MIN = doc["yScaleDomainMin"]
if TYPE is True:
    Y_SCALE_DOMAIN_MAX = doc["yScaleDomainMax"]
elif TYPE is False:
    Y_SCALE_DOMAIN_MAX = doc["yScaleDomainMax"] - doc["yScaleAdjust75Feet"]
else:
    print("No type given as third argument, assuming property line")
    Y_SCALE_DOMAIN_MAX = doc["yScaleDomainMax"]
COLOR_SCALE_DOMAIN_MIN = doc["colorScaleDomainMin"]
COLOR_SCALE_DOMAIN_MAX = doc["colorScaleDomainMax"]
VIOLATION_T_MARK = doc["violationTFMark"][0]
VIOLATION_F_MARK = doc["violationTFMark"][1]

# change column names based on yaml doc
input_data.rename(columns=doc["columnNames"], inplace=True)

# create running timer
input_data["timing"] = input_data["time"].cumsum()

# create violation detection
input_data["violation"] = np.where(input_data["dBA"] > NOISE_VIOLATION_THRESHOLD , True, False)

# print
print(TYPE)
print(NOISE_VIOLATION_THRESHOLD)
print(Y_SCALE_DOMAIN_MAX)

# begin time series plot
baseChart = (
    alt.Chart(input_data)
    .mark_line(color="red")
    .encode(
        alt.X("timing", scale=alt.Scale(zero=False)),
        alt.Y(
            "dBA:Q",
            scale=alt.Scale(
                zero=False, domain=(Y_SCALE_DOMAIN_MIN, Y_SCALE_DOMAIN_MAX)
            ),
        ),
        alt.Tooltip(["dBA:Q"]),
        order="timing",
    )
    .properties(title=SOURCE_FILE)
)

point = baseChart.mark_point().encode(
    alt.X("timing", scale=alt.Scale(zero=False)),
    alt.Y(
        "dBA",
        scale=alt.Scale(zero=False, domain=(Y_SCALE_DOMAIN_MIN, Y_SCALE_DOMAIN_MAX)),
    ),
    alt.Color(
        "dBA",
        scale=alt.Scale(
            scheme="lightgreyred",
            domain=(COLOR_SCALE_DOMAIN_MIN, COLOR_SCALE_DOMAIN_MAX),
        ),
    ),
    alt.Shape(
        "violation",
        scale=alt.Scale(
            domain=(True, False), range=(VIOLATION_T_MARK, VIOLATION_F_MARK)
        ),
    ),
    order="timing",
)

# set up horizontal rule for law
noise_df = pd.DataFrame({"noise": [NOISE_VIOLATION_THRESHOLD]})
hline = alt.Chart(noise_df).mark_rule().encode(y="noise:Q")

plot_to_save = alt.layer(baseChart, point, hline)
out_name = sys.argv[1].replace(".csv_trimmed", "") + ".html"
print("Saving file: " + out_name)
plot_to_save.save(out_name)
