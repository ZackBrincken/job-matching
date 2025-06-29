# OVERVIEW ==========================================================================================================================================================================
'''
embed_resume.py leverages OpenAI's text-embedding-3-large model to create fairly precise embeddings for user resumes. This allows the resume to be easily compared numerically to
job listings that have undergone the same embedding process.

To use embed_resume.py, you must have a valid API key registered with OpenAI and a few cents USD in your account. Please follow official OpenAI documentation on how to set this up.
If you have done this, please upload a text-only version of your resume to the job_matching_project/user_resumes directory and run embed_resume.py as follows:

python embed_resume.py <my_resume_name_without_path>.<extension>
OR
python3 embed_resume.py <my_resume_name_without_path>.<extension>

This should create a json file in the job_matching_project/user_resume_embeddings directory titled <my_resume_without_path>_embedding.json and will contain the text from your 
resume as well as the embedding provided by text-embedding-3-large.

To see your top matches, please navigate to job_matching_project/resume_comparison.py and follow the instructions provided in the overview.
'''
# ===================================================================================================================================================================================





# IMPORTS ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from openai import OpenAI       # for interacting with OpenAI through their API
import json                     # for manipulating json files
import argparse                 # for command-line resume path argument

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





# MAIN =============================================================================================================================================================================

if __name__ == "__main__":

# Take command-line argument for resume name --------------------------------------------------------------------------------------------------------------------------------------

    parser = argparse.ArgumentParser()

    # positional arguments
    parser.add_argument(help = "Enter your resume file name (resume should be placed in the job_matching_project/user_resumes directory).", dest = 'resume_name', type = str)
    args = parser.parse_args()

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Get resume text ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    resume_path = f"../user_resumes/{args.resume_name}"     # create resume path

    try:
        # read user resume
        with open(resume_path, "r", encoding = "utf-8") as fin:
            resume = fin.read()
    except Exception as e:
        print(f"Error opening {resume_path}: {e}")
        exit(-1)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Create embedding -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    # create the client to interact with OpenAI through my API key
    client = OpenAI()

    try:
        # create the list of embeddings for the resume text (single element list)
        embedding = client.embeddings.create(
            model = "text-embedding-3-large",
            input = resume
        )
    except Exception as e:
        print(f"Error when trying to embed: {e}")
        exit(-1)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Write embedding to json ----------------------------------------------------------------------------------------------------------------------------------------------------------

    embedding_destination_path = f"../user_resume_embeddings/{args.resume_name.rsplit('.', 1)[0]}_embedding.json"     # create resume embedding path

    try:
        # write the embedding to a json file
        with open(embedding_destination_path, "w", encoding = "utf-8") as fout:
            resume_data = {
                'resume_text': resume,
                'embedding': embedding.data[0].embedding
            }

            json.dump(resume_data, fout)
    except Exception as e:
        print(f"Error when writing to {embedding_destination_path}: {e}")
        exit(-1)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# END MAIN ========================================================================================================================================================================