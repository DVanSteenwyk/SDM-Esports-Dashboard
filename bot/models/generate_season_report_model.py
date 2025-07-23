# bot/models/generate_season_report_model.py

import datetime
from collections import defaultdict

def ordinal_suffix(n):
    if 11 <= (n % 100) <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")

def generate_season_report(matches):
    completed = [m for m in matches if m.get('HomeScore') not in [None, "", " "]]

    if not completed:
        return "No completed matches to report."

    ffa_results = defaultdict(list)
    league_records = defaultdict(lambda: {'wins': 0, 'losses': 0, 'draws': 0})
    overall = {'wins': 0, 'losses': 0, 'draws': 0}

    report_lines = []
    report_lines.append("Season Report")
    report_lines.append(f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("=" * 40)

    for match in completed:
        league = match.get('League', 'Unknown League')
        away_team = match.get('AwayTeam', '').strip()
        home_score = match.get('HomeScore')

        if not away_team:
            # FFA match
            try:
                placement = int(home_score)
                pool_size = int(match.get('PoolSize', 0))
                ffa_results[league].append((placement, pool_size))
            except ValueError:
                continue
        else:
            # H2H match
            try:
                home_score = int(home_score)
                away_score = int(match.get('AwayScore'))
            except (ValueError, TypeError):
                continue

            if home_score > away_score:
                league_records[league]['wins'] += 1
                overall['wins'] += 1
            elif home_score < away_score:
                league_records[league]['losses'] += 1
                overall['losses'] += 1
            else:
                league_records[league]['draws'] += 1
                overall['draws'] += 1

    report_lines.append(f"Overall Record: {overall['wins']}W - {overall['losses']}L - {overall['draws']}D")
    report_lines.append("")

    for league, rec in league_records.items():
        report_lines.append(f"{league}: {rec['wins']}W - {rec['losses']}L - {rec['draws']}D")

    if ffa_results:
        report_lines.append("\nFFA Season Summary:")
        for league, entries in ffa_results.items():
            total_placement = sum(p for p, _ in entries)
            total_pool = sum(ps for _, ps in entries if ps > 0)
            avg_placement = total_placement / len(entries)
            avg_pool = total_pool / len([ps for _, ps in entries if ps > 0])
            report_lines.append(
                f"{league}: {len(entries)} entries, Average Placement: {avg_placement:.2f} out of {avg_pool:.1f}"
            )
        report_lines.append("-" * 40)

    report_lines.append("=" * 40)

    for match in completed:
        league = match.get('League', 'Unknown League')
        away_team = match.get('AwayTeam', '').strip()
        round_ = match.get('Round', 'N/A')
        date = match.get('Date', 'N/A')
        time = match.get('Time', '')

        if not away_team:
            try:
                placement = int(match.get('HomeScore'))
                pool_size = int(match.get('PoolSize', 0))
                report_lines.append(
                    f"Round {round_}: Placed {placement}{ordinal_suffix(placement)} out of {pool_size} in {league} on {date} @ {time}"
                )
            except ValueError:
                continue
        else:
            line = (
                f"Round {round_}: "
                f"Hardrocker Esports ({match.get('HomeRank', '')}) "
                f"{match.get('HomeScore')} - {match.get('AwayScore')} "
                f"{match.get('AwayTeam', 'Unknown')} ({match.get('AwayRank', '')}), "
                f"Date: {date} {time}, "
                f"League: {league}"
            )
            report_lines.append(line)

    return "\n".join(report_lines)