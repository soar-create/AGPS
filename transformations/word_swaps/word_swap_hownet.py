"""
Word Swap by OpenHowNet
-------------------------------
"""


import pickle

from textattack.shared import utils

from .word_swap import WordSwap


class WordSwapHowNet(WordSwap):
    """Transforms an input by replacing its words with synonyms in the stored
    synonyms bank generated by the OpenHowNet."""

    PATH = "transformations/hownet"

    def __init__(self, max_candidates=-1, **kwargs):
        super().__init__(**kwargs)
        self.max_candidates = max_candidates

        # Download synonym candidates bank if they're not cached.
        cache_path = utils.download_from_s3(
            "{}/{}".format(WordSwapHowNet.PATH, "word_candidates_sense.pkl")
        )

        # Actually load the files from disk.
        with open(cache_path, "rb") as fp:
            self.candidates_bank = pickle.load(fp)

        self.pos_dict = {"ADJ": "adj", "NOUN": "noun", "ADV": "adv", "VERB": "verb"}
        self.nonpos_word={"A":1,"An":1,"a":1,"an":1,"s":1,"is":1,"are":1,"been":1,"am":1,"be":1,"was":1,"were":1,"has":1,"have":1}
    """    
    def _get_replacement_words(self, word, word_pos):
             
        Returns a list of possible 'candidate words' to replace a word in a
        sentence or phrase.

        Based on nearest neighbors selected word embeddings.
        >>> from textattack.transformations import WordSwapHowNet
        >>> from textattack.augmentation import Augmenter

        >>> transformation = WordSwapHowNet()
        >>> augmenter = Augmenter(transformation=transformation)
        >>> s = 'I am fabulous.'
        >>> augmenter.augment(s)
        
        word_pos = self.pos_dict.get(word_pos, None)
        if word_pos is None:
            return []

        try:
            candidate_words = self.candidates_bank[word.lower()][word_pos]
            if self.max_candidates > 0:
                candidate_words = candidate_words[: self.max_candidates]
            return [
                recover_word_case(candidate_word, word)
                for candidate_word in candidate_words
            ]
        except KeyError:
            # This word is not in our synonym bank, so return an empty list.
            return []
    """
    def _get_replacement_words(self, word, word_pos):
        word_pos = self.pos_dict.get(word_pos, None)
        word_nonpos = self.nonpos_word.get(word, None)
        if word_pos is None or word_nonpos == 1:
        #if word_pos is None:
            return []
        else:
            return ['at','in','before','by','until','till','for','through','within','to','of','up','out','down','as','among','without','under','across','into','besides']
        #['a','an','at','on','in','before','after','by','until','till','for','during','through','from','since','within','to','with','of','over','up','out','down','as','between','among','without','about','under','below','above','across','past','into','onto','outside','off','except','besides']
    """
    def _get_transformations(self, current_text, indices_to_modify):
        transformed_texts = []
        for i in indices_to_modify:
            word_to_replace = current_text.words[i]
            word_to_replace_pos = current_text.pos_of_word_index(i)
            replacement_words = self._get_replacement_words(
                word_to_replace, word_to_replace_pos
            )
           
            transformed_texts_idx = []
            for r in replacement_words:
                if r != word_to_replace and utils.is_one_word(r):
                    transformed_texts_idx.append(
                        current_text.replace_word_at_index(i, r)
                    )
            transformed_texts.extend(transformed_texts_idx)
# list of all indices in *this* text that have been modified
        return transformed_texts
    """
    def _get_transformations(self, current_text, indices_to_modify):
        # words = current_text.words
        transformed_texts = []
        for i in indices_to_modify:
            word_to_replace = current_text.words[i]
            word_to_replace_pos = current_text.pos_of_word_index(i)
            replacement_words = self._get_replacement_words(
                word_to_replace, word_to_replace_pos
            )
            for r in replacement_words:
                transformed_texts.append(current_text.replace_word_at_index(i, r))
        return transformed_texts


    def extra_repr_keys(self):
        return ["max_candidates"]
    

def recover_word_case(word, reference_word):
    """Makes the case of `word` like the case of `reference_word`.

    Supports lowercase, UPPERCASE, and Capitalized.
    """
    if reference_word.islower():
        return word.lower()
    elif reference_word.isupper() and len(reference_word) > 1:
        return word.upper()
    elif reference_word[0].isupper() and reference_word[1:].islower():
        return word.capitalize()
    else:
        # if other, just do not alter the word's case
        return word
