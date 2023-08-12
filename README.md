# number go up 

#### Installation

```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

#### Usage

```bash
export FLASK_APP=serve.py; export FLASK_DEBUG=true; flask run
```

#### Structure 
```bash
+-- serve.py 
+-- gpt.py 
|   +-- main 
|   |   +-- core.py 
|   +-- prompts 
|   |   +-- classifier.yaml 
```

#### Implementation 
1. User asks a question
2. LLM classifies question into a label 
3. If cls identified, LLM gets params to evaluate 
4. number go up evaluates params which could be an api call or function call
5. number go up returns answer to client 

ngup - number go up
