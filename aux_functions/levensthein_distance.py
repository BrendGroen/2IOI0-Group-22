def compute_damerau_levensthein_distance(dataframe, concept_name, concept_name_predictions, position, case_concept_name):


    """

    Converts each activity into an alphabet with "A_SUBMITTED" always being "A"
    Converts each process into words based on the alphabet mapping
    The same is done for predicted activities
    Computes the levensthein distance
    
    param dataframe: a dataframe with the below below parameters included as columns     
    param concept_name: the activity, also called concept:name in the dataset
    param concept_name: the predicted activity
    param position: the position within the process
    param case_concept_name: the unique case id, also called the case:concept:name in the dataset

    Ignore "SettingWithCopyWarning"
    

    """

    import pandas as pd

    df_mapping = dataframe[dataframe[concept_name] != "A_SUBMITTED"]
    
    alphabet_mapping = {}
    current_alphabet = 'B'  # Start with 'A' as the first alphabet
    for word in df_mapping[concept_name]:
        if word not in alphabet_mapping:
            alphabet_mapping[word] = current_alphabet
            current_alphabet = chr(ord(current_alphabet) + 1)  # Move to the next alphabet
    
    
    df_mapping['alphabet_mapping'] = df_mapping[concept_name].map(alphabet_mapping)
    
    df_submitted = dataframe[dataframe[concept_name] == "A_SUBMITTED"]
    
    df_submitted["alphabet_mapping"] = "A"
    
    df_encoded = pd.concat([df_submitted, df_mapping], axis=0)

    df_encoded.reset_index(inplace = True)

    df_encoded = df_encoded.sort_values([position], ascending = True).groupby(case_concept_name)["alphabet_mapping"].apply(lambda x: ''.join(x)).reset_index()


    df_mapping_predictions = dataframe[dataframe[concept_name_predictions] != "A_SUBMITTED"]
    
    alphabet_mapping = {}
    current_alphabet = 'B'  # Start with 'A' as the first alphabet
    for word in df_mapping_predictions[concept_name_predictions]:
        if word not in alphabet_mapping:
            alphabet_mapping[word] = current_alphabet
            current_alphabet = chr(ord(current_alphabet) + 1)  # Move to the next alphabet
    
    
    df_mapping_predictions['alphabet_mapping_predictions'] = df_mapping_predictions[concept_name_predictions].map(alphabet_mapping)
    
    df_submitted_predictions = dataframe[dataframe[concept_name] == "A_SUBMITTED"]
    
    df_submitted_predictions["alphabet_mapping_predictions"] = "A"
    
    df_encoded_predictions = pd.concat([df_submitted_predictions, df_mapping_predictions], axis=0)

    df_encoded_predictions.reset_index(inplace = True)

    df_encoded_predictions = df_encoded_predictions.sort_values([position], ascending = True).groupby(case_concept_name)["alphabet_mapping_predictions"].apply(lambda x: ''.join(x)).reset_index()

    merged_df = pd.merge(df_encoded, df_encoded_predictions, on = case_concept_name)
    
    import textdistance
    
    def calculate_distance(row):
        return textdistance.damerau_levenshtein.distance(row['alphabet_mapping'], row['alphabet_mapping_predictions'])
    
    merged_df['damerau_levenshtein_distance'] = merged_df.apply(lambda row: calculate_distance(row), axis=1)

    return merged_df
