import xdice


def parse_msg(message_content):
    attr_score = 0
    adv = 0
    vicious = False
    repeat = False
    destructive = False

    repeat_factor = 1

    args = message_content.split(" ")[1:]
    for arg in args:
        if arg == "-V" or arg == "-v":
            vicious = True
        elif arg == "-R" or arg == "-r":
            repeat = True
        elif arg == "-D" or arg == "-d":
            destructive = True

    args = [a for a in args if a.isnumeric()]

    if len(args) < 2 or len(args) > 3:
        return -1

    attr_score = args[0]
    adv = args[1]
    if int(adv) > 10:
        adv = 10

    if repeat and len(args) == 3:
        repeat_factor = args[2]

    return vicious, destructive, int(attr_score), int(adv), int(repeat_factor)


def roll20(adv, vicious, destructive):
    d20_count = 1 + abs(adv)
    if adv >= 0:
        score = xdice.rolldice(20, d20_count, adv, 0)
    elif adv < 0:
        score = xdice.rolldice(20, d20_count, 0, adv)

    rolls = []
    dropped = score.dropped
    dropped_vicious = []

    for res in list(score):
        roll = [int(res)]
        while res == 20 or (destructive and res == 19):
            if vicious:
                score = xdice.rolldice(20, 2, 1, 0)
            else:
                score = xdice.rolldice(20, 1, 0, 0)
            res = int(score)
            roll.append(res)
            dropped_vicious = score.dropped
        rolls.append(roll)

    return rolls, dropped, dropped_vicious


def rollAttr(dcount, dsize, adv, destructive):
    dcount += abs(adv)
    if adv >= 0:
        score = xdice.rolldice(dsize, dcount, adv, 0)
    elif adv < 0:
        score = xdice.rolldice(dsize, dcount, 0, adv)

    rolls = []
    dropped = score.dropped

    for res in list(score):
        roll = [int(res)]
        while res == dsize or (destructive and res == dsize - 1):
            score = xdice.rolldice(dsize, 1, 0, 0)
            res = int(score)
            roll.append(res)
        rolls.append(roll)

    return rolls, dropped


def calculate_result(vicious, destructive, attr_score, adv, repeat_factor):
    results = []
    dcount, dsize = get_dice_from_attr(int(attr_score))

    if dcount > 0:
        info = "{}d{}".format(dcount, dsize)
        for i in range(repeat_factor):
            result = (roll20(0, vicious, destructive), rollAttr(
                dcount, dsize, adv, destructive))
            results.append(result)

    else:
        info = "0"
        for i in range(repeat_factor):
            result = (roll20(adv, vicious, destructive), ([[0]], [0]))
        results.append(result)

    return results, info


def get_dice_from_attr(attr_score):
    count, size = 0, 0
    if attr_score == 0:
        return count, size
    elif attr_score == 1:
        count, size = 1, 4
        return count, size
    elif attr_score == 2:
        count, size = 1, 6
        return count, size
    elif attr_score == 3:
        count, size = 1, 8
        return count, size
    elif attr_score == 4:
        count, size = 1, 10
        return count, size
    elif attr_score == 5:
        count, size = 2, 6
        return count, size
    elif attr_score == 6:
        count, size = 2, 8
        return count, size
    elif attr_score == 7:
        count, size = 2, 10
        return count, size
    elif attr_score == 8:
        count, size = 3, 8
        return count, size
    elif attr_score == 9:
        count, size = 3, 10
        return count, size
    elif attr_score == 10:
        count, size = 4, 8
        return count, size
    elif attr_score > 10:
        count, size = 4, 8
        return count, size


def roll_raw(pattern):
    try:
        xdice_pattern = xdice.Pattern(pattern)
    except ValueError:
        return -1
    return xdice_pattern.roll()
