def compute_levensthein_distance(predicted, actual):
    """
    calculating the distance between the two lists of activities
    :param predicted: list of activities
    :param actual: list of activities
    :return: distance between the two lists
    """

    # if the actual list is empty, return the length of the predicted list
    if len(actual) == 0:
        return len(predicted)

    # if the predicted list is empty, return the length of the actual list
    if len(predicted) == 0:
        return len(actual)

    # creating a matrix with the size of the two lists
    matrix = [[0 for _ in range(len(actual) + 1)] for _ in range(len(predicted) + 1)]

    # filling the first row and the first column of the matrix
    for i in range(len(predicted) + 1):
        matrix[i][0] = i
    for j in range(len(actual) + 1):
        matrix[0][j] = j

    # filling the matrix
    for i in range(1, len(predicted) + 1):
        for j in range(1, len(actual) + 1):
            if predicted[i - 1] == actual[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1]
            else:
                matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + 1)

    return matrix[len(predicted)][len(actual)]
