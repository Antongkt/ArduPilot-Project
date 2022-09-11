## Automating attacks against SITL



This directory contains experimental scripts for testing attacks against the ArduPilot SITL framwork, and is part of my university project **"Evaluating Attack Consequences on AUVs".**

The files are used to  test different attacks against the drone sensors in an automated manner, for the purpose of evaluating their effects on the drone and how the framework responds.

Attacks are performed by modifying the data read by the drone, by injecting false data inside the sensor libraries. The goal is that for each mission file provided inside the `missions` directory and each attack specified, automated tests are run and log files are produced for analysis. 
We are interested in the following types of attacks:

- false data injection: original sensor data is modified (e.g. by adding a constant bias)
- replay attacks: sensor readings are captured and later replayed to the drone
- stall attacks: sensor readings are completely blocked for a specific time frame (similar to DoS attacks)

The sensors currently affected are the accelerometer and gyroscope, but more might be tested in the future (e.g. GPS attacks).

Credit for the original version of `run-tests.sh` goes to GitHub user s8olheyd.

