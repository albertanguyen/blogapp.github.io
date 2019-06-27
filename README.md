# CoderSchool FTW - *Blog Flask app*

Created with :blue_heart: by: Anh Nguyen
    
[//]: # (One or two sentence summary of your project.)

[//]: # (## Video Walkthrough)

[//]: # (Here's a walkthrough of implemented user stories.)


## User Stories

The following **required** functionalities are completed:

THE USER is


The following **optional** features are implemented:
THE USER is


**Bonus Requirements**

[//]: # (The following **additional** features are implemented:)

[//]: # (* [x] List anything else that you can get done to improve the page!)

## Time Spent and Lessons Learned
* Using <a href="https://pypi.org/">this site</a> to check the latest version of all dependencies

## Describe any challenges encountered while building the app (retrived several of my google queries).
* Cannot create different python version or switch between python version in <code>venv</code>. It is impossible since to first create a virtual environment, we had to specify the python version. Somehow along the way, I have overidden python 3.x to python 2.x. As a side note, in <a href="https://stackoverflow.com/questions/22681824/how-do-i-use-different-python-version-in-venv-from-standard-library-not-virtua">this answer</a>, they suggest using pyenv to handle dependency version in python.
* We would have to delete the whole table db and migration directory if we created a new column (decided to change the database structure) after already running it.
* Need to setup <code>requirements.txt</code> file because I screwed up python version in venv meaning I need to delete the old one, create new one  and install all dependecies via <code>pip install -r requirements.txt</code>. For more information, please refer to <a href="https://devcenter.heroku.com/articles/python-pip">this link</a>.

## Version 1.0.0
Adapted from the <a href="https://www.youtube.com/watch?v=h0GStcG17X8&feature=youtu.be" target="_blank">live demo</a> of Mr. Khanh

## License

    Copyright 2019 Anh Nguyen

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
