def calculate_score(
    emd,
    supertrend,
    rsi
):

    score = 0

    if emd == 1:
        score += 40

    if supertrend == 1:
        score += 30

    if rsi > 60:
        score += 30

    return score
