# AI-Powered EcoGenomics

A web application that provides inexpensive computational methods of assessing biodiversity and both genomic and environmental components of resilience with genome skims.
***This website is still in development and only available for local usage***

## Local Installation
***Pythong 3.6 and up is required to install locally***
1. Clone the repository
2. Navigate to your cloned repository and set up a virtual environment and install all dependencies:
   - Using conda:
   '''bash
   conda env create -f environment.yml
   conda activate env
   '''
   - Using pip:
   '''bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   '''
3. Set up flask development server
   '''bash
   export FLASK_APP=run.py
   export FLASK_ENV=development
   '''

## Local Usage
Follow this instruction whenever you want to run the web application on local computer (after installation)
- For the application to run as expected, user must install all tools listed in the "tools" section. Please refer to the git repoistory linked in the description.
1. Go to the cloned local directory
2. Activate the virtual environment:
   - Using conda:
   '''bash
   conda activate env
   '''
   - Using pip:
   '''bash
   source env/bin/activate
   '''
3. Use following command line to run Flask application:
   '''bash
   flask run
   '''
4. Once ran, development server will be running on ''' localhost:5000 ''' in your default web browser



## Tools

**CONSULT:** Remove contamination by filtering extraneous reads
  - To install this tool in your local computer refer [here](https://github.com/noraracht/CONSULT).
**RESPECT:** Given the cleaned  up reads, RESPECT will output the estimated genomic length of the species and the repeat spectrum.
  - To install this tool in your local computer refer [here](https://github.com/shahab-sarmashghi/RESPECT).
**Skmer:** Estimate distances between genomes from low-coverage sequencing reads (genome-skims), without needing any assembly or alignment step
  - To install this tool in your local computer refer [here](https://github.com/shahab-sarmashghi/Skmer).
**APPLE:** Accurately phylogenetically place the reads into tree
  - *Not integrated into the website yet*
**MISA:** Analyze mixed samples of multiple species that are hard to physically separate before sequencing
  - *Not integrated into the website yet*

## Online Usage
### Home Page
- When development server starts running, the home page looks like this:
  - ![Home Page 1](https://github.com/sarahki511/senior-design/blob/master/app/static/image/home_pg1.png)
    - Fist Look of the home page includes:
      - Navigation Bar:
        - **Home:** Allows users to navigate back to the home page wherever they in the website (this is the default of the website)
        - **Flow Diagram:** Since there are more than one way for the users to use each tools, there is a basic flowchart that shows the users the basic pipeline of the tools. There are 4 different pipeline that the users can use on this website: 1. Processing of Individual Query and References 2. Distance Estimation 3. Indication of Query 4. Mixture of Analysis. The diagram shows the relationship between one pipeline to the other.
        - **App:** This is a dropdown menu that allows user to navigate to any one of the tools that are described in the ["Tools"](# Tools) section. When any one of the options are selected, it navigates the users to a page that describes the function of the tool and allows the users to run each tools individually and separately from the pipeline.
        - **Contact Us:** Navigates the users to the contact page. Users can contact the developers using this function.
      - Header: This has a basic description of the website also giving the user the option to know more about the website by referring them to a link that has a more indepth description of the project.
      - Choose your Pipeline: This section gives access to the tools from the very beginning. Pipeline 1, 2, 3, and 4 are buttons that navigate the users to the respective page that allows users to input their sample reads to run the set of tools that are needed to execute each of the pipeline. 
    - Second Page of home page:
      - Scroll down to the second page of the home page, and we will see the flow diagram of the tools:
        - ![Flow Diagram pg](https://github.com/sarahki511/senior-design/blob/master/app/static/image/flow_diagram.png)
    - Third Page of home page:
      - Scroll down to the third page of the home page, and we will see the Applications that are included in the website:
        - ![Applications pg](https://github.com/sarahki511/senior-design/blob/master/app/static/image/application_pg.png)
            - Each tools shown are buttons that takes users to the page that describes and run each tool.
- When the user clicks on any of the Application tools, the user will see the following form:
    - ![Inside App](https://github.com/sarahki511/senior-design/blob/master/app/static/image/inside_app.png)
        - After a brief explanation of the tool, there is a form that allows users to run the tools individually from the pipeline.
        - User email is required since the tool is ran independently of local computer. Inputting email allows the users to navigate away from the web page and still receive the results via email.
        - Once the user submits the sample input and email address and the results are processed, the user will receive an email with a link to the results page with the visualization of the output and text files that contains the output:
            - ![Email Results Example](https://github.com/sarahki511/senior-design/blob/master/app/static/image/email_results.png)
- Results Page:
    - The visualization is still in development
- Contact Us page:
    - ![Contact Us Page](https://github.com/sarahki511/senior-design/blob/master/app/static/image/conact_us.png)
        - Asks for user's Name, email address and Reason of Contact
        - When the email is sent to the user, the developers will receive an email of this form





