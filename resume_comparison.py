# OVERVIEW =======================================================================================================================================================================
'''
resume_comparison.py takes a user's resume embedding and compares it to the embeddings of many jobs scraped from a job listing site. Then, the top matches are returned in an HTML
document titled Top_N_Jobs.html which can be viewed from your machine's web broswer.
The ordered list is also output as a jsonl file in job_matching_project/user_ranked_jobs titled <my_resume_name>_ranked_jobs.jsonl in order of closest to furthest match.
These comparisons are done using SciPy 1.16.0's scipy.spatial.distance.cosine() function to calculate cosine distance between two vectors. 

To use resume_comparison.py, navigate to job_matching_project/embedding/embed_resume.py and read the overview that describes how to get an embedding for your resume.
Once you have your embedding, run this program in the command line as follows:

python resume_comparison.py <my_resume_name_without_path>.<extension>
OR
python3 resume_comparison.py <my_resume_name_without_path>.<extension>

Additionally, you may provide an optional argument, --num-jobs, in the command-line to specify the number of matches you want to see. This number is 10 by default.
'''
# ================================================================================================================================================================================





# IMPORTS ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from scipy.spatial import distance          # for for cosine distance (distance.cosine())
import json                                 # for manipulating json files
import html                                 # for displaying most similar jobs (html.escape() needed)
import argparse                             # for taking resume name as a command-line argument

from job.job_module import EmbeddedJob      # for making and keeping track of jobs and their assigned cosine distances

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





# CONSTANT DEFINITIONS ----------------------------------------------------------------------------------------------------------------------------------------------------------

TOP_N = 10  # top N most similar jobs that will be displayed

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





# FUNCTIONS DEFINTIONS ----------------------------------------------------------------------------------------------------------------------------------------------------------

# gets all jobs with their associated embeddings from a jsonl file
def get_embedded_jobs(filename: str) -> list[EmbeddedJob]:
    embedded_jobs = []  # stores EmbeddedJob objects

    try:
        # opens the jsonl and stores each line (individual json object) as an EmbeddedJob object
        with open(filename, "r", encoding = "utf-8") as fin:
            for line in fin:
                job = json.loads(line)

                embedded_jobs.append(
                    EmbeddedJob(
                        job['title'],
                        job['company'],
                        job['location'],
                        job['full_description'],
                        job['embedding']
                    )
                )
        return embedded_jobs
    except Exception as e:
        print(f"Error in retrieving job vectors from {filename}: {e}")
        exit(-1)

# gets the embedding vector from a json file for the user resume
def get_resume_vector(filename: str) -> list[float]:
    try:
        # open the json file and read the content, returning the embedding
        with open(filename, "r", encoding = "utf-8") as fin:
            return json.loads(fin.read())['embedding']
    except Exception as e:
        print(f"Error in retrieving resume vector from {filename}: {e}")
        exit(-1)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





# MAIN ==========================================================================================================================================================================

if __name__ == "__main__":

# Take command-line arguments for resume name and number of job matches ---------------------------------------------------------------------------------------------------------

    parser = argparse.ArgumentParser()

    # positional arguments
    parser.add_argument(help = "Enter your resume file name (resume should be placed in the job_matching_project/user_resumes directory).", dest = 'resume_name', type = str)

    # optional arguments
    parser.add_argument("--num-jobs", help = f"Enter the number of jobs you want to see (default: {TOP_N})", dest = 'num_jobs', type = int, default = TOP_N)

    args = parser.parse_args()

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    resume_name = args.resume_name.rsplit('.', 1)[0]
    resume_path = f"user_resume_embeddings/{resume_name}_embedding.json"     # create resume embedding path

    jobs = get_embedded_jobs("job_data/jobs_embeddings.jsonl")
    resume_vector = get_resume_vector(resume_path)

    for job in jobs:
        try:
            job.add_cosine_distance(distance.cosine(resume_vector, job.embedding))
        except Exception as e:
            print(f"Error calculating cosine distance between resume vector and job vector for {job.title} -=- {job.company}: {e}")
            continue

    jobs.sort()     # sorts jobs in order of lowest cosine distance to highest (highest similarity to lowest)

    # add a ranked list of jobs to a jsonl file in user_ranked_jobs directory
    with open(f"user_ranked_jobs/{resume_name}_ranked_jobs.jsonl", "w", encoding = "utf-8") as fout:
        for job in jobs:
            try:
                json.dump(job.__dict__, fout)
                fout.write("\n")
            except Exception as e:
                print(f"Error writing ranked job {job.title} | {job.company} to ranked_jobs.jsonl: {e}")

    try:
        # open the html file and write the top 10 jobs to it (weird indentation to create pleasant html formatting)
        with open("Top_N_Jobs.html", "w", encoding = "utf-8") as fout:

            html_listing = f"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Top {args.num_jobs} Jobs</title>
        <meta charset="UTF-8">
    </head>

    <body style="margin: 20px">
        <h1 style="text-decoration: underline">Top {args.num_jobs} jobs for {html.escape(resume_name)}</h1>
        <ol>
"""
            # add an ol item for each job (min() in case there are less jobs than num_jobs) -- escape all strings to ensure proper html formatting
            for i in range(min(args.num_jobs, len(jobs))):
                job = jobs[i]
                html_description = html.escape(job.full_description).replace("\n", "<br>")  # html treats \n as a single space, so replace all with <br>

                html_listing += f"""
            <li>
                <h3>{html.escape(job.title)} | Similarity: {(1 - job.cosine_distance) * 100:.4f}%</h3>
                <ul>
                    <li><strong>Company:</strong> {html.escape(job.company)}</li>
                    <li><strong>Location:</strong> {html.escape(job.location)}</li>
                    <li>
                        <strong>Full Description -</strong>
                        <p>{html_description}</p>
                    </li>
                </ul>
            </li>
            """

            html_listing += f"""
        </ol>
    </body>
</html>
"""

            fout.write(html_listing)    # write the html top N to the html file (open this file in your browser to view results)

    except Exception as e:
        print(f"Error writing to Top_N_Jobs.html: {e}")
        exit(-1)

    print("Finished comparing resume to job data. View the results in Top_N_Jobs.html.")

# END MAIN ====================================================================================================================================================================