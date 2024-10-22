import random
import datetime
import re
import hyperSel.request_utilities as request_utilities
import hyperSel.log_utilities as log_utilities
import hyperSel.nodriver_utilities as nodriver_utilities
import hyperSel.selenium_utilities as selenium_utilities
import hyperSel.playwright_utilites as playwright_utilites
import hyperSel.colors_utilities as colors_utilities
import asyncio  # Add this import
import time
import re
import util
import converter
import threading
from itertools import groupby
import calc
import report

print("NOTE [1]: LATER: SEE IF IT'S POSSIBLE TO DO THIS WITH PARLAYS?", " bet on 3 outcomes instead of 2", "so make 6 bets")
print("NOTE [2]: AT SOME POINT, I WOULD BE PRINTING OUT OR LOGGING HOW MANY BETS I GOT FROM EACH URL")
print("NOTE [3]: I WANT TO BE ABLE TO SEE WHAT ALL THE DODS ARE FOR A PARTICULAR OUTCOME")
print("NOTE [4]: some odds are wrong, some returning zeroes, some wrong index etc")
print("NOTE [5]: print all outcom1  of a particular group ")
print("NOTE [6]: If mopre than 1 standard deviation awa, its prob busted, 1,1.2,1.3,1.4 6, 6 prob wrong")
print("NOTE [7]: NEED TO INCLUDE THE BET TIMES to make up for double headers, will just switch sports [MMA] for now (NO DOUBLE HEADERs)")

# input("DID U CHECK THE NOTES?")
print("========="*10)

def clean_text(text):
    return re.sub(r'[^a-zA-Z0-9\s.]', '', text)

def betway(sports):
    # print("betway sport choice:", sports)
    urls = {
        "basketball": ["https://betway.ca/en-ca/sports/grp/basketball/usa/nba"],        
    }

    all_bets = []
    for sport, urls in urls.items():
        if sport not in sports:
            continue
        # colors_utilities.c_print(f"doing {sport}", color="green")

        for url in urls:
            soup = request_utilities.get_soup(url)
            # log_utilities.log_function(soup)
            
            all_outcomes = soup.find_all("div", class_="collapsablePanel")
            for outcome_soup in all_outcomes:
                for outcome_soup in all_outcomes:
                    try:
                        outcomes = outcome_soup.select('.teamNameFirstPart')
                        outcome_1_raw = outcomes[0].text.strip()
                        outcome_1 = util.detect_and_split(clean_text(outcome_1_raw))

                        outcome_2 = util.detect_and_split(clean_text(outcomes[1].text.strip()))
                        
                        odds = outcome_soup.select('.oddsDisplay .odds')
                        odds_1 = clean_text(odds[0].text.strip())
                        odds_2 = clean_text(odds[1].text.strip())
                    

                        bet = {
                            'outcome_1': outcome_1,
                            'odds_1': odds_1,
                            'outcome_2': outcome_2,
                            'odds_2': odds_2,
                            'site': url,
                            'time_found': datetime.datetime.now().isoformat()  # Store the current time in ISO format
                        }
                        all_bets.append(bet)
                    except:
                        continue
                        
            all_scoreboards = soup.find_all("div", class_="oneLineEventItem")
            for i in all_scoreboards:
                try:
                    outcome_1 = util.detect_and_split(clean_text(i.find('div', class_='teamNameHome').get_text(strip=True)))
                    outcome_2 = util.detect_and_split(clean_text(i.find('div', class_='teamNameAway').get_text(strip=True)))
                    odds_elements = i.find_all('div', class_='odds')
                    odds = [clean_text(odds.get_text(strip=True)) for odds in odds_elements]
                    bet = {
                        'outcome_1': outcome_1,
                        'odds_1': odds[0],
                        'outcome_2': outcome_2,
                        'odds_2': odds[1],
                        'site': url,
                        'time_found': datetime.datetime.now().isoformat()
                    }
                    all_bets.append(bet)
                    continue
                except Exception as e:
                    pass
                
                try:
                    teams = i.select(".scoreboardInfoNames .teamNameFirstPart")
                    # print("teams", teams)
                    
                    outcome_1 = teams[0].get_text(strip=True)
                    outcome_2 = teams[1].get_text(strip=True)
           
                    odds = [odd.get_text(strip=True) for odd in soup.select(".oddsDisplay .odds")]
                    bet = {
                        'outcome_1': outcome_1,
                        'odds_1': odds[0],
                        'outcome_2': outcome_2,
                        'odds_2': odds[1],
                        'site': url,
                        'time_found': datetime.datetime.now().isoformat()
                    }
                    all_bets.append(bet)
                    continue
                except:
                    pass
                    
    return all_bets

def bet365(sports):
    print("BET365 SCAPE BROKEN")
    return []
    urls = {
        "basketball": ["https://www.on.bet365.ca/#/AS/B18/"],
    }
    all_bets = []
    for sport, urls in urls.items():
        if sport not in sports:
            continue
        
        for url in urls:
            # print(sport, url)
            driver = selenium_utilities.open_site_selenium(url, show_browser=True)
            time.sleep(10)
            soup = selenium_utilities.get_driver_soup(driver)
            input("WHAT IS GOING ON HERE?")
            exit()
            # log_utilities.log_function(soup)
            selenium_utilities.close_driver(driver)
            
            init_names = soup.find_all("div", class_="sbb-ParticipantTwoWayWithPitchersBaseball rcl-MarketCouponAdvancedBase_Divider gl-Market_General-cn1 sbb-ParticipantTwoWayWithPitchersBaseball-wide")
            all_team_names = []
            for i in range(len(init_names)):
                options = [
                    'sbb-ParticipantTwoWayWithPitchersBaseball_Team', 
                    'rcl-ParticipantFixtureDetailsTeam_TeamName', 
                    ]
                team_names = []
                for option in options:
                    team_name_elements = init_names[i].find_all('div', class_=option)
                    if len(team_name_elements) > 0 :
                        team_names = [element.get_text(strip=True) for element in team_name_elements]
                        all_team_names.append(team_names)
                
                if team_names == []:
                    print("no team names found?")

            all_odds = []
            all_odds_soup = soup.find_all("span", class_='sac-ParticipantCenteredStacked60OTB_Odds',)
            for i in range(len(all_odds_soup)):
                all_odds.append(all_odds_soup[i].text)

            odds = util.chunk_list(all_odds, chunk_size=30)[2]
            for i in range(len(all_team_names)):
                # Calculate the indices for odds
                odds_index = i * 2  # Odds are paired, so multiply index by 2
                
                # Get the current pair of odds
                odds_1 = odds[odds_index]
                odds_2 = odds[odds_index + 1]
                
                # Get the current team names
                outcome_1 = all_team_names[i][0]
                outcome_2 = all_team_names[i][1]

                # Construct the bet
                bet = {
                    'outcome_1': outcome_1,
                    'odds_1': odds_1,
                    'outcome_2': outcome_2,
                    'odds_2': odds_2,
                    'site': url,
                    'time_found': datetime.datetime.now().isoformat()
                }
                all_bets.append(bet)
            
    return all_bets

def betvictorcan(sports):
    # colors_utilities.c_print("GET DYNAMICALLY MATCHES FROM HERE, TONS", color="green")
    # GET URLS
    urls = {
        "basketball": [
            "https://www.betvictor.com/en-ca/sports/227/meetings/367476010/all"
            ],
    }
    all_bets = []
    for sport, urls in urls.items():
        if sport not in sports:
            continue
        
        
        for url in urls:
            # print("URL:", url)
            driver = selenium_utilities.open_site_selenium(url, show_browser=True)

            time.sleep(4)
            soup = selenium_utilities.get_driver_soup(driver)

            # href = soup.find("li", class_="row list").find('a')['href']
            # url = f"https://www.betvictor.com{href}"
            # selenium_utilities.go_to_site(driver, url)

            selenium_utilities.close_driver(driver)
            for i in soup.find_all("div", class_="inplay-coupon-row inplay"):
                # Extract team names
                teams = [team.get_text() for team in i.find_all('span', class_='inplay-coupon-team-name')]

                # Extract moneyline odds (inside the <strong> tags within bvs-button-multi-sport span elements)
                money_line_bets = [odds.get_text() for odds in i.find_all('strong')]
                
                bet = {
                    'outcome_1': teams[0],
                    'odds_1': money_line_bets[0],
                    'outcome_2': teams[1],
                    'odds_2': money_line_bets[1],
                    'site': url,
                    'time_found': datetime.datetime.now().isoformat()
                }
                # print("bet:", bet)
                all_bets.append(bet)

    return all_bets

def thescorebets(sports):
    # colors_utilities.c_print("GET DYNAMICALLY MATCHES FROM HERE, TONS", color="green")
    # GET URLS
    urls = {
        "basketball": [
            "https://thescore.bet/sport/basketball/organization/united-states/competition/nba"
            ],
    }
    all_bets = []
    for sport, urls in urls.items():
        if sport not in sports:
            continue
    
        for url in urls:
            # print("URL:", url)
            driver = selenium_utilities.open_site_selenium(url, show_browser=True)

            time.sleep(4)
            soup = selenium_utilities.get_driver_soup(driver)

            selenium_utilities.close_driver(driver)
            for i in soup.find_all("div", class_="flex flex-col gap-3 rounded p-4 bg-card-primary-temp"):

                try:
                    # Extract team names
                    teams = [team.get_text() for team in i.find_all('div', class_='text-style-s-medium text-primary text-primary')]

                    # Extract moneyline bets
                    money_line_bets = [bet.get_text() for bet in i.find_all('span', class_='font-bold')]

                    bet = {
                        'outcome_1': teams[0],
                        'odds_1': money_line_bets[2],
                        'outcome_2': teams[1],
                        'odds_2': money_line_bets[5],
                        'site': url,
                        'time_found': datetime.datetime.now().isoformat()
                    }
                    all_bets.append(bet)
                except Exception as e:
                    # print(e)
                    pass

    return all_bets

def draftkings(sports):
    all_bets = []
    urls = {
        'basketball': ["https://sportsbook.draftkings.com/leagues/basketball/nba"]
    }
    
    for sport, urls in urls.items():
        if sport not in sports:
            continue
        for url in urls:
            soup = request_utilities.get_soup(url)
            bet_elements = []
            
            index = 1
            for div in soup.find_all("div", class_="sportsbook-outcome-cell no-label"):
                index +=1
                if index % 2 == 0: # gotta skip the ones we dont need
                    continue

                team_name = util.detect_and_split(div.find('div', class_='sportsbook-outcome-cell__body')['aria-label'].strip())

                odds = div.find('span', class_='sportsbook-odds').text.strip()
                bet_elements.append((team_name, odds))

            for i in range(0, len(bet_elements), 2):
                if i + 1 < len(bet_elements):
                    team1, odds1 = bet_elements[i]
                    team2, odds2 = bet_elements[i + 1]
                    bet = {
                        'outcome_1': team1,
                        'odds_1': odds1,
                        'outcome_2': team2,
                        'odds_2': odds2,
                        'site': url,
                        'time_found': datetime.datetime.now().isoformat()
                    }
                    # print()
                    all_bets.append(bet)

    return all_bets

def caesars(sports):
    return []

def pointsbet(sports):
    all_bets = []
    urls = {
        'basketball':['https://on.pointsbet.ca/sports/basketball/NBA']
    }
    for sport, urls in urls.items():
        if sport not in sports:
            continue

        for url in urls:
            driver = selenium_utilities.open_site_selenium(url, show_browser=True)
            time.sleep(5)
            soup = selenium_utilities.get_driver_soup(driver)

            selenium_utilities.close_driver(driver)
            
            for div in soup.find_all('div', class_="fohvkg fe7oesx"):
                try:
                    # Extract team names
                    teams = [team.get_text() for team in div.find_all('p', class_='f193t5zp')]
                    if teams == []:
                        continue
                    # print("teams:", teams)

                    # Extract moneylines (odds are found inside the 'fheif50' class)
                    moneylines = [odds.get_text() for odds in div.find_all('span', class_='fheif50')]
                    if moneylines == []:
                        continue
                    # print("moneylines:", moneylines)
                    
                    bet = {
                        'outcome_1': teams[0],
                        'odds_1': moneylines[1],
                        'outcome_2': teams[1],
                        'odds_2':  moneylines[3],
                        'site': url,
                        'time_found': datetime.datetime.now().isoformat()
                    }
                    
                    all_bets.append(bet)
                except Exception as e:
                    pass
    
    return all_bets

def fanduel(sports):
    return []

    all_bets = []
    urls = {
        'basketball':['https://on.sportsbook.fanduel.ca/navigation/nba']
    }

    for sport, urls in urls.items():
        if sport not in sports:
            continue
        for url in urls:

            driver = selenium_utilities.open_site_selenium(url, show_browser=True)
            time.sleep(5)
            soup = selenium_utilities.get_driver_soup(driver)
            selenium_utilities.close_driver(driver)

            
            list_of_bets = soup.find_all("div", class_="am aq ao ap af ic s dd id az h i j ah ai m aj o ak q al")
            for li in list_of_bets:
                try:
                    outcome_1 = li.find_all("span", class_="ae af ii ij ik il hr hs ht hx im s ey ca in h i j ah ai m aj o ak q al br")[0].text
                    outcome_2 = li.find_all("span", class_="ae af ii ij ik il hr hs ht hx im s ey ca in h i j ah ai m aj o ak q al br")[1].text
                    odds_1 = li.find_all('span', class_="iq ir ey er iz ja fo")[1].text
                    odds_2 = li.find_all('span', class_="iq ir ey er iz ja fo")[4].text

                    bet = {
                            'outcome_1': outcome_1,
                            'odds_1': odds_1,
                            'outcome_2': outcome_2,
                            'odds_2': odds_2,
                            'site': url,
                            'time_found': datetime.datetime.now().isoformat()
                    }
                    all_bets.append(bet)
                except Exception as e:
                    pass

    return all_bets

async def sports_interaction(sports):
    all_bets = []
    urls = {
        'basketball':['https://sports.on.sportsinteraction.com/en-ca/sports/basketball-7']
    }

    browser = await nodriver_utilities.open_nodriver(headless=False, proxy=False)
    for sport, urls in urls.items():
        if sport not in sports:
            continue

        for url in urls:
            time.sleep(5)
            soup = await nodriver_utilities.get_site_soup(browser, url, wait=7)
            all_divs = soup.find_all("div", class_="grid-event-wrapper has-all-markets image ng-star-inserted")
            for div in all_divs:
                #print("div:",div)
                #print("---")
                try:
                    # Extract team names
                    teams = [team.get_text(strip=True) for team in div.find_all('div', class_='participant ng-star-inserted')]

                    # Extract bet spreads and odds
                    # spreads = [spread.get_text(strip=True) for spread in div.find_all('div', class_='option-attribute ng-star-inserted')]
                    odds = [odds.get_text(strip=True) for odds in div.find_all('ms-font-resizer')]

                    bet = {
                            'outcome_1': teams[0],
                            'odds_1': odds[-2],
                            'outcome_2': teams[1],
                            'odds_2': odds[-1],
                            'site': url,
                            'time_found': datetime.datetime.now().isoformat()
                    }
                    all_bets.append(bet)
                except Exception as e:
                    # print(e)
                    pass
             
    try:
        await nodriver_utilities.custom_kill_browser(browser)
    except Exception as e:
        print("cant close the driver??")

    time.sleep(5)
    return all_bets

def bet99(sports):
    all_bets = []
    urls = {
        'basketball':['https://on.bet99.ca/en/sports/basketball/usa/nba/3139']
    }
    for sport, urls in urls.items():
        if sport not in sports:
            continue
        for url in urls:
            # print(sport, url)
            driver = selenium_utilities.open_site_selenium(url, show_browser=True)
            time.sleep(10)
            driver.execute_script("document.body.style.zoom='10%'")
            time.sleep(5)
            soup = selenium_utilities.get_driver_soup(driver)
            # input("--")
            selenium_utilities.close_driver(driver)
            
            div_elements = soup.find_all('div', {'data-cy': 'priceblock-33daa089'})

            all_odds = []

            for i in range(len(div_elements)):
                all_odds.append(div_elements[i].text)

            chunks = util.chunk_list(all_odds, chunk_size=6)
            options = soup.find_all('div', {'data-cy': 'participants-cdfd8c9b'})

            for i in range(len(chunks)):
                options_1 = options[2 * i].text.strip()
                options_2 = options[2 * i + 1].text.strip()

                bet = {
                    'outcome_1': options_1,
                    'odds_1': chunks[i][2],
                    'outcome_2': options_2,
                    'odds_2': chunks[i][3],
                    'site': url,
                    'time_found': datetime.datetime.now().isoformat()
                }
                all_bets.append(bet)

    return all_bets

def sport888(sports):
    all_bets = []
    urls = {
        'basketball':['https://www.888sport.ca/basketball/nba/']
    }
    for sport, urls in urls.items():
        if sport not in sports:
            continue

        for url in urls:
            # print(sport, url)
            driver = selenium_utilities.open_site_selenium(url, show_browser=True)
            time.sleep(5)
            soup = selenium_utilities.get_driver_soup(driver)
            selenium_utilities.close_driver(driver)

            bet_soups = soup.find_all("div", class_="bet-card")
            for div in bet_soups:
                teams = [team.text.replace("@", "").strip() for team in div.find_all('span', class_='event-name__text')]
                odds = [odd.text.strip() for odd in div.find_all('div', class_='bet-button-new')]

                bet = {
                    'outcome_1': teams[0],
                    'odds_1': odds[5],
                    'outcome_2': teams[1],
                    'odds_2': odds[4],
                    'site': url,
                    'time_found': datetime.datetime.now().isoformat()
                }
                all_bets.append(bet)

    return all_bets

def betano(sports):
    urls = {
        "basketball": ["https://www.betano.ca/sport/basketball/competitions/north-america/11326/"],
    }
    all_bets = []
    for sport, urls in urls.items():
        if sport not in sports:
            continue

        for url in urls:
            # print(sport, url)
            driver = selenium_utilities.open_site_selenium(url, show_browser=True)
            time.sleep(10)
            soup = selenium_utilities.get_driver_soup(driver)
            selenium_utilities.close_driver(driver)

            soups = soup.find_all("div", class_="tw-flex tw-flex-row tw-items-stretch tw-justify-start tw-w-full")
            for i in soups:
                titles = [title.get_text(strip=True) for title in i.select('div[data-qa="participant"] span')]

                title1 = titles[0]
                title2 = titles[1]


                betobj =  i.find_all("span",class_="tw-text-tertiary dark:tw-text-quartary tw-text-s tw-leading-s tw-font-bold tw-max-w-full")
                odds1 = betobj[0].text
                odds2 = betobj[1].text

                bet = {
                    'outcome_1': title1,
                    'odds_1':odds1,
                    'outcome_2': title2,
                    'odds_2': odds2,
                    'site': url,
                    'time_found': datetime.datetime.now().isoformat()
                }
                all_bets.append(bet)

    return all_bets

def pokerstars(sports):
    print("CANT CREATE POKERSTARS APP?")
    return []
    urls = {
        "baseball": ["https://www.pokerstars.com/sports/baseball/7511/matches/"],
    }
    
    all_bets = []
    for sport, urls in urls.items():
        for url in urls:
            soup = request_utilities.get_soup(url)
            # log_utilities.log_function(soup)
            # Find all rows with betting data
            for table in soup.find_all("table",class_="_a6cc75a"):
                try:
                    # Find all rows with betting data
                    rows = table.find_all("tr", class_="_85767fe")
                    # Check to ensure there are at least two teams listed
                    if len(rows) >= 2:
                        # Extract first team details
                        title1 = rows[0].find("a", class_="_3c5be94").text.strip()
                        odds1 = rows[0].find("strong").text.strip()
                        
                        # Extract second team details
                        title2 = rows[1].find("a", class_="_3c5be94").text.strip()
                        odds2 = rows[1].find("strong").text.strip()
                        
                        # Create the bet dictionary
                        bet = {
                            'outcome_1': title1,
                            'odds_1': odds1,
                            'outcome_2': title2,
                            'odds_2': odds2,
                            'site': url,
                            'time_found': datetime.datetime.now().isoformat()
                        }

                        all_bets.append(bet)
                except:
                    pass
    return all_bets

def bet20(sports):
    print("BET 20 HAS THEIR BETS LOCKED ON WEBSITE")
    return []

    all_bets = []

    urls = {
        "baseball": ["https://20bet.com/ca/prematch/baseball"],
    }
    
    for sport, urls in urls.items():
        for url in urls:
            # print(sport, url)
            driver = selenium_utilities.open_site_selenium(url, show_browser=True)
            time.sleep(10)
            soup = selenium_utilities.get_driver_soup(driver)
            input("-")
            selenium_utilities.close_driver(driver)

def betrivers(sports):
    all_bets = []

    urls = {
        "basketball": ["https://on.betrivers.ca/?page=sportsbook&group=1000093652&type=matches"],
    }
    
    for sport, urls in urls.items():
        if sport not in sports:
            continue
        
        for url in urls:
            # print(sport, url)
            driver = selenium_utilities.open_site_selenium(url, show_browser=True)
            time.sleep(10)

            for i in range(2):
                try:
                    selenium_utilities.click_button_by_class(driver, "sc-cQGHq duNKWO")
                except Exception as e:
                    # print(e)
                    pass

            soup = selenium_utilities.get_driver_soup(driver)
            selenium_utilities.close_driver(driver)

            couplets = soup.find_all("article", attrs={"data-testid": lambda x: x and x.startswith("listview-group-1000093616-event-")})

            for i in couplets:
                try:
                    odd1 = i.find_all('button')[0].get('aria-label')
                    odd2 = i.find_all('button')[1].get('aria-label')
                    if odd1 is None or odd2 is None:
                        continue
                    
                    title1, odds1 = odd1.replace("Match Odds, ", "").split(" at ")
                    title2, odds2 = odd2.replace("Match Odds, ", "").split(" at ")

                    
                    # Create the bet dictionary
                    bet = {
                        'outcome_1': title1,
                        'odds_1': odds1,
                        'outcome_2': title2,
                        'odds_2': odds2,
                        'site': url,
                        'time_found': datetime.datetime.now().isoformat()
                    }
                    # print(bet)
                    all_bets.append(bet)

                    # print("=="*10)
                except:
                    pass
    return all_bets

def clean_all_bets(bets):
    cleaned_bets = []
    for bet in bets:
        # print(bet)
        try:
            cleaned_bet = {
                'odds_1': converter.convert_to_decimal(bet.get('odds_1', '')),
                'odds_2': converter.convert_to_decimal(bet.get('odds_2', '')),
                'site': bet.get('site', ''),
                'outcome_1': util.detect_and_split(bet.get('outcome_1', '')),
                'outcome_2': util.detect_and_split(bet.get('outcome_2', '')),
               
                'time_found': bet.get('time_found', '')
            }
            cleaned_bets.append(cleaned_bet)
        except Exception as e:
            colors_utilities.c_print(text="\n===============================================", color="blue")
            colors_utilities.c_print(text=e, color="red")
            print(bet)
            colors_utilities.c_print(text="===============================================", color="blue")
            print()
            continue

    return cleaned_bets

def fetch_and_extend(bets_function, name, all_bets, bet_counts):
    try:
        bets = bets_function()
        # print(f"{name}_bets:", len(bets))
        all_bets.extend(bets)
        bet_counts[name] = len(bets)  # Update the count in the dictionary
    except Exception:
        print(f"{name} failed")
        bet_counts[name] = 0  # Record 0 if the function failed

def get_all_bets_raw(test=False, sports=[]):
    print(f"TESTING?: [{test}]")
    threads = []
    bet_counts = {}  # Dictionary to keep track of the number of bets

    bet_functions = [
        (betway, "betway"),
        (betvictorcan, "betvictorcan"),
        (draftkings, "draftkings"),
        (bet99, "bet99"),
        (sport888, "sport888"),
        (betano, "betano"),
    ]
    
    if test:
        bet_functions = [
        (betway, "betway"),
        (betvictorcan, "betvictorcan"),
        ]

    all_bets_raw = []

    # ADDITIONAL CUZ NOT WORKING FOR SOME REASON
    for bet in asyncio.run(sports_interaction(sports)):
        all_bets_raw.append(bet)

    for bet in pointsbet(sports):
        all_bets_raw.append(bet)

    for bet in thescorebets(sports):
        all_bets_raw.append(bet)
        
    def fetch_and_extend(func, name, all_bets_raw, bet_counts, sports):
        bets = func(sports)  # Call the betting function with the sports argument
        all_bets_raw.extend(bets)
        bet_counts[name] = len(bets)
    
    threads = []
    for func, name in bet_functions:
        thread = threading.Thread(target=fetch_and_extend, args=(func, name, all_bets_raw, bet_counts, sports))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    final_bets_raw = []

    for i in all_bets_raw:
        if i['odds_1'] == '' or i['odds_2'] == '' or i['outcome_2'] == '' or i['outcome_1'] == '':
            continue
        final_bets_raw.append(i)
        
    return final_bets_raw, bet_functions, bet_counts

def grouped_bets_cleaner(grouped_bets):
    arbs = []
    # Create a list to hold the cleaned bets
    grouped_bets_cleaned = []

    # Iterate over the groups of bets
    for i in grouped_bets:
        # Sort and remove direct duplicates
        data_sorted = sorted(i, key=lambda x: (x['outcome_1'], x['odds_1'], x['outcome_2'], x['odds_2'], x['site']))
        unique_data = [next(group) for _, group in groupby(data_sorted, key=lambda x: (x['outcome_1'], x['odds_1'], x['outcome_2'], x['odds_2'], x['site']))]

        # Create a set to track sites with more than one entry
        site_count = {}
        for bet in unique_data:
            site = bet['site']
            if site in site_count:
                site_count[site] += 1
            else:
                site_count[site] = 1

        # Filter out all instances of sites that appear more than once
        filtered_data = [bet for bet in unique_data if site_count[bet['site']] == 1]

        # Add the filtered bets to the cleaned list
        grouped_bets_cleaned.append(filtered_data)
    
    #print(len(grouped_bets_cleaned))
    #print("grouped_bets_cleaned", grouped_bets_cleaned)

    if grouped_bets_cleaned == [[]]:
        print(f"NOT ENOUGH BET GROUPS FOR ARB: [-{grouped_bets_cleaned}-]")
        print("EXITING...")
        exit()

    colors_utilities.c_print("there is something going on with the flipping of games", color="green")
    for i in grouped_bets_cleaned:
        highest_odds_1 = 0
        highest_odds_2 = 0
        wanted_outcome1 = None
        wanted_outcome2 = None
        wanted_site1 = None
        wanted_site2 = None

        odds_list1 = [j["odds_1"] for j in i]
        odds_1_anomalies = util.detect_anomalies_robust(numbers=odds_list1, threshold_percentage=20)['anomalies']
        
        odds_list2 = [j["odds_2"] for j in i]
        odds_2_anomalies = util.detect_anomalies_robust(numbers=odds_list2, threshold_percentage=20)['anomalies']
        
        for j in i:
            odds_1 = j["odds_1"]
            if odds_1 in odds_1_anomalies:
                print(F"[ANOM][1]-SKIPPING [{odds_1}]: {odds_1_anomalies}")

            odds_2 = j["odds_2"]
            if odds_2 in odds_2_anomalies:
                print(F"[ANOM][2]-SKIPPING [{odds_2}]: {odds_2_anomalies}")

            if odds_1 >= highest_odds_1:
                wanted_outcome1 = j['outcome_1']
                wanted_site1 = j['site']
                highest_odds_1 = j['odds_1']
            
            if odds_2 >= highest_odds_2:
                wanted_outcome2 = j['outcome_2']
                wanted_site2 = j['site']
                highest_odds_2 = j['odds_2']

        prob = calc.calculate_implied_probability(odds=[highest_odds_1, highest_odds_2])
        arbs.append({
            "implied_probability":prob['Total Implied Probability (%)'],
            "1": {
                "o_1":wanted_outcome1,
                "s_1":wanted_site1,
                "p_1":highest_odds_1,
            },
            "2": {
               "o_2":wanted_outcome2,
                "s_2":wanted_site2,
                "p_2":highest_odds_2,
            }
           
        })

    return arbs

if __name__ == '__main__':
    sports = ['basketball']

    for bet in pointsbet(sports):
        colors_utilities.c_print(bet, "background_bright_blue")
        colors_utilities.c_print("--", "background_bright_blue")
    print("===="*20)
    print("===="*20)
    exit()
    for bet in asyncio.run(sports_interaction(sports)):
        colors_utilities.c_print(bet, "white")
        colors_utilities.c_print("--", "white")
    print("===="*20)
    print("===="*20)
    exit()

    for bet in betano(sports):
        colors_utilities.c_print(bet, "white")
        colors_utilities.c_print("--", "white")
    print("===="*20)
    print("===="*20)
    
    for bet in sport888(sports):
        colors_utilities.c_print(bet, "white")
        colors_utilities.c_print("--", "white")
    print("===="*20)
    print("===="*20)
    
    for bet in bet99(sports):
        colors_utilities.c_print(bet, "white")
        colors_utilities.c_print("--", "white")
    print("===="*20)
    print("===="*20)





    for bet in draftkings(sports):
        colors_utilities.c_print(bet, "bright_yellow")
        colors_utilities.c_print("--", "bright_yellow")
    print("===="*20)
    print("===="*20)

    for bet in betway(sports):
        colors_utilities.c_print(bet, "cyan")
        colors_utilities.c_print("--", "cyan")
    print("===="*20)
    print("===="*20)

    for bet in betvictorcan(sports):
        colors_utilities.c_print(bet, "green")
        colors_utilities.c_print("--", "green")
    print("===="*20)
    print("===="*20)
    
    for bet in thescorebets(sports):
        colors_utilities.c_print(bet, "red")
        colors_utilities.c_print("--", "red")
    print("===="*20)
    print("===="*20)
    pass
