from sauron.rule_engine import RuleEngine

engine = RuleEngine()


@engine.condition()
def condition_true(session):
    return True


@engine.condition()
def second_condition_true(session):
    return True


@engine.condition()
def condition_false(session):
    return False


@engine.condition()
def condition_failure(session):
    raise Exception


@engine.action()
def action_success(session):
    print("success")


rule = """
    {
        "conditions": [
            {
                "name": "condition_false",
                "args": {
                }
            }
        ],
        "actions": [
            {
                "name": "action_success"
            }
        ]
    }
    """

# get signals instances to connect
pre_job_hook = engine.get_signal('pre_job_call')
post_job_hook = engine.get_signal('post_job_call')

pre_engine_run = engine.get_signal('pre_engine_run')
post_engine_run = engine.get_signal('post_engine_run')


# declare functions to be called on hook
def pre_hook_callback(sender, **kwargs):
    print(f"[PRE] Caught signal from {sender} \n\twith kw:{kwargs}")


def post_hook_callback(sender, **kwargs):
    print(f"[POST] Caught signal from {sender} \n\twith kw:{kwargs}")


# connect signals and callbacks:
pre_job_hook.connect(pre_hook_callback, sender=engine)
post_job_hook.connect(post_hook_callback, sender=engine)

pre_engine_run.connect(pre_hook_callback, sender=engine)
post_engine_run.connect(post_hook_callback, sender=engine)

engine.run(rule)
