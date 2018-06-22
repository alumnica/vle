from django import forms

class EvaluationForm(forms.Form):
    def review_evaluation(self, evaluation, relationship_answers, multiple_option_answers, multiple_answer_answers,
                               numeric_answers, pulldown_list_answers, learner):
        questions = relationship_answers.split('|')

