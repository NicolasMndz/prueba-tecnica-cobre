# test_data_integrity.py
import pytest
import pandas as pd
import numpy as np

@pytest.fixture(scope='module')
def balances():
    df = pd.read_csv('account_balances_daily_CLEAN.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

@pytest.fixture(scope='module')
def accounts():
    return pd.read_csv('accounts.csv')

@pytest.fixture(scope='module')
def transfers():
    df = pd.read_csv('transfers_log_CLEAN.csv')
    df['date_requested'] = pd.to_datetime(df['date_requested'])
    df['date_settled'] = pd.to_datetime(df['date_settled'])
    return df

def test_temporal_continuity(balances):
    for acc in balances['account_id'].unique():
        sub = balances[balances['account_id'] == acc].sort_values('date')
        assert len(sub) == 270, f'Cuenta {acc} tiene {len(sub)} registros, esperado 270'
        date_diffs = sub['date'].diff().dropna()
        assert (date_diffs == pd.Timedelta(days=1)).all(), f'Cuenta {acc} tiene huecos'

def test_no_null_values(balances):
    critical_cols = ['date', 'account_id', 'currency', 'balance', 'inflow', 'outflow', 'net_flow']
    null_counts = balances[critical_cols].isna().sum()
    assert null_counts.sum() == 0, f'Existen nulos: {null_counts.to_dict()}'

def test_non_negative_values(balances):
    assert (balances['balance'] >= 0).all(), 'Saldos negativos'
    assert (balances['inflow'] >= 0).all(), 'Inflows negativos'
    assert (balances['outflow'] >= 0).all(), 'Outflows negativos'

def test_currency_standardization(balances, accounts):
    valid_currencies = {'COP', 'USD', 'MXN'}
    assert set(balances['currency'].unique()).issubset(valid_currencies)
    for _, row in accounts.iterrows():
        acc = row['account_id']
        expected_curr = row['currency']
        actual_currs = balances[balances['account_id'] == acc]['currency'].unique()
        assert len(actual_currs) == 1 and actual_currs[0] == expected_curr

def test_accounting_identity_median(balances):
    for acc in balances['account_id'].unique():
        sub = balances[balances['account_id'] == acc].sort_values('date')
        disc = (sub['balance'].diff() - (sub['inflow'] - sub['outflow'])).dropna()
        assert np.isclose(disc.median(), 0.0, atol=1e-2)

def test_transfers_consistency(transfers, accounts):
    acc_ids = set(accounts['account_id'].unique())
    assert set(transfers['from_account'].unique()).issubset(acc_ids)
    assert set(transfers['to_account'].unique()).issubset(acc_ids)
    assert (transfers['lag_days'] >= 0).all()
    assert (transfers['amount'] > 0).all()
    assert (transfers['fee'] >= 0).all()
