import praw
import spacy

clientid = "RTdfPLIOwBEHZyxPGNKHbw"
clientsecret = "wUd9rYc5-XGRIbxUCxpcp5ZxO5SKLw"
useragent = "RedUniversity/0.1 by Own_Meal7959"
redirecturi = "https://github.com/AnikaitKadamb/redditUniversity.git"


nlp = spacy.load("en_core_web_sm")


reddit = praw.Reddit(
    client_id = clientid,
    client_secret = clientsecret,
    user_agent = useragent,
    redirect_uri = redirecturi
)


def get_course_posts(coursecode, subreddit, limit):
    posts = reddit.subreddit(subreddit).search(query = coursecode, sort = "relevance", limit=limit);

    return list(posts)


def add_comments(commentlist, comment):
    commentlist.append(comment.body)
    if len(comment.replies) > 0:
        for reply in comment.replies:
            add_comments(commentlist, reply)
    return

def get_posts_comments(posts):
    commentlist = [];
    for post in posts:
        post.comments.replace_more(limit=0);
        for comment in post.comments:
            add_comments(commentlist, comment)

    return commentlist


def get_clauses(comment):
    current_clause = []
    clauses = []
    doc = nlp(comment)
    for token in doc:
        if token.dep_ == "cc" or token.dep_ == "punct" or token.dep_ == "sconj":
            if current_clause:
                clauses.append(current_clause)
                current_clause = []
        else:
            current_clause.append(token)
    return clauses

def set_null_dict(dicto, nullval):
    if not dicto:
        return
    for item in dicto:
        dicto[item] = nullval
    return

def check_var(commentlist, checkdict):
    if not commentlist:
        return 0
    for comment in commentlist:
        clauses = get_clauses(comment)
        for clause in clauses:
            check = ""
            pos = True
            for token in clause:
                if token.lemma_ in checkdict:
                    print(token)
                    check = token.lemma_
                if token.dep_ == "neg":
                    pos = False
            if pos and check:
                checkdict[check] += 1
    return 1

def course_work_list(checkdict, categorydict, benchmark):
    tempdict = {}
    for key, value in checkdict.items():

        if value:
            tempdict[key] = min(100, round((value/benchmark)*100))
    #exams
    if "final" in tempdict:
        categorydict["Exams"]["final"] = 100
    if "midterm" in tempdict or "test" in tempdict:
        categorydict["Exams"]["midterm"] = max(tempdict["midterm"],tempdict["test"],86)

    #assignments
    for item in ["assignment","quiz","lab"]:
        if item in tempdict:
            categorydict["Assignments"][item] = tempdict[item]

    #projects
    for item in ["presentation","group","project","essay","research"]:
        if item in tempdict:
            if item == "group":
                categorydict["Projects"][item+" work"] = tempdict[item]
            categorydict["Projects"][item] = tempdict[item]

    finaldict = {}
    for key, value in categorydict.items():
        if value:
            finaldict[key] = value

    return finaldict




