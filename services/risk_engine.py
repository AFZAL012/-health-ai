def calculate_risk(probability, severity, duration, emergency):

    score = probability

    if severity in ["severe", "intense", "unbearable"]:
        score += 20

    if duration:
        score += 10

    if emergency:
        score += 50

    if score < 40:
        return "Low", score
    elif score < 70:
        return "Medium", score
    else:
        return "High", score