def aggregate_by_player_id(statistics, playerid, fields):
    """
    Aggregates baseball statistics by player ID.

    Args:
        statistics: A list of dictionaries, where each dictionary represents a
                    row of baseball statistics.
        playerid: The key in each dictionary that corresponds to the player's ID.
        fields: A list of keys for the stats to be aggregated.

    Returns:
        A dictionary where keys are player IDs and values are dictionaries
        containing the aggregated stats for that player.
    """
    aggregated_stats = {}
    for row in statistics:
        pid = row[playerid]
        if pid not in aggregated_stats:
            # Initialize the dictionary for this new player
            aggregated_stats[pid] = {playerid: pid}
            for field in fields:
                aggregated_stats[pid][field] = 0
        
        # Add the stats from the current row
        for field in fields:
            # Important: Convert stat from string to number before adding
            aggregated_stats[pid][field] += float(row[field])
            
    return aggregated_stats
def top_player_ids(info, statistics, formula, k):
    """
    Finds the top k players based on a given statistical formula.

    Args:
        info: A dictionary of configuration information.
        statistics: A list of dictionaries with player stats.
        formula: A function that takes a dictionary of stats and returns a score.
        k: The number of top players to return.

    Returns:
        A list of (player_id, score) tuples for the top k players,
        sorted in descending order by score.
    """
    player_scores = []
    for player_stats in statistics:
        player_id = player_stats[info['playerid']]
        
        # The formula function expects a single dictionary of stats.
        score = formula(player_stats) 
        
        player_scores.append((player_id, score))
    
    # Sort the list of tuples by the score (the second element)
    player_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return the top k players
    return player_scores[:k]
# Assume you have a function like this from the project description
# def read_csv_as_list_dict(filename, separator, quote):
#     ... returns a list of dictionaries ...

def lookup_player_names(info, player_ids_stats):
    """
    Looks up player names and formats the output.
    
    Args:
        info: A dictionary of configuration information.
        player_ids_stats: A list of (player_id, stat) tuples.
        
    Returns:
        A list of strings, each formatted as "STAT --- PLAYER_NAME".
    """
    # This function was likely called with the wrong arguments in your code.
    # It should take the list of (player_id, stat) tuples.
    master_data = read_csv_as_list_dict(info['masterfile'], info['separator'], info['quote'])
    
    name_map = {}
    for row in master_data:
        player_id = row[info['playerid']]
        first_name = row[info['firstname']]
        last_name = row[info['lastname']]
        name_map[player_id] = f"{first_name} {last_name}"

    formatted_list = []
    for player_id, stat in player_ids_stats:
        player_name = name_map.get(player_id, "Unknown Player")
        formatted_list.append(f"{stat:.3f} --- {player_name}")
        
    return formatted_list

def compute_top_stats_year(info, formula, k, year):
    """
    Computes the top k players for a given year and statistic.
    """
    batting_data = read_csv_as_list_dict(info['battingfile'], info['separator'], info['quote'])
    
    # 1. Filter data for the given year
    year_stats = filter_by_year(batting_data, year, info['yearid'])
    
    # 2. Get top player IDs and their stats
    # Note: top_player_ids needs the list of player stat dicts
    top_ids_and_stats = top_player_ids(info, year_stats, formula, k)
    
    # 3. Look up names and format the output
    result = lookup_player_names(info, top_ids_and_stats)
    
    return result # Make sure this return statement exists!

def compute_top_stats_career(info, formula, k):
    """
    Computes the top k players for a career and statistic.
    """
    batting_data = read_csv_as_list_dict(info['battingfile'], info['separator'], info['quote'])
    
    # 1. Aggregate stats by player ID
    # The test expects a dictionary, but top_player_ids expects a list of dicts.
    # So we take the values from the aggregated dictionary.
    aggregated_dict = aggregate_by_player_id(batting_data, info['playerid'], info['battingfields'])
    career_stats_list = list(aggregated_dict.values())

    # 2. Get top player IDs and their stats
    top_ids_and_stats = top_player_ids(info, career_stats_list, formula, k)
    
    # 3. Look up names and format the output
    result = lookup_player_names(info, top_ids_and_stats)
    
    return result # Make sure this return statement exists!
