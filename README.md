# Monitor Solution to a Concurrent Problem
This repository contains the implementation and analysis of a synchronized crossing system for a bridge shared by pedestrians and vehicles in both directions, using a monitor in Python. The problem is inspired by the real-world scenario of the bridge in Ambite, which crosses the river Tajuña and is used by both pedestrians and vehicles, but cannot accommodate vehicles in both directions simultaneously. The key challenge is to ensure safety by preventing pedestrians and vehicles from sharing the bridge at the same time and avoiding vehicles crossing in opposite directions.

## Repository Contents:

1. **FernandezdelAmoP_PRPAPractica2.pdf**
   - **Description**: This document includes a detailed description, code, and analysis of the solutions provided in this repository. It demonstrates the correctness of the solutions in terms of safety and liveliness.

2. **FernandezdelAmoP_Practica2.py**
   - **Description**: The initial solution to the exercise, developed independently without using the provided template. It references scripts seen in class about philosophers, readers, etc.

3. **FernandezdelAmoP_Practica2Ianicion.py**
   - **Description**: This script is a version of the solution that does not take into account the problem of starvation (inanición). It is developed using the provided template (skel.py).

4. **FernandezdelAmoP_Practica2vplantilla.py**
   - **Description**: This version of the solution addresses the problem of starvation using turns. It is also developed based on the provided template.

5. **Problem_Description.pdf**
   - **Description**: A document that provides a comprehensive description of the problem, including the context and specific challenges to be addressed in the solutions.

## Problem Analysis and Solutions:

- **Safety**: The solutions ensure that the bridge is safe by preventing simultaneous access by pedestrians and vehicles, and by avoiding vehicles crossing in opposite directions.
- **Deadlock Avoidance**: The implementations demonstrate the absence of deadlocks, ensuring that the system can operate continuously without halting.
- **Starvation (Inanición)**: The scripts address the issue of starvation, ensuring that all entities (pedestrians and vehicles) eventually get a chance to cross the bridge.
- **Monitor Invariant**: Each solution includes an invariant for the monitor, ensuring the correct and safe operation of the bridge crossing system.

## Usage and Implementation:

- The solutions are implemented in Python using the `multiprocessing` library.
- The repository provides both a basic solution and an advanced solution that addresses starvation.
- The PDF documents offer insights into the theoretical underpinnings and practical considerations of the implemented solutions.

This repository serves as a comprehensive resource for understanding and implementing a synchronized crossing system for shared bridges, with a focus on safety, deadlock avoidance, and starvation solutions in a multiprocessing environment.
