def grade_episode(actions, task):
    score = 0.0

    correct_category = task["category"]

    classified_correctly = False
    resolved = False

    for action in actions:
        if action["action_type"] == "classify":
            if action["value"] == correct_category:
                classified_correctly = True

        if action["action_type"] == "resolve":
            resolved = True

    if classified_correctly:
        score += 0.5

    if resolved:
        score += 0.5

    # 🔥 Fix for validator constraint
    if score == 0.0:
        score = 0.01
    elif score == 1.0:
        score = 0.99

    return round(score, 2)