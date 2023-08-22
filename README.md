# Fantasy Football Scoring Adjuster

## Introduction

`fantasy_football_scoring_adjuster.py` is a Python script designed to explore different ways to balance the scoring of the quarterback (QB) position in a fantasy football league. The script focuses on adjusting the scoring parameters for various statistical categories to make the QB position more balanced with other positions, such as wide receivers (WR) and running backs (RB). This README provides an overview of the script's purpose, functionality, usage, and the adjustments it offers.

## Table of Contents

- [Introduction](#introduction)
- [Table of Contents](#table-of-contents)
- [Adjustment Strategies](#adjustment-strategies)
- [Usage](#usage)
- [Scoring Parameter Examples](#scoring-parameter-examples)
- [Dependencies](#dependencies)
- [Getting Started](#getting-started)
- [License](#license)

## Adjustment Strategies

The script offers several adjustment strategies to balance the scoring of the QB position:

1. **Lower Passing Touchdown Points:** Reduce the number of points awarded for passing touchdowns to bring down the point ceiling for QBs.

2. **Adjust Passing Yards Points:** Decrease the points awarded for passing yards to balance yardage values across all positions.

3. **Minimize or Remove Rushing Points:** Reduce or eliminate points for QB rushing yards and touchdowns to align the value of running QBs with pocket passers.

4. **Adjust Sack Penalties:** Modify the severity of sack penalties for QBs, reducing the impact of negative points and balancing scoring relative to other positions.

5. **Increase Negative Points for Fumbles:** (*Note: The script doesn't currently implement this strategy specifically for QBs.*)

6. **Emphasize Other Positions:** Increase point values for touchdowns, yardage, or other metrics for WRs and RBs to enhance overall roster balance.

## Usage

1. Install the required dependencies (see [Dependencies](#dependencies)).
2. Modify the `csv_file_path` variable in the script to point to your CSV file containing player statistics.
3. Run the script using a Python interpreter: `python fantasy_football_scoring_adjuster.py`

The script will process the CSV data and output average fantasy points for players and positions based on different scoring parameter adjustments.

## Scoring Parameter Examples

The script provides three sets of scoring parameters for different levels of QB scoring adjustment:

- `default_league_scoring_parameters`: Standard scoring parameters.
- `slight_qb_nerf_scoring_parameters`: Scoring parameters with a slight QB nerf.
- `heavy_qb_nerf_scoring_parameters`: Scoring parameters with a heavy QB nerf.

You can customize these parameters to experiment with different adjustments.

## Dependencies

The script requires the following dependencies:

- Python 3.x
- `matplotlib` library (for graphing results)

You can install the `matplotlib` library using the following command:
`pip install matplotlib`


## Getting Started

1. Clone this repository: `git clone https://github.com/your_username/your_repository.git`
2. Navigate to the project directory: `cd your_repository`
3. Modify the `csv_file_path` variable in `fantasy_football_scoring_adjuster.py`.
4. Run the script: `python fantasy_football_scoring_adjuster.py`

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use and modify the script according to your needs.

---

*Author: Kevin Ponek*
*Date: 8/21/23*
