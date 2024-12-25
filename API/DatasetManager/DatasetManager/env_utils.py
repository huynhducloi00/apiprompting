import os
def set_env():
    cache='/work/cvp352/loi_work/2025/hf_cache'
    os.environ['HF_HOME']=cache
    os.environ['HF_DATASETS_CACHE']=cache