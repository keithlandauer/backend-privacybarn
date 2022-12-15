import spacy
from spacy.matcher import PhraseMatcher
from collections import defaultdict    
from dateutil import parser
# set up global nlp 
nlp = spacy.load("en_core_web_sm")

class spacyClass:
    # spacy matcher object

    def __init__(self, t):
        self.patterns = [None]*30 
        self.patterns[0] = [nlp("do not sell"), nlp("will not sell"), nlp("do not rent or sell"), nlp("will not rent or sell"), nlp("never sell"), nlp("never rent")]
        self.patterns[1] = [nlp("datum be aggregate"),nlp("store aggregate"),nlp("de-identify"), nlp("aggregate information"), nlp("aggregate into statistic"), nlp("aggregate or pseudonymize"), nlp("aggregate statistic"), nlp("not contain personally identifiable"), nlp("non personally identifiable"), nlp("aggregate information")]
        self.patterns[2] = [nlp("collect personal datum"), nlp("collect a variety of information"), nlp("include personal information"), nlp("collect personal information"), nlp("collect many different type of personal"), nlp("information we may collect")] 
        self.patterns[3] = [nlp("partner provide information"), nlp("we receive personal datum"), nlp("receive information"), nlp("collect browsing information"), nlp("activity on third party"), nlp("whether or not you be log")]
        self.patterns[4] = [nlp("datum protection authority"), nlp("datum protection office"), nlp("datum protection officer"), nlp("datum protection supervisor"), nlp("datum protection regulation"), nlp("datum protection supervisory")]
        self.patterns[5] = [nlp("do not collect use or share location"), nlp("do not store personal information"), nlp("no IP address")]
        self.patterns[6] = [nlp("collect location information"), nlp("about your location"), nlp("precise location"), nlp("determine a location")]
        self.patterns[7] = [nlp("use for many different purpose"), nlp("for the follow purpose"), nlp("personalize your experience"), nlp("provide advertising"), nlp("collect datum for various reason"), nlp("use for a variety of purpose"), nlp("personalize our service"), nlp("we use the information")]
        self.patterns[8] = [nlp("scan and analyze"), nlp("scan technology"), nlp("review your message"), nlp("private message"), nlp("content of the communication")]
        self.patterns[9] = [nlp("receive certain information"), nlp("receive information"), nlp("other website"), nlp("third party website")]
        self.patterns[10] = [nlp("cookie be not"), nlp("cookie do not"), nlp("do not use cookie")]
        self.patterns[11] = [nlp("google analytics"), nlp("third party cookie"), nlp("partner use"), nlp("third party advertise"), nlp("third party service provider")]
        self.patterns[12] = [nlp("refer page"), nlp("refer source"), nlp("refer web page"), nlp("exit page"), nlp('exit web'), nlp("referral web page"), nlp("referral source"), nlp("referral website")]
        self.patterns[13] = [nlp("do not use any cookie or track"), nlp("do not use cookie"), nlp("never collect"), nlp("not be track"), nlp("do not track")]
        self.patterns[14] = [nlp("facebook pixel"),nlp ("social media cookie"), nlp("social media feature"), nlp("pixel tag")]
        self.patterns[15] = [nlp("refuse cookie"), nlp("refuse our cookie"), nlp("reject cookie"), nlp("reject our cookie"), nlp("block cookie"), nlp("block all cookie"), nlp("delete cookie"), nlp("disable cookie"), nlp("decline cookie")]
        self.patterns[16] = [nlp("session cookie"), nlp("temporary cookie"), nlp("session datum")]
        self.patterns[17] = [nlp("web beacon"), nlp("tracking pixel"),nlp("browser fingerprint"), nlp("device fingerpint"), nlp("pixel tag")]
        self.patterns[18] = [nlp("flash cookie")]
        self.patterns[19] = [nlp("do not respond to"), nlp("do not recognize"), nlp("do not current recognize"), nlp("do not currently respond")]
        self.patterns[20] = [nlp("enable do not track"), nlp("do not track enable"), nlp("respect your browser")]
        self.patterns[21] = [nlp("security breach"), nlp("breach of security"), nlp("datum breach"), nlp("breach of datum")]
        self.patterns[22] = [nlp("long as is necessary"), nlp("long as necessary"), nlp("retain your personal datum"), nlp("retain your datum")]
        self.patterns[23] = [nlp("do not log your ip"), nlp("do not collect ip"), nlp("do not record your login ip"), nlp("do not record your ip")]
        self.patterns[24] = [nlp("collect your IP address"), nlp("include your ip address"), nlp("include ip address"), nlp("such as ip address"), nlp("such as your ip address"), nlp("approximate location")]
        self.patterns[25] = [nlp("gps")]
        self.patterns[26] = [nlp("biometric"), nlp("fingerprint"), nlp("call recording")]
        self.patterns[27] = [nlp("browse history")]
        self.patterns[28] = [nlp("right to request"), nlp("request access"), nlp("request deletion"), nlp("delete your information")]
        self.patterns[29] = [nlp("copy of your personal datum"), nlp("copy of the personal datum"), nlp("copy of your personal information"), nlp("copy of this personal information")]
        self.fullText =  t
        self.matchedDict = defaultdict(list)
        self.matcher = PhraseMatcher(nlp.vocab, attr="LEMMA")
        self.doc = None
        self.sentence = [] 


    def set_text(self, t):
        """This is a simple setter for the text that the user will provide.

        Args:
            t (String): fullText of policy 
        """        
        self.fullText = t 

    def clean_lemmatize(self):
        self.doc = nlp(self.fullText.lower())

    def find_date(self):
        """This function finds the date of the policy and converts it to 'yyyy-mm-dd' format for the database.

        Returns:
            str: yyyy-mm-dd 
        """
        
        dates = [str(ent) for ent in self.doc.ents if ent.label_ == 'DATE']
        finalDate = parser.parse(dates[0].strip())
        # print(finalDate)
        # finalDate = finalDate[:len(finalDate) - 9]
        return str(finalDate)

    def phrase_match(self):
        """This is the main function for automatic annotations of a privacy policy. It uses pre-approved phrases and searches text for matches."""
             
        for i in range(30):
            self.matcher.add("ID", self.patterns[i])
            match = self.matcher(self.doc)
            self.matcher.remove("ID")
            for match_id, start, end in match:
                span = self.doc[start:end]
                self.matchedDict[i].append(span)
                sent = str(span.sent).capitalize()
                self.sentence.append(sent) 

    def testMatch(self):
        
        self.matcher.add("ID", self.patterns[0])
        self.clean_lemmatize()
        match = self.matcher(self.doc)
        self.matcher.remove("ID")
        for match_id, start, end in match:
            print("matched")
            span = self.doc[start:end]
            sents = str(span.sent)
            print(span, "||||||", sents)
    
sp = spacyClass("effective: june 29, 2022")
sp.clean_lemmatize()
sp.find_date()