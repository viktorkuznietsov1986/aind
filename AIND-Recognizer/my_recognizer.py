import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer
    test_sequences = list(test_set.get_all_Xlengths().values())
    for test_X, test_Xlength in test_sequences:
        prob = {}
        logL_max = float("-inf")
        best_guess = ""

        for word, model in models.items():
            try:

                logL = model.score(test_X, test_Xlength)
                prob[word] = logL

                if logL > logL_max:
                    logL_max = logL
                    best_guess = word

            except:
                print ("Model for word '{0}' cannot score the data.".format(word))

        probabilities.append(prob)

        if best_guess != "":
            guesses.append(best_guess)

    return probabilities, guesses

