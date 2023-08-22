#
#  @file   fantasy_football_scoring_adjuster.py
#
#  @author kevinponek.
#  @date   8/21/23.
#

"""
* Different ways to balance QB position *
Reducing quarterback scoring in a superflex league can help balance the value of the QB position with other positions
like wide receivers (WR) and running backs (RB).

1. Lower Passing Touchdown Points
- Reduce the number of points awarded for passing touchdowns. Instead of the standard 4 points per passing touchdown,
  consider lowering it to 3 or even 2 points. This adjustment will bring down the point ceiling for QBs.

2. Adjust Passing Yards Points
- Decrease the points awarded for passing yards. Instead of the standard 1 point for every 25 passing yards, you could
  use a ratio of 1 point for every 30 or 40 passing yards. This balances out the value of yardage across all positions.

3. Minimize or Remove Rushing Points
- If you currently award points for quarterback rushing yards and touchdowns, reduce or eliminate these points. This
  helps bring the value of running QBs more in line with pocket passers.

4. Adjust Sack Penalties
- If your league penalizes quarterbacks for sacks, consider making the penalty less severe. This change would reduce the
  impact of negative points for QBs and balance their scoring relative to other positions.

5. Increase Negative Points for Fumbles (not sure if this can be specifically tweaked only for QB in ESPN)

6. Emphasize Other Positions
- Consider increasing the point values for touchdowns, yardage, or other performance metrics for WRs and RBs. This
  encourages managers to value and invest in these positions more, enhancing overall roster balance.
"""
import csv
from collections import defaultdict

csv_file_path = 'player_stats.csv'

default_league_scoring_parameters = {
	'points_per_passing_td': 4,
	'points_per_passing_yard': 0.04,
	'points_per_interception': -2,
	'points_per_rushing_td': 6,
	'points_per_rushing_yard': 0.1,
	'points_per_receiving_td': 6,
	'points_per_receiving_yard': 0.1,
	'points_per_reception': 1,

	# special stats not used before
	'points_per_sack': 0,
	'qb_points_per_rushing_td': 6, # this separate variable is to differentiate between rushing td's of QB's vs other positions
	'qb_points_per_rushing_yard': 0.1, # this separate variable is to differentiate between rushing yd's of QB's vs other positions
}

slight_qb_nerf_scoring_parameters = {
	'points_per_passing_td': 4,
	'points_per_passing_yard': 0.04,
	'points_per_interception': -3,
	'points_per_rushing_td': 6,
	'points_per_rushing_yard': 0.1,
	'points_per_receiving_td': 6,
	'points_per_receiving_yard': 0.1,
	'points_per_reception': 1,

	# special stats not used before
	'points_per_sack': 0,
	'qb_points_per_rushing_td': 5, # this separate variable is to differentiate between rushing td's of QB's vs other positions
	'qb_points_per_rushing_yard': 0.1, # this separate variable is to differentiate between rushing yd's of QB's vs other positions
}

heavy_qb_nerf_scoring_parameters = {
	'points_per_passing_td': 3,
	'points_per_passing_yard': 0.04,
	'points_per_interception': -2,
	'points_per_rushing_td': 6,
	'points_per_rushing_yard': 0.1,
	'points_per_receiving_td': 6,
	'points_per_receiving_yard': 0.1,
	'points_per_reception': 1,

	# special stats not used before
	'points_per_sack': 0,
	'qb_points_per_rushing_td': 4, # this separate variable is to differentiate between rushing td's of QB's vs other positions
	'qb_points_per_rushing_yard': 0.1, # this separate variable is to differentiate between rushing yd's of QB's vs other positions
}

def print_columns(csv_path):
	with open(csv_path, 'r', newline='') as csvfile:
		reader = csv.reader(csvfile)
		headers = next(reader)  # Read the header row

		print(f"Columns in the CSV: {headers}")
		# for column in headers:
		# 	print(column)


def calculate_fantasy_points(row, scoring_parameters):
	# PPR Scoring
	passing_tds_points = float(row['passing_tds']) * scoring_parameters['points_per_passing_td']
	passing_yards_points = float(row['passing_yards']) * scoring_parameters['points_per_passing_yard']
	interceptions_penalty = float(row['interceptions']) * scoring_parameters['points_per_interception']

	if row['position'].upper() == 'QB':
		sacks_penalty = float(row['sacks']) * scoring_parameters['points_per_sack']
	else:
		sacks_penalty = 0

	if row['position'].upper() == 'QB': # special cases for QB done with this
		rushing_tds_points = float(row['rushing_tds']) * scoring_parameters['qb_points_per_rushing_td']
		rushing_yards_points = float(row['rushing_yards']) * scoring_parameters['qb_points_per_rushing_yard']
	else:
		rushing_tds_points = float(row['rushing_tds']) * scoring_parameters['points_per_rushing_td']
		rushing_yards_points = float(row['rushing_yards']) * scoring_parameters['points_per_rushing_yard']

	receiving_tds_points = float(row['receiving_tds']) * scoring_parameters['points_per_receiving_td']
	receiving_yards_points = float(row['receiving_yards']) * scoring_parameters['points_per_receiving_yard']
	receptions_points = float(row['receptions']) * scoring_parameters['points_per_reception']  # PPR

	# Calculate total fantasy points
	total_fantasy_points = (
		passing_tds_points +
		passing_yards_points +
		interceptions_penalty +
		rushing_tds_points +
		rushing_yards_points +
		receiving_tds_points +
		receiving_yards_points +
		receptions_points +
		sacks_penalty
		# Add more calculations for other categories
	)

	return total_fantasy_points

def process_csv_per_player_averages(csv_path, chosen_year, scoring_parameters):
	player_data = defaultdict(list)

	with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['season'] == chosen_year:
				fantasy_points = calculate_fantasy_points(row, scoring_parameters)
				player_name = row['player_name']
				player_position = row['position']
				player_data[(player_name, player_position)].append(fantasy_points)

	print("Player Averages and Totals:")

	for (player_name, player_position), points_list in player_data.items():
		total_points = sum(points_list)
		average_points = total_points / len(points_list)
		print(f"Player Name: {player_name}, Position: {player_position}, Total Points: {total_points:.2f}, Average Points: {average_points:.2f}")


def process_csv_position_averages(csv_path, chosen_year, scoring_parameters, x = 30):
	player_data = defaultdict(list)

	with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['season'] == chosen_year:
				fantasy_points = calculate_fantasy_points(row, scoring_parameters)
				player_name = row['player_name']
				player_position = row['position']
				player_data[(player_name, player_position)].append(fantasy_points)

	top_x_averages = {}
	position_averages = {}
	for (player_name, player_position), points_list in player_data.items():
		total_points = sum(points_list)
		average_points = total_points / len(points_list)

		if player_position not in top_x_averages:
			top_x_averages[player_position] = []

		top_x_averages[player_position].append(average_points)

	for position, averages_list in top_x_averages.items():
		top_x_averages[position] = sorted(averages_list, reverse=True)[:x]
		avg = sum(top_x_averages[position]) / len(top_x_averages[position])
		if position in ('QB', 'RB', 'WR'):
			print(f"Position: {position}, Average Points: {avg:.2f}")
			position_averages[position] = avg
	return position_averages

def graph_results(position_averages_all):
	import matplotlib.pyplot as plt

	fig, ax = plt.subplots()
	for year, x_dict in position_averages_all.items():
		for x, position_dict in x_dict.items():
			# for position, avg in position_dict.items():
				plt.plot(list(position_dict.keys()), list(position_dict.values()), label=f'{year} - Top {x}')
	plt.xlabel('Position')
	plt.ylabel('Average Points')
	plt.title('Average Fantasy Points for QB Position Across Years')
	leg = plt.legend(loc='upper center')
	plt.grid(True)
	plt.show()
	plt.clf()


if __name__ == "__main__":
	position_averages_all = {}
	for chosen_year in ['2020', '2021', '2022']:
		position_averages_all[chosen_year] = {}
		for x in [10, 20, 30, 40]:

			print(f"\nAverage Fantasy Points in {chosen_year} for Top {x} Players by Position with last year's settings:")
			position_averages = process_csv_position_averages(csv_file_path, chosen_year, default_league_scoring_parameters, x)
			position_averages_all[chosen_year][x] = position_averages
			print(f"\nAverage Fantasy Points in {chosen_year} for Top {x} Players by Position with slight QB nerf:")
			position_averages_slight = process_csv_position_averages(csv_file_path, chosen_year, slight_qb_nerf_scoring_parameters, x)
			position_averages_all[chosen_year][x]['QB_slight_nerf'] = position_averages_slight['QB']
			print(f"\nAverage Fantasy Points in {chosen_year} for Top {x} Players by Position with heavy QB nerf:")
			position_averages_heavy = process_csv_position_averages(csv_file_path, chosen_year, heavy_qb_nerf_scoring_parameters, x)
			position_averages_all[chosen_year][x]['QB_heavy_nerf'] = position_averages_heavy['QB']
			print('----------------------------------------------------------------------------------')
		print('************************************************************************')
		graph_results(position_averages_all)