"""

Determine if maintaining the same predicted label
---------------------------------------------------------------------
"""


from .classification_goal_function import ClassificationGoalFunction
import math
from textattack.metrics import Metric
from textattack.constraints.semantics.sentence_encoders import UniversalSentenceEncoder
#use = UniversalSentenceEncoder()

class InputReduction(ClassificationGoalFunction):
    """Attempts to reduce the input down to as few words as possible while
    maintaining the same predicted label.

    From Feng, Wallace, Grissom, Iyyer, Rodriguez, Boyd-Graber. (2018).
    Pathologies of Neural Models Make Interpretations Difficult. ArXiv,
    abs/1804.07781.
    """

    def __init__(self, *args, target_num_words=1, **kwargs):
        self.target_num_words = target_num_words
        super().__init__(*args, **kwargs)

    def _is_goal_complete(self, model_output, attacked_text):
        return (
            self.ground_truth_output == model_output.argmax()
            and attacked_text.num_words <= self.target_num_words
        )

    def _should_skip(self, model_output, attacked_text):
        return self.ground_truth_output != model_output.argmax()
    
    def _get_score(self, model_output, attacked_text):
        # Give the lowest score possible to inputs which don't maintain the ground truth label.
        if self.ground_truth_output != model_output.argmax():
            #print(model_output.argmax())
            #print(self.ground_truth_output)
            return 0
        cur_num_words = attacked_text.num_words
        initial_num_words = self.initial_attacked_text.num_words

        # The main goal is to reduce the number of words (num_words_score)
        # Higher model score for the ground truth label is used as a tiebreaker (model_score)
        num_words_score = max(
            (initial_num_words - cur_num_words) / initial_num_words, 0
        )
        model_score = model_output[self.ground_truth_output]
        
        return min(num_words_score + model_score / initial_num_words, 1)
        """
        #sst2
        semantics_score=use._sim_score(self.ground_truth_output,attacked_text)
        #print(semantics_score)
        L=num_words_score + model_score / initial_num_words+semantics_score
        return L
            
        #mrpc
        use = UniversalSentenceEncoder()
        semantics_score=use._sim_score(attacked_text)
        if model_output.argmax()==0:
            semantics_score=semantics_score/initial_num_words
        else:
            semantics_score= math.exp(-semantics_score)
        L=num_words_score + model_score / initial_num_words+semantics_score
        return L
        """
        
            
    def extra_repr_keys(self):
        if self.maximizable:
            return ["maximizable"]
        else:
            return ["maximizable", "target_num_words"]
