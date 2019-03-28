import argparse
import datetime as dt
import os
import logging

import login_attempt_simulator as sim

user_base_file = 'user_data/user_base.txt'
user_ip_mapping_file = 'user_data/user_ips.json'
attempt_log_file = 'logs/log.csv'
hack_log_file = 'logs/attacks.csv'

# Logging configuration
FORMAT = '[%(levelname)s] [ %(name)s ] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(os.path.basename(__file__))

if __name__ == '__main__':
    # command line argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "days", type=float,
        help="number of days to simulate from start"
    )
    parser.add_argument(
        "start_date", type=str,
        help="datetime to start in the form 'YYYY-MM-DD' or 'YYYY-MM-DD-HH'"
    )
    parser.add_argument(
        "-m", "--make", action='store_true', help="make userbase"
    )
    parser.add_argument(
        "-u", "--userbase", help="file to write the userbase to"
    )
    parser.add_argument(
        "-i", "--ip", help="file to write the user-ip map to"
    )
    parser.add_argument(
        "-l", "--log", help="file to write the attempt log to"
    )
    parser.add_argument(
        "-hl", "--hacklog", help="file to write the hack log to"
    )
    args = parser.parse_args()
    user_ip_mapping_file = args.ip or user_ip_mapping_file

    if args.make:
        logger.warning('Creating new user base and mapping IPs to them.')

        user_base_file = args.userbase or user_base_file

        # create usernames and write to file
        sim.utils.make_userbase(user_base_file)

        # create one or more IPs per user and save mapping to file
        valid_users = sim.utils.get_valid_users(user_base_file)
        sim.utils.save_user_ips(
            sim.utils.assign_ip_addresses(valid_users), user_ip_mapping_file
        )

    try:
        start = dt.datetime(*map(int, args.start_date.split('-')))
    except TypeError:
        logger.error('Start date must be in the format "YYYY-MM-DD"')
        raise
    except ValueError:
        logger.warning(
            f'Could not interpret {args.start_date}, '
            'using February 2, 2019 at 7AM as start instead'
        )
        start = dt.datetime(2019, 2, 1, 7, 0)


    end = start + dt.timedelta(days=args.days)

    try:
        logger.info(f'Simulating {args.days} days...')
        simulator = sim.LoginAttemptSimulator(user_ip_mapping_file, start, end)
        simulator.simulate(attack_prob=0.1, try_all_users_prob=0.65, vary_ips=False)

        # save logs
        logger.info('Saving logs')
        simulator.save_hack_log(args.hacklog or hack_log_file)
        simulator.save_log(args.log or attempt_log_file)

        logger.info('All done!')
    except:
        logger.error('Oops! Something went wrong...')
