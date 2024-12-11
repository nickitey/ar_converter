class TrialException:
    suppress_trial_exception: bool

    @property
    def suppress_trial_exception(self):
        return self.suppress_trial_exception
    
    @suppress_trial_exception.setter
    def suppress_trial_exception(self, value):
        self.suppress_trial_exception = value
