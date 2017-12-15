#Kai Murray 2019
import requests;
import html2text;
def getEbookContent(filename):
    text = open(filename, "r").read()
    return text
def fetchEbook(url):
    r = requests.get(url)
    rtext = html2text.html2text(r.text)
    rtext = rtext[rtext.find("* * *"):]
    rtext = rtext[:rtext.find("End of the Project")]
    return rtext
def stripEbook(text):
    text = text.lower()
    strippedChars = ['\\', '*', '_', '#', "\"", ".", "|", ",",
                     "?", "!", ":", ";", "-", " \'", "\' "]
    for strippedChar in strippedChars:
        text = text.replace(strippedChar, " ")
    text = text.replace("\'s", "")
    return text
def countWordFreq(text):
    words = text.split()
    wordsDict = {}
    for i in range(len(words)):
        if words[i] not in list(wordsDict.keys()):
            wordsDict[words[i]] = 0
        wordsDict[words[i]] = wordsDict[words[i]] + 1
    return wordsDict
def sortWordFreq(wordsDict, amount=20):
    length = len(wordsDict)
    wordsSorted = sorted(wordsDict, key = wordsDict.__getitem__)
    wordsDictSorted = {}
    for i in range(length - 1, length - min([amount, length]) - 1, -1):
        wordsDictSorted[wordsSorted[i]] = wordsDict[wordsSorted[i]]
    return wordsDictSorted
def getChapterNames(text):
    sliced = text[text.find("contents") + 13:text.find("contents") + 465]
    lines = sliced.splitlines()
    chapterList = []
    for line in lines:
        words = line.split()
        if len(words) > 0:
            chapterName = " ".join(words[1:])
            chapterList.append(chapterName)
    return chapterList
def removeContents(text):
    return text[text.find("adventure  i"):]
def getChapters(text, chapterNames):
    chapters = [text]
    for i in range(len(chapterNames) - 1):
        chapter = text[text.find(chapterNames[i]):
                       text.find(chapterNames[i + 1]) - 20]
        chapters.append(chapter)
    lastChapter = text[text.find(chapterNames[-1]):]
    chapters.append(lastChapter)
    return chapters
def main():
    #rawEbook = getEbookContent("1661-8.txt")
    rawEbook = fetchEbook("http://www.gutenberg.org/files/1661/1661-h/1661-h.htm")
    ebook = stripEbook(rawEbook)
    chapterNames = getChapterNames(ebook)
    chapters = getChapters(removeContents(ebook), chapterNames)
    specialWords = ["i", "you", "sherlock", "holmes", "watson",
                    "mystery", "adventure", "crime", "dead", "observe"]
    print("tracked words:")
    for word in specialWords:
        print(word, end = " ")
    print("")
    for i in range(len(chapters)):
        wordFreq = countWordFreq(chapters[i])
        specialWordFreq = {}
        for word in specialWords:
            try:
                specialWordFreq[word] = wordFreq[word]
            except KeyError:
                specialWordFreq[word] = 0
        specialWordsSorted = sortWordFreq(specialWordFreq, 20)
        ebookWords = sortWordFreq(wordFreq, 20)
        if i == 0:
            print("\n\nentire book\n")
        else:
            print("\n\nchapter ", i, ": ", chapterNames[i - 1], "\n", sep = "")
        for j in ebookWords:
            print("{0:<20} {1:>5}".format(*(j, ebookWords[j])))
        print("")
        for j in specialWordsSorted:
            print("{0:<20} {1:>5}".format(*(j, specialWordsSorted[j])))
main()







