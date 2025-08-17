from langfuse import Langfuse
# from core.config import LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_HOST

langfuse_client = Langfuse(
    secret_key="sk-lf-8a7c9180-32aa-47c7-af35-23ddeb070851",
    public_key="pk-lf-d812c460-f6cc-44d4-9dae-90042eaa7c46",
    host="https://cloud.langfuse.com"
)
