from django.dispatch import Signal


user_attributes_changed = Signal(providing_args=["candidate_id", "score_up"])

