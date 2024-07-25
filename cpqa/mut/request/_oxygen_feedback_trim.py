from cpqa.mut.request import MutRequest


class OxygenFeedbackTrim(MutRequest):
    @property
    def name(self):
        return "OxygenFeedbackTrim"

    @property
    def name_short(self):
        return "O2FeedbackTrim"

    @property
    def request_id(self):
        return 0x0F

    @property
    def unit(self):
        return "%"

    @property
    def max(self):
        return 200

    @property
    def min(self):
        return 0

    def convert(self, x):
        return (0.1961 * x) - 25  # 0.78125 * x ??
