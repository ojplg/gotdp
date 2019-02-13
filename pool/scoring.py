
COUPLES = [ ]

def compute_mortality_score(selections,characters):
    score = 0
    for selection in selections.picks():
        for character in characters:
            if( character == selection.character ):
                if( selection.outcome == character.status ):
                    score+=1
                else:
                    score-=1
    return score

def is_correct_couple(couple):
    for c in COUPLES:
        print("checking " + c[0] + " and " + c[1] + " with " + str(couple))
        if ( c[0] == couple.left.name and c[1] == couple.right.name ):
            return True
    return False

def compute_romance_score(selections):
    score = 0
    for couple in selections.couples():
        if is_correct_couple(couple):
            score += 4
        else:
            score -= 1
    return score

def calculate_score(selections, characters):
    mortality_score = compute_mortality_score(selections,characters)
    romance_score = compute_romance_score(selections)
    return (mortality_score, romance_score, mortality_score + romance_score)

