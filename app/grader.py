def grade_episode(actions, task):
    """
    actions: list of actions taken by agent
    task: current task dictionary

    returns: score between 0.0 and 1.0
    """

    score = 0.0

    correct_category = task["category"]

    classified_correctly = False
    resolved = False

    # 🔍 Check actions
    for action in actions:
        if action["action_type"] == "classify":
            if action["value"] == correct_category:
                classified_correctly = True

        if action["action_type"] == "resolve":
            resolved = True

    # ✅ Scoring logic
    if classified_correctly:
        score += 0.5

    if resolved:
        score += 0.5

    return round(score, 2)