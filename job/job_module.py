# a Job class for storing initially scraped jobs
class Job:

    def __init__(self, title: str, company: str, location: str, full_description: str):
        self.title = title
        self.company = company
        self.location = location
        self.full_description = full_description

    # prints all attributes of a Job object by a <key>: <value>\n format (for debugging)
    def __str__(self):
        ret_str = ""
        for key, value in self.__dict__.items():
            ret_str += key + ": " + value + "\n"
        return ret_str
    




# an EmbeddedJob class for storing jobs that have been scraped and given embeddings
class EmbeddedJob:

    def __init__(self, title: str, company: str, location: str, full_description: str, embedding: list[float]):
        self.title = title
        self.company = company
        self.location = location
        self.full_description = full_description
        self.embedding = embedding
        self.cosine_distance = 1

    # prints all attributes of a Job object by a <key>: <value>\n format (for debugging)
    def __str__(self):
            ret_str = ""
            for key, value in self.__dict__.items():
                ret_str += key + ": " + value + "\n"
            return ret_str
    
    # defines the < operator for the class (for sorting, finding top N most similar jobs)
    def __lt__(self, other):
        return self.cosine_distance < other.cosine_distance
    
    # sets the cosine_distance for the job
    def add_cosine_distance(self, cosine_distance: float) -> None:
        self.cosine_distance = cosine_distance