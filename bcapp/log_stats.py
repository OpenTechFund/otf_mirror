"""
Analyze server stats for specific things related to onion services

version 0.1
"""
import sys
import os
import configparser
import click
import sh
import re
from proxy_utilities import get_configs

@click.command()
@click.option('--codes', is_flag=True, help="Status code frequency")
@click.option('--agents', is_flag=True, help="Frequency of user agents")
@click.option('--genstats', is_flag=True, help="General stats for log files")
@click.option('--path', type=str, help="Path to find file/s", default='.')
@click.option('--recursive', is_flag=True, help="Descent through directories")
@click.option('--unzip', is_flag=True, help="Unzip and analyze zipped log files", default=False)

def analyze(codes, agents, genstats, path, recursive, unzip):
    configs = get_configs()
    # get the file list to analyze
    if not os.path.exists(path):
        print("Path doesn't exist!")
        return
    if not os.path.isdir(path):
        files = [path]
    else:
        files = get_list(path, recursive)

    all_log_data = []
    for entry in files:
        if 'nginx-access' not in entry:
            continue
        analyzed_log_data = {
            'status': {},
            'user_agent': {}
        }
        entry_path = entry.split('/')
        file_parts = entry_path[-1].split('.')
        ext = file_parts[-1]
        if ((ext != 'log') and
            (ext != 'bz2')): # not a log file, nor a zipped log file
            continue
        if ext == 'bz2':
            raw_data = sh.bunzip2("-k", "-c", entry)
        else:
            with open(entry) as f:
                raw_data = f.read()
        raw_data_list = raw_data.split('\n')
        n = len(raw_data_list)
        print(f"File: {entry} Length: {n}")
        log_date_match = re.compile('[0-9]{2}[\/]{1}[A-Za-z]{3}[\/]{1}[0-9]{4}[:]{1}[0-9]{2}[:]{1}[0-9]{2}[:]{1}[0-9]{2}')
        log_status_match = re.compile('[\ ]{1}[0-9]{3}[\ ]{1}')
        for line in raw_data_list:
            log_data = {}
            try:
                log_data['datetime'] = log_date_match.search(line).group(0)
                log_data['status'] = log_status_match.search(line).group(0)
            except:
                continue
            try:
                log_data['user_agent'] = line.split(' "')[-1]
            except:
                continue
            if log_data['status'] in analyzed_log_data['status']:
                analyzed_log_data['status'][log_data['status']] += 1
            else:
                analyzed_log_data['status'][log_data['status']] = 1
            if log_data['user_agent'] in analyzed_log_data['user_agent']:
                analyzed_log_data['user_agent'][log_data['user_agent']] += 1
            else:
                analyzed_log_data['user_agent'][log_data['user_agent']] = 1
        
        for code in analyzed_log_data['status']:
            percent = int(analyzed_log_data['status'][code]/n * 100)
            print(f"Status Code {code} percentage: {percent}")

        for agent in analyzed_log_data['user_agent']:
            percent = int(analyzed_log_data['user_agent'][agent]/n * 100)
            print(f"User agent {agent} percentage: {percent}")
    return

def get_list(path, recursive):
    file_list = os.listdir(path)
    all_files = []
    for entry in file_list:
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path) and recursive:
            all_files = all_files + get_list(full_path, recursive)
        else:
            all_files.append(full_path)
    return all_files

if __name__ == '__main__':
    analyze()