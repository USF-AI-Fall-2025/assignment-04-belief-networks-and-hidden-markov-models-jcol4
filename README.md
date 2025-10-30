# Belief-Networks-Hidden-Markov-Models
Fall 2025 CS 362/562
Reflection
1. Give an example of a word which was correctly spelled by the user, but which was incorrectly “corrected” by the algorithm. Why did this happen?
I entered multifaceted, and the program output
Enter a word (or 'quit' to exit): multifaceted
Corrected: muatifaceted
I believe this occured because in my transition probabilities, m->u->a is a higher probability than m->u->l. Looking at the aspell.txt, while there is no m->u, there are a few correct words that contain m->->a, which would make my program more skewed to place a higher probability on m->u->a being the most likely "correct" sequence as it results in a higher path probability.

2. Give an example of a word which was incorrectly spelled by the user, but which was still incorrectly “corrected” by the algorithm. Why did this happen?
I entered plesae, meaning for please, and the program output
Enter a word (or 'quit' to exit): plesae
Corrected: pleste
Again, looking at aspell.txt, while please is not a word found, the pattern p->l->e is found 6 times. Mainly though, the pattern s->t->e is very common in aspell.txt, while a->s->e is only found once, leading me to believe that it saw a higher probability of the ending of the word being s->t->e, since that  is found in multiple correct words, while please is a very improbable sequence based on the data. In conclusion, the cumulative path probability is skewed towards an ending with s->t->e.

3. Give an example of a word which was incorrectly spelled by the user, and was correctly corrected by the algorithm. Why was this one correctly corrected, while the previous two were not?
I entered psle, meaning for pale, and the program output 
Enter a word (or 'quit' to exit): psle
Corrected: pale
Looking at aspell.txt, while pale is not a correct word listed, there are a few words starting with p->a, and only one starting with p->s, which also has a very long length (psychologist). As such, the viterbi algorithm found that p->a->l->e was the most probable sequence due to p->a probably having a higher probability than all the other options.

4. How might the overall algorithm’s performance differ in the “real world” if that training dataset is taken from real typos collected from the internet, versus synthetic typos (programmatically generated)?
I believe the program would become more accurate, as it is probability based. As such, if it was based on statistically the most common errors versus some typos that seem rather rare in aspell.txt, such as fantasy: famdasy, which in my opinion is a little hard to make unintentionally. This would make it a more useful program.