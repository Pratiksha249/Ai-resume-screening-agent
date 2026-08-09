from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingMatcher:
    """
    Converts text into embeddings and calculates
    semantic similarity between job descriptions
    and resumes.
    """

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def create_embedding(self, text):
        """
        Convert text into a numerical embedding.
        """

        return self.model.encode([text])

    def calculate_similarity(self, text1, text2):
        """
        Calculate semantic similarity between two texts.
        """

        embedding1 = self.create_embedding(text1)
        embedding2 = self.create_embedding(text2)

        similarity = cosine_similarity(
            embedding1,
            embedding2
        )[0][0]

        return float(similarity)