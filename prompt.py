from langchain.document_loaders import PyPDFLoader # for loading the pdf
from langchain.document_loaders import UnstructuredPDFLoader

import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    # AIMessage,
    HumanMessage,
    # SystemMessage
)
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from templates import (
    RESUME_PARSING_TEMPLATE,
    JOB_DESCRIPTION_TEMPLATE,
    RATE_TEMPLATE,
    REACHOUT_EMAIL_TEMPLATE,
    GENERATE_SCREEN_QUESTION_TEMPLATE,
)
from models import OPENAI_BASE_MODEL


def call_llm(prompt, temperature=0, streaming=False, **kwargs):
    chat = ChatOpenAI(streaming=streaming, # display in screen or not
                      callbacks=[StreamingStdOutCallbackHandler()], 
                      temperature=temperature, 
                      **kwargs)
    response = chat([HumanMessage(content=prompt)]).content
    return response

def parse_resume(path, model=OPENAI_BASE_MODEL):
    """
    input: path (str)
    output: parsed_resume (str)
    """
    loader = UnstructuredPDFLoader(os.path.expanduser(path))
    pages = loader.load_and_split()
    resume = '\n'.join([page.page_content for page in pages])
    prompt = RESUME_PARSING_TEMPLATE.format(resume=resume)
    return call_llm(prompt=prompt, model_name=model)

def parse_job_description(job_description, model=OPENAI_BASE_MODEL):
    """
    input: job_description (str)
    output: parsed_job_description (str)
    """
    prompt = JOB_DESCRIPTION_TEMPLATE.format(job_description=job_description)
    return call_llm(prompt=prompt, model_name=model)
        
def rate_candidate(resume, job_description, model=OPENAI_BASE_MODEL):
    """
    input: resume (str), job_description (str)
    output: score (float)
    """
    prompt = RATE_TEMPLATE.format(
        resume=resume,
        job_description=job_description,
    )
    return call_llm(prompt=prompt, model_name=model)

def compose_reachout_email(cand_name, cand_email, job_description, work_experience, skills, model=OPENAI_BASE_MODEL):
    """
    input: resume (str), job_description (str), cand_name (str)
    output: score (float)
    """
    prompt = REACHOUT_EMAIL_TEMPLATE.format(
        cand_name=cand_name,
        cand_email=cand_email,
        job_description=job_description,
        work_experience=work_experience,
        skills=skills,
        length=50, # can be changed to long, short, medium length for different cases
    )
    return call_llm(prompt=prompt, model_name=model)

def generate_screen_questions(cand_name, job_description, work_experience, skills, num_questions, model=OPENAI_BASE_MODEL):
    """
    input: cand_name (str), job_description(json str), work_experience (str), skills (str)
    output: questions (str)
    """
    prompt = GENERATE_SCREEN_QUESTION_TEMPLATE.format(
        cand_name=cand_name,
        job_description=job_description,
        work_experience=work_experience,
        skills=skills,
        num_questions=num_questions,
    )
    return call_llm(prompt=prompt, model_name=model)

