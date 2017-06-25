import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        self.pos = []
        self.neg = []

        with open(positives) as lines:
            for line in lines:
                if line.startswith(";") == False and line.startswith("\n") == False:
                    self.pos.append(line.strip())
                    
        with open(negatives) as lines:
            for line in lines:
                if line.startswith(";") == False and line.startswith("\n") == False:
                    self.neg.append(line.strip())





    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        count = 0
        self.tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = self.tokenizer.tokenize(text)
        for x in self.pos:
            for token_x in tokens:
                if x == token_x:
                    count += 1
        
        for y in self.neg:
            for token_y in tokens:
                if y == token_y:
                    count -= 1
                

        return count
