# 代码生成时间: 2025-10-10 17:17:59
# insurance_actuary_model.py

"""
Insurance Actuary Model using Python and Celery.
This model calculates various insurance metrics based on input data.
"""

import logging
from celery import Celery
from celery.result import AsyncResult
import pandas as pd
from datetime import datetime

# Initialize Celery app
app = Celery('insurance_actuary_model',
             broker='pyamqp://guest@localhost//',
             backend='rpc://')

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.task
def load_data(file_path):
    """
    Loads data from a given file path.
    
    :param file_path: Path to the CSV file containing insurance data.
    :return: DataFrame with loaded data.
    """
    try:
        data = pd.read_csv(file_path)
        logging.info(f'Data loaded successfully: {file_path}')
        return data
    except FileNotFoundError:
        logging.error(f'File not found: {file_path}')
        raise
    except Exception as e:
        logging.error(f'An error occurred while loading data: {e}')
        raise

@app.task
def calculate_policyholder_values(data):
    """
    Calculates policyholder values based on the provided data.
    
    :param data: DataFrame containing insurance data.
    :return: DataFrame with policyholder values.
    """
    try:
        # Example calculation: Sum of policyholder values
        policyholder_values = data['PolicyholderValue'].sum()
        logging.info('Policyholder values calculated successfully')
        return policyholder_values
    except KeyError:
        logging.error('PolicyholderValue column not found in data')
        raise
    except Exception as e:
        logging.error(f'An error occurred while calculating policyholder values: {e}')
        raise

@app.task
def calculate_claims(data):
    """
    Calculates claims data based on the provided data.
    
    :param data: DataFrame containing insurance data.
    :return: DataFrame with claims data.
    """
    try:
        # Example calculation: Count of claims
        claims = data['Claim'].str.contains('Claim', na=False).sum()
        logging.info('Claims calculated successfully')
        return claims
    except KeyError:
        logging.error('Claim column not found in data')
        raise
    except Exception as e:
        logging.error(f'An error occurred while calculating claims: {e}')
        raise

@app.task
def save_results(results, output_file):
    """
    Saves the results to an output CSV file.
    
    :param results: Dictionary containing results to be saved.
    :param output_file: Path to the output CSV file.
    """
    try:
        results_df = pd.DataFrame(results)
        results_df.to_csv(output_file, index=False)
        logging.info(f'Results saved successfully: {output_file}')
    except Exception as e:
        logging.error(f'An error occurred while saving results: {e}')
        raise

# Example usage
if __name__ == '__main__':
    file_path = 'insurance_data.csv'
    result = load_data.delay(file_path)
    data = result.get()
    policyholder_values = calculate_policyholder_values.delay(data)
    claims = calculate_claims.delay(data)
    results = {'PolicyholderValues': policyholder_values.get(),
               'Claims': claims.get()}
    output_file = 'insurance_results.csv'
    save_results.delay(results, output_file)