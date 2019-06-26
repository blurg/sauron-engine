class GenericRuleProcessor:
    def run(self, rule):
        if getattr(self, rule["condition"])(rule["value"]):
            getattr(self, rule["action"])()

