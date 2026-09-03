import pandas as pd

from sklearn.cluster import AgglomerativeClustering
from sentence_transformers import SentenceTransformer

from crawler.content_extractor import extract_content


MODEL = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def generate_focus_topics(page):

    text = (
        page["title"]
        + " "
        + " ".join(page["h1"])
        + " "
        + " ".join(page["h2"])
    )

    words = text.split()

    words = [
        word
        for word in words
        if len(word) > 4
    ]

    unique_words = list(
        dict.fromkeys(words)
    )

    focus_topic = ""

    if len(unique_words) > 0:
        focus_topic = unique_words[0]

    related_topics = unique_words[1:6]

    secondary_topics = unique_words[6:15]

    return {
        "focus": focus_topic,
        "related": related_topics,
        "secondary": secondary_topics
    }


def run_analysis(urls):

    pages = []

    for url in urls:

        result = extract_content(url)

        if "error" not in result:
            pages.append(result)

    if len(pages) == 0:

        return {
            "summary": {},
            "clusters": pd.DataFrame()
        }

    text_list = []

    for page in pages:

        complete_text = (
            page["title"]
            + " "
            + " ".join(page["h1"])
            + " "
            + page["content"][:5000]
        )

        text_list.append(
            complete_text
        )

    embeddings = MODEL.encode(
        text_list
    )

    cluster_count = min(
        5,
        len(pages)
    )

    if cluster_count < 2:
        cluster_count = 2

    clustering = (
        AgglomerativeClustering(
            n_clusters=cluster_count
        )
    )

    labels = clustering.fit_predict(
        embeddings
    )

    cluster_rows = []

    for i, page in enumerate(pages):

        topics = generate_focus_topics(
            page
        )

        cluster_rows.append({

            "URL":
                page["url"],

            "Title":
                page["title"],

            "Cluster":
                int(labels[i]),

            "Focus Topic":
                topics["focus"],

            "Related Topics":
                ", ".join(
                    topics["related"]
                ),

            "Secondary Topics":
                ", ".join(
                    topics["secondary"]
                ),

            "Hyperlinks":
                len(page["links"])
        })

    return {

        "summary": {

            "URLs Processed":
                len(pages),

            "Clusters Found":
                cluster_count
        },

        "clusters":
            pd.DataFrame(
                cluster_rows
            ),

        "pages":
            pages
    }
