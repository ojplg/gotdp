
from collections import Counter
from .models import Character, Selection, Selections, Couple

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

def character_sums(characters):
    allSelections = Selection.objects.all()
    deadCount = Counter()
    liveCount = Counter()
    for character in characters:
        deadCount[character] = 0
        liveCount[character] = 0
    for selection in allSelections:
        if selection.outcome == 'L' :
            liveCount[selection.character] += 1
        if selection.outcome == 'D' :
            deadCount[selection.character] += 1
    livePercentage = {}
    for character in characters:
        liveVotes = liveCount[character]
        deadVotes = deadCount[character]
        total = liveVotes + deadVotes
        if total == 0:
            livePercentage[character] = 0
        else: 
            livePercentage[character] = round(100 * liveVotes / ( liveVotes + deadVotes ), 1)
    return (deadCount, liveCount, livePercentage)
 
def calculate_couple_counts():
    allCouples = Couple.objects.all()
    coupleCounts = Counter()
    for couple in allCouples:
        key = (couple.left.name, couple.right.name)
        coupleCounts[key] += 1
    return coupleCounts
        
        
