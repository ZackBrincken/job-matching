# AI-Powered 💪 St. Louis Computer Science Job Matching System

This project allows the user to quickly compare their resume to hundreds of computer science job postings in the St. Louis, MO area and determine which ones are best for them.

### How it works

- Upload your resume.
- Have it compared to hundreds of computer science job listings from the St. Louis, MO area courtesy of Indeed.com.
- The top 10 most compatible jobs with the qualifications provided by your resume are found returned.

### Installation

##### Option 1 (Conda virtual environment, HIGHLY RECOMMENDED)

1. Make a local copy of this GitHub repository through `git clone https://github.com/ZackBrincken/job-matching.git` or your preferred method.
2. Install miniconda for python virtual environements if not already installed on your machine.
3. In your command-line, run `conda create --name <env_name> --file requirement.yml` to clone the environment this project was created in.
4. Activate the new environment by running `conda activate <env_name>` in your command-line. Now, you are ready to go.

#### Option 2 (Manually cloning the environment)

1. Make a local copy of this GitHub repository through `git clone https://github.com/ZackBrincken/job-matching.git` or your preferred method.
2. Install python on your machine. This program was written in a python version 3.11.13 environment, but any version 3.9+ is almost certainly fine.
3. Install pip or pip3 on your machine. This program was written in a pip version 25.1 environment, but any version is likely okay.
4. Using pip or pip3, install the requirements listed in `requirement.yml` or run the following commands in your command-line. As a disclaimer, this will install all project requirements onto your machine in their respective versions which will may be limiting and/or irritating when working with other projects in the future. This is why option 1 is highly recommended. If you must continue with option 2, run the following commands in your command-line (replace "pip" with "pip3" if you installed pip3):
```
1. pip install numpy
2. pip install selenium
3. pip install undetected-chromedriver
4. pip install openai
5. pip install scipy
```
Now, you are ready to go.

### Use

#### Use the sample resume

There is a sample resume provided in the user_resumes folder as well as that resume's embedding data in user_resume_embeddings and ranked jobs in user_ranked_jobs. There is also a pre-made HTML document called `Top_N_Jobs.html` that will display the top 10 jobs for the sample resume if opened in your browser. Feel free to look around at these files.

If you would like to see some of the magic work for yourself, go ahead and delete `Top_N_Jobs.html` from the home directory as well as `sample_resume_ranked_jobs.jsonl` from user_ranked_jobs. Don't worry, everything is in this repository, so you can't mess anything up. At this point, you will need to navigate to the project using your command-line. The easiest way to do this is to find the folder in which you cloned the GitHub repository in your file explorer and right click it. This should bring up a menu and one of the options should be along the lines of `Open in Terminal`. Click this option and a terminal should appear. Now, run the following command to recompare the sample resume to the jobs contained in job_data (python3 instead of python if that is what you are using):
```
python resume_comparison.py sample_resume.txt
```
You should see that Top_N_Jobs.html and sample_resume_ranked_jobs.jsonl have reappeared. What has happened (without getting into technical detail) is the resume's embedding--a numerical vector representation of the content of text--was compared to 600+ embeddings of job descriptions scraped from Indeed.com. This is done using a method called cosine similarity to quantify the similarity of two vectors. If you wish, you can view an extended list of job matches by running the command with `--num-jobs` as an optional command-line argument:
```
python resume_comparison.py sample_resume.txt --num-jobs <some_number>
```
This will recreate the Top_N_Jobs.html file and, upon refreshing your page, will now display however many jobs you specified.

#### Use your own resume

Using your own resume is substantially more useful, but also a bit more work. To do this, the first thing you will need to do is register an account on OpenAI's API platform. To do this, go to [OpenAI's website](https://openai.com/) and you should be able to select API in the top right corner of your screen (as of 06/28/2025). Now, you will be prompted to make an account. Once you have an account, it's time for the fun part: adding funds! Unfortunately, this project does require that you have a little bit of money in your OpenAI account. If this is too big of an issue for you, there are free embedding models out there, but using one would require you to modify the code in this project. On the bright side, it costs far less than a dollar to run this program, so put as little money in as you can. Now that you have funds in your account, follow these steps:

1. Navigate to your [API keys page](https://platform.openai.com/settings/organization/api-keys) on OpenAI's API platform and click `Create a new secret key` to get a new API key. Name this key whatever you like, select `Default project` in the `Project` dropdown menu, and give the key all permissions. Finally, click `Create secret key`
2. Now that you have created the key, make sure to copy it (the text provided) to a secure location and do not share it.
3. Run the following commands in your command-line based on your OS to make a new environment variable to store your key (replace &lt;yourkey&gt; with your key you saved):
```
WINDOWS:
setx OPENAI_API_KEY "<yourkey>"
```
```
LINUX / MACOS:
1. echo "export OPENAI_API_KEY='yourkey'" >> ~/.zshrc
2. source ~/.zshrc
```
4. Rewrite (or parse) your resume in a text (*.txt) document using as simple language as possible and place it in the user_resumes folder within your local cloned repository.
5. At this point, you will need to navigate to the project using your command-line. The easiest way to do this is to find the folder in which you cloned the GitHub repository in your file explorer and right click it. This should bring up a menu and one of the options should be along the lines of `Open in Terminal`. Click this option and a terminal should appear.
6. Now, you need to use OpenAI to create an embedding for your resume. This project uses OpenAI's text-embedding-3-large model which is relatively precise and very reasonably priced. To do this, execute the following commands in your terminal:
```
1. cd embedding
2. python embed_resume.py <resume_name>.txt
3. cd ..
```
7. These commands have ran embed_resume.py with your resume and now there should be a new file called &lt;resume_name&gt;_embedding_json in the user_resume_embeddings directory.
8. To get your job rankings, your resume's embedding will be compared with the 600+ computer science job listing embeddings from Indeed.com in the St. Louis, MO area via cosine similarity--a way of numerically comparing vectors of numbers. All you have to do to see this is run the following command in your terminal:
```
python resume_comparison.py <resume_name>.txt
```
9. Now, Top_N_Jobs.html will be rewritten to show the top 10 best matching jobs for your resume. Simply refresh your browser (or open Top_N_Jobs.html if you have not already) to see the results. Additionally, a file called <resume_name>_ranked_jobs.jsonl has been added to the user_ranked_jobs directory containing all jobs in order of most to least similar to your resume.
10. If you want to see more than 10 jobs, you can use the optional command-line argument `--num-jobs` to specify any number you like:
```
python resume_comparison.py <resume_name>.txt --num-jobs <num_jobs>
```

#### Embedding your own job listing data

If you would like, feel free to use the embed_data.py program within the embedding directory to add or replace the embedding data used for comparison with your own job listing data. This will also require the same API setup as described above and may require substantial changes to the program code. However, embed_data.py may still serve as a skeleton if you wish to do some embedding yourself, so feel free to play around with it!

### Scraping Plan

1. Go to indeed.com and scrape job data for all computer science jobs within 25 miles of St. Louis.
2. This will be done using Python 3.11.13, Selenium 4.33.0, and undetected-chromedriver 3.5.5.
3. Since Indeed's terms of service (TOS) explicitly prohibits the unauthorized scraping of data for commercial use, it is fair to assume scraping is generally not appreciated. Whether this is to keep their services exclusive or simply to reduce server lag, it is important to take their TOS into account. So, since the project requirements call for data from a high-profile job listings website (all of which prohibit scraping), there are slowdown functions (sleep, small_sleep, and tiny_sleep) implemented in various locations to reduce the load on the server. Additionally, this data will be used strictly for the academic purpose of designing this project, so no commercial gain will EVER be involved.
4. Each listing is scraped for its job title, company, location, and full job description.
5. This data is stored in a .jsonl file using the fields title, company, location, and full_description.

### Embedding Plan

This project uses OpenAI's text-embedding-3-large model to convert job descriptions into vectors of floating point numbers that can be easily compared to one another. text-embedding-3-large was chosen because it is a cheap model to use (the whole project costed less than $0.10) and it is more precise than it's counterpart, text-embedding-3-small. This model is technically slower than text-embedding-3-small, but it only took around 25-30 minutes to get all 600+ embeddings and that was with exceedingly careful rate limit avoidance including minute long delays to avoid the strictest tokens per minute limit as well as sending batches of around 26 descriptions per request to avoid daily request limits. Overall, this model worked very well for the project and the most similar jobs do seem fairly reasonable. I am glad I went with the higher precision model.

### Creation Tools

- Windows 11
- Python 3.11.13
- pip 25.1
- numpy 2.3.1
- SciPy 1.16.0
- Selenium 4.33.0
- Chrome + ChromeDriver
- Indeed (for data collection)
- undetected-chromedriver 3.5.5 websockets 15.0.1
- openai 1.92.2
- text-embedding-3-large and OpenAI API key