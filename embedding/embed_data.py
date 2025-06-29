# OVERVIEW ==========================================================================================================================================================================
'''
embed_data.py leverages OpenAI's text-embedding-3-large model to create fairly precise embeddings for many job descriptions. This allows user resumes to compared numerically
to job listings to find the closest matches.

To use embed_resume.py, you must have a valid API key registered with OpenAI some money in your account. Please follow official OpenAI documentation on how to set this up.
If you have done this, please upload your job listings to job_matching_project/job_data/jobs.jsonl following the format that can be seen inside. If you do not wish to follow this
format, some simple changes must be made to embed_data.py.

Once you have uploaded your job listings and registerd a valid API key with OpenAI, simply run embed_data.py as follows:

python embed_data.py
OR
python3 embed_data.py

There should now be a file called jobs_embeddings.jsonl in the job_matching_project/job_data directory. This file contains the same data as jobs.jsonl, but with the added
'embedding' field which stores the embedding provided by text-embedding-3-large.

Please note that, as embed_data.py stands, the 'full_description' field in jobs.jsonl will be the ONLY part taken into consideration when creating the text-embedding-3-large
embedding. If you wish to change this, fairly substantial changes must be made to embed_data.py.
'''
# ===================================================================================================================================================================================





# IMPORTS ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from openai import OpenAI       # for interacting with OpenAI through their API
import json                     # for manipulating json files
import time                     # for sleeping to avoid rate limits

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------





# CONSTANT DEFINTIONS --------------------------------------------------------------------------------------------------------------------------------------------------------------

TPM_LIMIT = 40000                                                   # the tokens per minute limit of the lowest tier of the text-embedding-3-large model
LARGEST_DESCRIPTION_IN_TOKENS = 1534                                # the greatest number of tokens in a single job description
MAX_BATCH_SIZE = int(TPM_LIMIT / LARGEST_DESCRIPTION_IN_TOKENS)     # the calculated max batch size to stay under the TPM rate limit

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





# EMBEDDING FUNCTION DEFINITION ----------------------------------------------------------------------------------------------------------------------------------------------------

# interacts with OpenAI to retrieve embeddings for all jobs and store them in a jsonl file
def embed_all(jobs, batch_size: int = MAX_BATCH_SIZE):
    # creates the client using my API key
    client = OpenAI()
    in_file = set()     # a set that will store all jobs that have embeddings in case the program must be ran multiple times

    # populates the in_file set by looking at which jobs are already in the jsonl file
    with open("../job_data/jobs_embeddings.jsonl", "r", encoding = "utf-8") as fin:
        for line in fin:
            try:
                job = json.loads(line)
                in_file.add(job['title'] + " -=- " + job['company'])    # creates a unique key for all jobs by combining the title and company
            except Exception as e:
                print(f"Error trying to retrieve line in jsonl: {e}")
                continue

    # opens the jsonl file and appends new jobs with embeddings
    with open("../job_data/jobs_embeddings.jsonl", "a", encoding = "utf-8") as fout:

        # for each job in batches of batch_size (default = MAX_BATCH_SIZE), get a batch of embeddings
        for i in range(0, len(jobs), batch_size):

            # construct the batch of jobs out of all jobs from i to i + batch_size which are not in in_file
            job_batch = [job for job in jobs[i:i + batch_size] if job['title'] + " -=- " + job['company'] not in in_file]

            # if job_batch is empty, continue
            if not job_batch:
                continue

            description_batch = [job['full_description'] for job in job_batch]  # make a batch of only job_descriptions to send to text-embedding-3-large

            try:
                # create the embeddings for all descriptions in the batch
                embeddings = client.embeddings.create(
                    model = "text-embedding-3-large",
                    input = description_batch
                )
            except Exception as e:
                print(f"Error in batch starting at job {i}: {e}")
                time.sleep(60)  # a minute long sleep to ensure that, in the case of unexpected errors, TPM limit is still respected
                continue

            # for each each embedding and its associated job, construct a json object
            for embedding, job in zip(embeddings.data, job_batch):

                job_data = {
                    'title': job['title'],
                    'company': job['company'],
                    'location': job['location'],
                    'full_description': job['full_description'],
                    'embedding': embedding.embedding
                }

                # dump the json object to the jsonl file and add it to the in_file set
                json.dump(job_data, fout)
                fout.write("\n")
                in_file.add(f"{job['title']} -=- {job['company']}")

            time.sleep(60)      # sleep for a minute before receiving the next batch (TPM limits)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





# MAIN =========================================================================================================================================================================

if __name__ == "__main__":

    jobs = []       # stores all the jobs to get embeddings

    # read all the jobs stored in the jobs jsonl
    with open("../job_data/jobs.jsonl", "r", encoding = "utf-8") as fin:

        for line in fin:

            line = line.strip()

            if line:
                jobs.append(json.loads(line))
            
    embed_all(jobs)     # create and store embeddings for each job

# END MAIN =====================================================================================================================================================================