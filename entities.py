class Arc:
    id="null"
    cnt=0
    def __init__(self, name):
        self.id = name
        self.cnt=1
    def frequency(self):
        return self.cnt
    def increase(self):
        self.cnt+=1

    def isID(self,name):
        if self.id==name:
            return True
        else:
            return False
class Trigram:
    id1="null"
    id2 = "null"
    id3="null"
    cnt=0
    def __init__(self, name1,name2,name3):
        self.id1 = name1
        self.id2 = name2
        self.id3 = name3
        self.cnt=1
    def frequency(self):
        return self.cnt
    def increase(self):
        self.cnt+=1
    def decrease(self):
        self.cnt-=1
    def isID(self,name1,name2,name3):
        if (self.id1==name1) and (self.id2==name2) and (self.id3==name3):
            return True
        else:
            return False



class Emit:
    id="null"
    cnt=0
    def __init__(self, name):
        self.id = name
        self.cnt=1
    def frequency(self):
        return self.cnt
    def increase(self):
        self.cnt+=1

    def isID(self,name):
        if self.id==name:
            return True
        else:
            return False
class Group:
    'Common base class for all employees'
    id = "null"
    total=0
    Arcs = []
    alphabet=[]
    total_arcs=0
    def __init__(self, name):
        self.id = name
        self.Arcs=[]
        self.alphabet=[]
        self.Trigrams=[]
        for i in range(97):
            e = Emit("*&^$$)@^$")
            listy = []
            listy.append(e)
            self.alphabet.append(listy)
        self.total=0
    def displayCount(self):
        return self.total
    def isID(self,name):
        if self.id==name:
            return True
        else:
            return False
    def addArc(self,grp):
        self.total_arcs+=1
        added=False
        for arc in self.Arcs:
            if arc.isID(grp):
                arc.increase()
                added=True
        if added!=True:
            arc=Arc(grp)
            self.Arcs.append(arc)
    def addEmission(self,word):
        self.total+=1
        added = False
        alp=self.alphabet[ord(word[0])-33]
        for emit in alp:
            if emit.isID(word):
                emit.increase()
                added = True
        if added != True:
            emit = Emit(word)
            alp.append(emit)
        #print(self.id)
        #print(len(self.Emits))
    def findEmissionFreq(self,word):
        alp = self.alphabet[ord(word[0]) - 33]
        for emit in alp:
            if emit.isID(word):
                return emit.frequency()
        return -1
    def find_transition_probability(self, grp):
        p=1.0
        for arc in self.Arcs:
            if arc.isID(grp):
                p=float(arc.frequency()/self.total_arcs)
                #print("transition freq ",arc.frequency(),self.total_arcs)
                return p
            #else:
                #print(arc.id+" is not "+grp)
        return 0
    def find_transition_frequency(self, grp):
        for arc in self.Arcs:
            if arc.isID(grp):
                return arc.frequency()
        return 0
class Sentence:
    words=[]
    pos=[]
    prob=[]
    def __init__(self):
        self.words = []
        self.pos = []
        self.prob = []
    def addToken(self,word):
        self.words.append(word)
    def addWord(self,word,pos,prob):
        self.words.append(word)
        self.pos.append(pos)
        self.prob.append(prob)
    def addSentence(self,sentence):
        for w in sentence.words:
            self.words.append(w)
        for p in sentence.pos:
            self.pos.append(p)
        for pr in sentence.prob:
            self.prob.append(pr)
    def lastGroup(self):
        return self.pos[len(self.pos)-1]
    def secondLastGroup(self):
        return self.pos[len(self.pos)-2]
    def length(self):
        return len(self.pos)
    def totalProbability(self):
        pr=1.0
        for p in self.prob:
            pr*=p
        return pr
    def printout(self):
        for w in self.words:
            print(w)
    def printoutp(self):
        for i in range(len(self.words)):
            print(self.words[i],self.pos[i],self.prob[i])
class Corpus:
    l1 = 0.3
    l2 = 0.5
    l3 = 0.2
    Groups=[]
    Trigrams = []
    def __init__(self):
        print("Starting the pass")
    def addWord(self,token,pos):
        if token.isdigit():
            added = False
            for group in self.Groups:
                if group.isID("CD"):
                    group.addEmission(token)
                    added = True
                    break
            if added != True:
                group = Group("CD")
                group.addEmission(token)
                self.Groups.append(group)
        else:
            added = False
            for group in self.Groups:
                if group.isID(pos):
                    group.addEmission(token)
                    added = True
                    break
            if added != True:
                group=Group(pos)
                group.addEmission(token)
                self.Groups.append(group)

    def addWordArc(self, token, pos,arc):
        if token.isdigit():
            added = False
            for group in self.Groups:
                if group.isID("CD"):
                    group.addEmission(token)
                    group.addArc(arc)
                    added = True
                    break
            if added != True:
                group = Group("CD")
                group.addEmission(token)
                group.addArc(arc)
                self.Groups.append(group)
        else:
            added = False
            for group in self.Groups:
                if group.isID(pos):
                    group.addEmission(token)
                    group.addArc(arc)
                    added = True
                    break
            if added != True:
                group=Group(pos)
                group.addEmission(token)
                group.addArc(arc)
                self.Groups.append(group)

    def addTrigramArc(self,posPrev,posLast):
        added=False
        for trigram in self.Trigrams:
            if(trigram.isID(posPrev[0],posPrev[1],posLast)):
                trigram.increase()
                added=True
                break
            if added!=True:
                t=Trigram(posPrev[0],posPrev[1],posLast)
                self.Trigrams.append(t)
    def find_transition_frequency(self,trigram):
        p=1.0
        ctr=0

        for group in self.Groups:
            if(group.isID(trigram.id1)):
                g1=group
                ctr+=1
            if(group.isID(trigram.id2)):
                g2=group
                ctr+=1
            if (group.isID(trigram.id3)):
                g3 = group
                ctr+=1
        else:
            p3=1.0*float(g3.displayCount()/len(self.Groups))
            p2=g2.find_transition_probability(g3.id)
            v=g1.find_transition_frequency(g2.id)
            if(v>0):
                p1=1.0*float(trigram.frequency()/v)
            else:
                p1=0
            p=self.l1*p1+self.l2*p2+self.l3*p3
        return p2
    def findEmissionProbabilities(self, word):
        found=False
        prob=[]
        pos=[]
        for group in self.Groups:
            f=group.findEmissionFreq(word)

            if int(f)>0:
                #print(word+" has an occurrence in "+group.id)
                p= f/group.total

                prob.append(p)
                pos.append(group.id)
        return prob,pos
    def findWordProbabilities(self, word,previous_grp):
        found = False
        prob = []
        pos = []
        previous=[]
        #if (word == "Accords") or (word == "counseling") or (word == "further") or (word == "Investors"):
            #print(word,previous_grp)
        for group in self.Groups:
            if group.isID(previous_grp):
                previous.append(group)
        for group in self.Groups:
            f = group.findEmissionFreq(word)


            if f > 0:
                if(len(previous)>0):
                    p = 1.0 * float(previous[0].find_transition_probability(group.id))
                else:
                    p=0.09
                p *= (f / group.total)
                #print(f,group.total,p)
                prob.append(p)
                pos.append(group.id)
        return prob, pos
    def findTrigramWordProbabilities(self, word3,group2,group1):
        found = False
        prob = []
        pos = []
        previous=[]
        #if(word3=="Accords")or(word3=="counseling")or(word3=="further")or(word3=="Investors"):
         #   print(word3,group2,group1)
        for group in self.Groups:
            f = group.findEmissionFreq(word3)
            if f > 0:
                for t in self.Trigrams:
                    if (t.isID(group1, group2, group.id)):
                        trigram = t
                        found = True
                if found!=True:
                    trigram=Trigram(group1, group2, group.id)
                    trigram.decrease()
                    self.Trigrams.append(trigram)
                p = 1.0 * float(self.find_transition_frequency(trigram))

                p *= (f / group.total)
                prob.append(p)
                pos.append(group.id)
        return prob, pos

    def viterbi(self,sentence):
        sentences=[]
        j=0

        for word in sentence.words:
            #print("word is ",word)
            prob = []
            pos = []
            if j==0:
                j=1
                if word.isdigit():
                    prob=[0.8]
                    pos=["CD"]
                else:
                    prob,pos=self.findEmissionProbabilities(word)
                    if(len(pos)==0):
                        '''if((ord(word[0])>=65)and(ord(word[0])<=90)):
                           prob.append(0.3)
                           pos.append("NNP")
                           print("Capital "+word)'''
                        if (word[len(word)-1]=='.'):
                           prob.append(0.3)
                           pos.append("NNP")
                           print("abbrev "+word)
                        elif(word.find("-")):
                            prob.append(0.09)
                            pos.append("VBG")
                            prob.append(0.09)
                            pos.append("VBD")
                            prob.append(0.2)
                            pos.append("VB")
                            prob.append(0.09)
                            pos.append("VBN")
                            prob.append(0.09)
                            pos.append("VBP")
                            prob.append(0.09)
                            pos.append("VBZ")
                            prob.append(0.3)
                            pos.append("JJ")
                            #print("hyphen "+word)
                        else:
                            for g in self.Groups:
                                prob.append(0.09)
                                pos.append(g.id)
                            #print("Unknown "+word)
                for i in range(len(pos)):
                    sen=Sentence()
                    sen.addWord(word,pos[i],prob[i])
                    sentences.append(sen)
                    #print("added ",pos[i]," for ",word)
            else:

                remove=[]
                adds=[]
                for sen in sentences:
                    prob = []
                    pos = []
                    #print("current sen is ")
                    #sen.printoutp()
                    if word.isdigit():
                        prob = [0.8]
                        pos = ["CD"]
                    else:
                        prob, pos = self.findWordProbabilities(word,sen.lastGroup())
                    if (len(pos) == 0):
                        if((ord(word[0])>=65)and(ord(word[0])<=90)):
                           prob.append(0.3)
                           pos.append("NNP")
                           prob.append(0.3)
                           pos.append("NNPS")
                           #print("Capital "+word)
                        elif (word[len(word) - 1] == '.'):
                            prob.append(0.3)
                            pos.append("NNP")
                            #print("abbrev " + word)
                        elif (word.find("-")!=-1):
                            prob.append(0.09)
                            pos.append("VBG")
                            prob.append(0.09)
                            pos.append("VBD")
                            prob.append(0.2)
                            pos.append("VB")
                            prob.append(0.09)
                            pos.append("VBN")
                            prob.append(0.09)
                            pos.append("VBP")
                            prob.append(0.09)
                            pos.append("VBZ")
                            prob.append(0.3)
                            pos.append("JJ")
                            #print("hyphen " + word)
                        else:
                            for g in self.Groups:
                                prob.append(0.09)
                                pos.append(g.id)
                            #print("Unknown " + word)
                    '''if(word=="."):
                        print("Debugging . ",prob,pos)'''
                    for i in range(len(pos)):
                        sen1=Sentence()
                        sen1.addSentence(sen)
                        sen1.addWord(word,pos[i],prob[i])
                        #print("added ", pos[i], " for ", word)
                        adds.append(sen1)
                        #print(len(adds))
                    remove.append(sen)
                '''print("Old")
                for s in sentences:
                    s.printout()'''
                for a in adds:
                    sentences.append(a)

                for r in remove:
                    sentences.remove(r)
                if(len(sentences)>5):
                    while(len(sentences)>5):
                        min=2.0
                        k=-1
                        i=0
                        for  sen in sentences:
                            v=sen.totalProbability()
                            if(v<min):
                                k=i
                                min=v
                            i += 1
                        sen=sentences[k]
                        sentences.remove(sen)
                '''print("New")
                for s in sentences:
                    s.printout()'''

                #j += 1
        max=0.0
        maxs=sentences[0]
        for s in sentences:
            if s.totalProbability()>max:
                maxs=s
                max=s.totalProbability()
        return maxs

    def viterbi_trigram(self, sentence):
        sentences = []
        j = 0

        for word in sentence.words:
            #print("word is ", word)
            prob = []
            pos = []
            if j == 0:
                j = 1
                if word.isdigit():
                    prob=[0.8]
                    pos=["CD"]
                else:
                    prob, pos = self.findEmissionProbabilities(word)
                    if (len(pos) == 0):
                        '''if((ord(word[0])>=65)and(ord(word[0])<=90)):
                           prob.append(0.3)
                           pos.append("NNP")
                           print("Capital "+word)'''
                        if (word[len(word) - 1] == '.'):
                            prob.append(0.3)
                            pos.append("NNP")
                            if (word[len(word) - 1] == '.'):
                                prob.append(0.3)
                                pos.append("NNPS")
                            #print("abbrev " + word)
                        elif (word.find("-")):
                            prob.append(0.09)
                            pos.append("VBG")
                            prob.append(0.09)
                            pos.append("VBD")
                            prob.append(0.2)
                            pos.append("VB")
                            prob.append(0.09)
                            pos.append("VBN")
                            prob.append(0.09)
                            pos.append("VBP")
                            prob.append(0.09)
                            pos.append("VBZ")
                            prob.append(0.3)
                            pos.append("JJ")
                            #print("hyphen " + word)
                        else:
                            for g in self.Groups:
                                prob.append(0.09)
                                pos.append(g.id)
                            #print("Unknown " + word)
                for i in range(len(pos)):
                    sen = Sentence()
                    sen.addWord(word, pos[i], prob[i])
                    sentences.append(sen)
                    # print("added ",pos[i]," for ",word)
            else:

                remove = []
                adds = []
                for sen in sentences:
                    prob = []
                    pos = []
                    # print("current sen is ")
                    # sen.printoutp()
                    if word.isdigit():
                        prob = [0.8]
                        pos = ["CD"]
                    else:
                        if (sen.length() <2):
                            prob, pos = self.findWordProbabilities(word, sen.lastGroup())
                        else:
                            prob, pos = self.findTrigramWordProbabilities(word, sen.lastGroup(), sen.secondLastGroup())
                    if (len(pos) == 0):
                        if ((ord(word[0]) >= 65) and (ord(word[0]) <= 90)):
                            prob.append(0.3)
                            pos.append("NNP")
                            #print("Capital " + word)
                        elif (word[len(word) - 1] == '.'):
                            prob.append(0.3)
                            pos.append("NNP")
                            #print("abbrev " + word)
                        elif (word.find("-") != -1):
                            prob.append(0.09)
                            pos.append("VBG")
                            prob.append(0.09)
                            pos.append("VBD")
                            prob.append(0.2)
                            pos.append("VB")
                            prob.append(0.09)
                            pos.append("VBN")
                            prob.append(0.09)
                            pos.append("VBP")
                            prob.append(0.09)
                            pos.append("VBZ")
                            prob.append(0.3)
                            pos.append("JJ")
                            #print("hyphen " + word)
                        else:
                            for g in self.Groups:
                                prob.append(0.09)
                                pos.append(g.id)
                            #print("Unknown " + word)
                    '''if(word=="."):
                        #print("Debugging . ",prob,pos)'''
                    for i in range(len(pos)):
                        sen1 = Sentence()
                        sen1.addSentence(sen)
                        sen1.addWord(word, pos[i], prob[i])
                        # print("added ", pos[i], " for ", word)
                        adds.append(sen1)
                        # print(len(adds))
                    remove.append(sen)
                '''print("Old")
                for s in sentences:
                    s.printout()'''
                for a in adds:
                    sentences.append(a)

                for r in remove:
                    sentences.remove(r)
                if (len(sentences) > 3):
                    while (len(sentences) > 3):
                        min = 2.0
                        k = -1
                        i = 0
                        for sen in sentences:
                            v = sen.totalProbability()
                            if (v < min):
                                k = i
                                min = v
                            i += 1
                        sen = sentences[k]
                        sentences.remove(sen)
                '''print("New")
                for s in sentences:
                    s.printout()'''

                # j += 1
        max = 0.0
        maxs = sentences[0]
        for s in sentences:
            if s.totalProbability() > max:
                maxs = s
                max = s.totalProbability()
        return maxs

    def printout(self):
        print("Groups\n")
        for group in self.Groups:
            print(group.id)

            print(group.total)

            print(group.total_arcs)

            '''for arc in group.Arcs:
                print(arc.id)

                print(arc.frequency())'''
            '''for a in group.alphabet:
                for emit in a:
                    print(emit.id)

                    print(emit.frequency())'''



'''c=Corpus()
c.addWord("nitisha","nn")
c.addWord("nitisha","nn")
c.addWordArc("run","vb","nn")'''
