import pandas as pd


def split_data(df: pd.DataFrame, ratio: float = 0.8, report: bool = True) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits the dataframe into a training and test set based on the given ratio.
    The ratio is the percentage of the training set, the test set will be 1 - ratio.
    The split is based on the case:concept:name, so all events of a case will be in the same set.
    The function will remove cases that are present in both sets.
    :param df: The dataframe to split
    :param ratio: The ratio of the training set
    :param report: Whether to print a report of the split
    :return: A tuple with the training and test set
    """

    # Split the dataframe
    nr_rows = len(df)
    train_size = int(nr_rows * ratio)
    test_size = nr_rows - train_size
    train = df.head(train_size)
    test = df.tail(test_size)

    # Get the unique cases in both sets
    train_cases = train['case:concept:name'].unique()
    test_cases = test['case:concept:name'].unique()
    intersection = set(train_cases).intersection(test_cases)

    # Remove cases that are present in both sets
    train = train[~train['case:concept:name'].isin(intersection)]
    test = test[~test['case:concept:name'].isin(intersection)]

    # Print a report
    if report:
        print(f'Original size: {nr_rows}')
        print(f'Train size: {len(train)}')
        print(f'Test size: {len(test)}')
        print(f'Ratio: {len(train) / (len(train) + len(test))}')
        print(f'Dropped cases in both sets: {len(intersection)}')
        print(f'Dropped rows from dataset: {nr_rows - len(train) - len(test)}')

    return train, test
