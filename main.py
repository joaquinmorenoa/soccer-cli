import requests
import click
import leagueids

BASE_URL = 'http://api.football-data.org/alpha/'
LIVE_URL = ''
LEAGUE_IDS = leagueids.LEAGUE_IDS

def get_standings(league):
	""" Queries the API and gets the standings for a particular league """

	league_id = LEAGUE_IDS[league]
	league_table = requests.get('{base_url}soccerseasons/{id}/leagueTable'.format(
			base_url=BASE_URL, id=league_id)).json()
	print_standings(league_table)

def print_standings(league_table):

	for team in league_table["standing"]:
		print "{position}. {team_name}".format(position=team["position"], team_name=team["teamName"])

def get_scores(league, time):
	""" Queries the API and fetches the scores for fixtures based upon the league and time parameter """

	if league:
		league_id = LEAGUE_IDS[league]
		fixtures_results = requests.get('{base_url}soccerseasons/{id}/fixtures?timeFrame=p{time}'.format(
			base_url=BASE_URL, id=league_id, time=str(time))).json()
		pretty_print(fixtures_results)
		return

	fixtures_results = requests.get('{base_url}fixtures?timeFrame=p{time}'.format(
		base_url=BASE_URL, time=str(time))).json()
	pretty_print(fixtures_results)
	return

def pretty_print(total_data):
	""" Prints the data in a pretty format """

	for data in total_data["fixtures"]:
		print data["homeTeamName"] + " " + str(data["result"]["goalsHomeTeam"]) + " vs "  + str(data["result"]["goalsAwayTeam"]) + " " + data["awayTeamName"] 


@click.command()
@click.option('--standings', is_flag=True, help= 'Standings for a particular league')
@click.option('--league', '-league', type=click.Choice(LEAGUE_IDS.keys()), 
	help= (
		"Choose the league whose fixtures you want to see. Bundesliga(BL), Premier League(EPL), La Liga (LLIGA)," 
	 	"Serie A(SL), Ligue 1(FL), Eredivisie(DED), Primeira Liga(PPL)')"
	)
)
@click.option('--time', '-t', default=6, 
	help= 'The number of days for which you want to see the scores')

def main(league, time, standings):
	""" A CLI for live and past football scores from various leagues """

	if standings:
		get_standings(league)
		return

	get_scores(league, time)

if __name__ == '__main__':
	main()