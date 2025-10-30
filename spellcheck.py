from collections import defaultdict, Counter

def load_aspell(filename="aspell.txt"):
    correct_to_typo = defaultdict(list)
    #open file
    with open(filename, "r") as f:
        #for every line, strip, make sure valid format, strip correct and typos
        for line in f:
            line = line.strip()
            if not line or ':' not in line:
                continue
            correct, typos = line.split(':')
            correct = correct.strip().lower()
            typos = typos.strip().split()
            #make all typos point to correct word
            correct_to_typo[correct].extend([t.lower() for t in typos])
    return correct_to_typo

#keep counter of emmited characters for each state(letter)
def build_emissions(correct_to_typo):
    emissions = defaultdict(Counter)
    #for every correct-typos pair
    for correct, typos in correct_to_typo.items():
        for i, c in enumerate(correct):
            #count correct letter since that should be most probable
            emissions[c][c] += 1
        for typo in typos:
            #for every typo, if within length of correct, increment
            for i, c in enumerate(typo):
                if i < len(correct):
                    emissions[correct[i]][c] += 1
                else:
                    #else count extra letters
                    emissions['<END>'][c] += 1
    for state, counts in emissions.items():
        #convert into probabilities - find total, then find probability for count[k] - for every key in counts
        total = sum(counts.values())
        for k in counts:
            counts[k] /= total
    return emissions

def build_transitions(correct_to_typo):
    transitions = defaultdict(Counter)
    #for every word
    for word in correct_to_typo:
        #add start and end tokens around word to signify word - a_11 and a_nn
        letters = ['<START>'] + list(word) + ['<END>']
        #count transitions in word
        for a, b in zip(letters, letters[1:]):
            transitions[a][b] += 1
    #normalize probabilties, same as emissions
    for state, counts in transitions.items():
        total = sum(counts.values())
        for k in counts:
            counts[k] /= total
    return transitions

def viterbi(word, states, T, E):
    #make word list of letters
    word = list(word)
    #V is max probabilities at each position and state, and we store best previous states in backpointer
    n = len(word)
    V = [{}]
    backpointer = [{}]

    #get prob of starting in each state and finding first char of word - use 1e-6 to avoid 0
    for s in states:
        V[0][s] = T['<START>'].get(s, 1e-6) * E[s].get(word[0], 1e-6)
        #make previous state
        backpointer[0][s] = '<START>'

    #for every next letter in word - 1 -> n (len(word))
    for t in range(1, n):
        V.append({})
        backpointer.append({})
        #for every current state, also consider previous states
        for s in states:
            max_prob = 0
            best_prev = None
            #generate prob that s fits into previous steps
            for s_prev in states:
                #first prob of s_prev being previous step
                #prob of moving from s_prev to s
                #prob that s emits observed letter
                prob = V[t-1][s_prev] * T[s_prev].get(s, 1e-6) * E[s].get(word[t], 1e-6)
                if prob > max_prob:
                    #update
                    max_prob = prob
                    best_prev = s_prev
            #store new probabilties
            V[t][s] = max_prob
            #previous state
            backpointer[t][s] = best_prev

    #after last letter in word - gone through all letters
    max_prob = 0
    best_last = None
    #get prob of going from last letter to end
    for s in states:
        #get prob of last letter -> <END>
        prob = V[-1][s] * T[s].get('<END>', 1e-6)
        #if new best prob, update
        if prob > max_prob:
            max_prob = prob
            best_last = s

    #get best last state and move backwards and create most likely sequence of letters
    result = [best_last]
    for t in range(n-1, 0, -1):
        #add best prev state and add to result and reverse
        result.append(backpointer[t][result[-1]])
    result.reverse()
    return ''.join(result)

#load text file of correct and typos pairs, make emissions and transitions, get the states
def spell_corrector():
    correct_to_typo = load_aspell()
    emissions = build_emissions(correct_to_typo)
    transitions = build_transitions(correct_to_typo)
    states = list(emissions.keys())

    if '<END>' in states:
        states.remove('<END>')

    #user in loop - if quit then delete
    while True:
        user_input = input("Enter a word (or 'quit' to exit): ").strip().lower()
        if user_input == "quit":
            break
        #get corrected word
        corrected = viterbi(user_input, states, transitions, emissions)
        print(f"Corrected: {corrected}")

if __name__ == "__main__":
    spell_corrector()
